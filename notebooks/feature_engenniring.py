import pandas as pd

def _fe_idade_veiculo(df):
    """Codifica idade_veiculo em faixas discretas"""
    df['idade_veiculo'] = df['idade_veiculo'].apply(
        lambda x: 1 if x == '< 1 Year' else
                  2 if x == '1-2 Year' else
                  3
    )
    return df


def _fe_veiculo_danificado(df):
    """Transforma variável binária de texto ('Yes'/'No') em 1/0"""
    df['veiculo_danificado'] = df['veiculo_danificado'].apply(
        lambda x: 1 if x == 'Yes' else 0
    )
    return df


def _fe_idade_class_etaria(df):
    """Cria faixa etária com base em idade"""
    df['idade_class_etaria'] = df['idade'].apply(
        lambda x: 1 if x <= 35 else
                  2 if (x > 35) and (x <= 65) else
                  3
    )
    return df


def _fe_premio_anual(df):
    """Cria categoria de prêmio anual com base em faixas de valores"""
    bins = [0, 25000, 50000, 75000, 100000, float('inf')]
    labels = [1, 2, 3, 4, 5]
    df['premio_anual_cat'] = pd.cut(
        x=df['premio_anual'],
        bins=bins,
        labels=labels,
        right=False
    ).astype('int64')
    return df

def _fe_semanas_contrato(df):
    df['semanas_contrato'] = df['cliente_dias_contrato']/7
    return df

def _fe_meses_contrato(df):
    df['meses_contrato'] = df['cliente_dias_contrato']/30
    return df

def _fe_contrato(df):
    df = _fe_semanas_contrato(df)
    df = _fe_meses_contrato(df)
    return df

DICTFE = {
    'idade_veiculo': _fe_idade_veiculo,
    'veiculo_danificado': _fe_veiculo_danificado,
    'idade': _fe_idade_class_etaria,
    'premio_anual': _fe_premio_anual,
    'cliente_dias_contrato': _fe_contrato,
}

def fe(df):
    for col, fn in DICTFE.items():
        if col in df.columns:
            df = fn(df)
        else:
            print(f"[Aviso] Coluna {col} ausente, pulando.")
    return df