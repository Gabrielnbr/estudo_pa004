from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold

import data_preparation as dp
import feature_engenniring as fe


DEFAULT_K_PERCENTAGE = 0.4


def load_pickle(path: Path) -> Any:
    with path.open("rb") as file:
        return pickle.load(file)

def _required(data: pd.DataFrame) -> pd.DataFrame:
    required = {"score", "resposta"}
    if not required.issubset(data.columns):
        raise ValueError(f"DataFrame precisa conter as colunas: {required}")
    return data.loc[:, ["score", "resposta"]].copy()


def _resolve_k(
    n_rows_total_df: int,
    k: int | None = None,
    k_percentage: float | None = None,
) -> int:
    if k is None:
        pct = DEFAULT_K_PERCENTAGE if k_percentage is None else k_percentage
        if not (0 < pct <= 1):
            raise ValueError(f"k_percentage precisa estar entre 0 e 1. Valor atual: {pct}")
        k = int(round(n_rows_total_df * pct))

    if k > n_rows_total_df:
        raise ValueError(
            "k precisa ser menor ou igual ao tamanho total do DataFrame.\n"
            f"k: {k};\n"
            f"linhas do DF: {n_rows_total_df}"
        )
    if k < 1:
        raise ValueError("k precisa ser >= 1.")

    return k


def precision_at_k(
    data: pd.DataFrame,
    k: int | None = None,
    k_percentage: float | None = None,
) -> float:
    ranked = _required(data).sort_values("score", ascending=False).reset_index(drop=True)
    ranked["ranking"] = ranked.index + 1
    ranked["precision_at_k"] = ranked["resposta"].cumsum() / ranked["ranking"]

    k_safe = _resolve_k(len(ranked), k, k_percentage)
    return float(ranked.loc[k_safe - 1, "precision_at_k"])


def recall_at_k(
    data: pd.DataFrame,
    k: int | None = None,
    k_percentage: float | None = None,
) -> float:
    ranked = _required(data).sort_values("score", ascending=False).reset_index(drop=True)
    positives = ranked["resposta"].sum()

    if positives == 0:
        return 0.0

    ranked["recall_at_k"] = ranked["resposta"].cumsum() / positives

    k_safe = _resolve_k(len(ranked), k, k_percentage)
    return float(ranked.loc[k_safe - 1, "recall_at_k"])


def ml_error(
    model: Any,
    data: pd.DataFrame,
    k: int | None = None,
    k_percentage: float | None = None,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Model_Name": [model.__class__.__name__],
            "precision_at_k": [precision_at_k(data, k=k, k_percentage=k_percentage)],
            "recall_at_k": [recall_at_k(data, k=k, k_percentage=k_percentage)],
        }
    )


def _unificar_df(
    x_data_frame: list[pd.DataFrame],
    y_data_frame: list[pd.Series],
    response: str | None = None,
) -> list[pd.DataFrame]:
    if not response:
        raise ValueError("Informe o nome da coluna response.")

    if len(x_data_frame) != len(y_data_frame):
        raise ValueError("x_data_frame e y_data_frame precisam ter o mesmo tamanho.")

    lista_response_df = []
    for x_df, y_df in zip(x_data_frame, y_data_frame):
        df_unificado = x_df.copy()
        df_unificado[response] = y_df.copy()
        lista_response_df.append(df_unificado)

    return lista_response_df


def aplicar_modificacoes(
    x_data_frame: list[pd.DataFrame],
    y_data_frame: list[pd.Series],
    response: str,
    cols_select: list[str] | None = None,
) -> list[pd.DataFrame]:
    lista_tratados = _unificar_df(x_data_frame, y_data_frame, response)
    lista_retorno = []

    for df in lista_tratados:
        df_tratado = dp.data_prep(fe.fe(df)).dropna().copy()

        if cols_select is not None:
            cols_model = [*cols_select, response]
            df_tratado = df_tratado[cols_model].copy()

        lista_retorno.append(df_tratado)

    return lista_retorno


def separar_df(
    lista_df: list[pd.DataFrame],
    response: str,
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    if len(lista_df) < 2:
        raise ValueError("lista_df precisa conter ao menos dois DataFrames: teste e validacao.")

    df_teste = lista_df[0].copy()
    df_validacao = lista_df[1].copy()

    x_teste = df_teste.drop(columns=[response]).copy()
    y_teste = df_teste[response].copy()

    x_validacao = df_validacao.drop(columns=[response]).copy()
    y_validacao = df_validacao[response].copy()

    return x_teste, y_teste, x_validacao, y_validacao


def cross_val(
    modelo: Any,
    kfold: int,
    x_dados: pd.DataFrame,
    y_dados: pd.Series,
    k: int | None = None,
    k_percentage: float | None = None,
) -> pd.DataFrame:
    precision_list = []
    recall_list = []

    skf = StratifiedKFold(n_splits=kfold, shuffle=True, random_state=42)

    for i, (train_idx, val_idx) in enumerate(skf.split(x_dados, y_dados), start=1):
        print(f"{i}/{kfold}")

        x_tr = x_dados.iloc[train_idx]
        y_tr = y_dados.iloc[train_idx]

        x_val = x_dados.iloc[val_idx]
        y_val = y_dados.iloc[val_idx]

        model = clone(modelo)
        model.fit(x_tr, y_tr)

        y_proba_kfold = model.predict_proba(x_val)

        data_fold = pd.DataFrame(
            {
                "resposta": y_val.values,
                "score": y_proba_kfold[:, 1],
            }
        )

        precision_list.append(precision_at_k(data_fold, k=k, k_percentage=k_percentage))
        recall_list.append(recall_at_k(data_fold, k=k, k_percentage=k_percentage))

    return pd.DataFrame(
        {
            "Model_Name": [modelo.__class__.__name__],
            "Precision@k Mean": [float(np.mean(precision_list))],
            "Precision@k STD": [float(np.std(precision_list))],
            "Recall@k Mean": [float(np.mean(recall_list))],
            "Recall@k STD": [float(np.std(recall_list))],
        }
    )


def tamanho_modelo(lista_modelos: list[Any]) -> pd.DataFrame:
    lista_temp = []

    for modelo in lista_modelos:
        tamanho_bytes = len(pickle.dumps(modelo))
        tamanho_kb = tamanho_bytes / 1024
        tamanho_mb = tamanho_kb / 1024

        lista_temp.append(
            {
                "model": modelo.__class__.__name__,
                "bytes": tamanho_bytes,
                "KB": tamanho_kb,
                "MB": tamanho_mb,
            }
        )

    return pd.DataFrame(lista_temp)

def tabela_lift(y_true, y_score, bins=20):
    df_lift = pd.DataFrame({
        "target": y_true,
        "score": y_score,
    }).sort_values("score", ascending=False).reset_index(drop=True)

    df_lift["faixa"] = pd.qcut(df_lift.index, bins, labels=False)
    taxa_global = df_lift["target"].mean()

    tabela = df_lift.groupby("faixa").agg(
        clientes=("target", "count"),
        interessados=("target", "sum"),
    )

    tabela["precision_faixa"] = tabela["interessados"] / tabela["clientes"]
    tabela["lift"] = tabela["precision_faixa"] / taxa_global
    tabela["clientes_acumulados"] = tabela["clientes"].cumsum()
    tabela["interessados_acumulados"] = tabela["interessados"].cumsum()
    tabela["recall_acumulado"] = tabela["interessados_acumulados"] / tabela["interessados"].sum()

    return tabela.reset_index()