import pickle
import pandas as pd
import numpy as np

#============================
# NORMALIZAÇÃO
#============================

def _norm_premio_anual(df):
    df[['premio_anual']] = np.log1p(df[['premio_anual']])
    return df

DICTNORMALIZE = {
    'premio_anual': _norm_premio_anual
}

def _normalizacao(df):
    for col, fn in DICTNORMALIZE.items():
        if col in df.columns:
            df = fn(df)
        else:
            print(f"[Aviso] Coluna {col} ausente, pulando.")
    return df

#============================
# REESCALA
#============================

def _reescala_premio_anual(df):
    mms_pa = pickle.load(open('../src/features/mms_pa.pkl','rb'))
    df[['premio_anual']] = mms_pa.transform( df[['premio_anual']].values )
    return df

def _reescala_idade(df):
    mms_idade = pickle.load(open('../src/features/mms_idade.pkl', 'rb'))
    df[['idade']] = mms_idade.transform(df[['idade']].values)
    return df

def _reescala_cdc(df):
    mms_cdc = pickle.load(open('../src/features/mms_cdc.pkl', 'rb'))
    df[['cliente_dias_contrato']] = mms_cdc.transform(df[['cliente_dias_contrato']].values)
    return df

def _reescala_semana_contrato(df):
    mms_sc = pickle.load(open('../src/features/mms_sc.pkl','rb' ) )
    df[['semanas_contrato']] = mms_sc.transform( df[['semanas_contrato']].values )
    return df

def _reescala_meses_contrato(df):
    mms_mc = pickle.load(open('../src/features/mms_mc.pkl','rb' ) )
    df[['meses_contrato']] = mms_mc.transform( df[['meses_contrato']].values )
    return df

DICTRESCALE = {
    'premio_anual': _reescala_premio_anual,
    'idade': _reescala_idade,
    'cliente_dias_contrato': _reescala_cdc,
    'semanas_contrato': _reescala_semana_contrato,
    'meses_contrato': _reescala_meses_contrato
}

def _reescala(df):
    for col, fn in DICTRESCALE.items():
        if col in df.columns:
            df = fn(df)
        else:
            print(f"[Aviso] Coluna {col} ausente, pulando.")
    return df

#============================
# ENCONDER
#============================

def _enc_genero(df):
    target_encode_genero = pickle.load( open ('../src/features/target_encode_genero.pkl', 'rb' ) )
    df.loc[:, 'genero'] = df['genero'].map(target_encode_genero)
    return df

def _enc_codigo_regiao(df):
    target_encode_codigo_regiao = pickle.load( open ('../src/features/target_encode_codigo_regiao.pkl', 'rb' ) )
    df.loc[:, 'codigo_regiao'] = df['codigo_regiao'].map(target_encode_codigo_regiao)
    return df

def _enc_idade_veiculo(df):
    df = pd.get_dummies(df, prefix=['idade_veiculo'], columns=['idade_veiculo'])
    return df

def _enc_contato_cliente(df):
    fe_contato_cliente = pickle.load( open ('../src/features/fe_contato_cliente.pkl', 'rb' ) )
    df.loc[:, 'contato_cliente'] = df['contato_cliente'].map(fe_contato_cliente)
    return df

DICTENCODER = {
    'genero': _enc_genero,
    'codigo_regiao': _enc_codigo_regiao,
    'idade_veiculo': _enc_idade_veiculo,
    'contato_cliente': _enc_contato_cliente
}

def _encoder(df):
    for col, fn in DICTENCODER.items():
        if col in df.columns:
            df = fn(df)
        else:
            print(f"[Aviso] Coluna {col} ausente, pulando.")
    return df

#============================
# DATA_PREPARATION
#============================

def data_prep(df):
    df = _normalizacao(df)
    df = _reescala(df)
    df = _encoder(df)
    return df