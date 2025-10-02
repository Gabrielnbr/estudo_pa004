import pickle
import pandas as pd

def normalizacao(df):
    
    ss = pickle.load( open('../src/features/premio_anual_normalize.pkl','rb') )
    
    if "premio_anual" in df.columns:
        df['premio_anual'] = ss.fit_transform( df[['premio_anual']].values)
    
    return df

def reescala(df):
    
    mms_idade = pickle.load( open('../src/features/mms_idade.pkl', 'rb'))
    mms_cdc = pickle.load( open('../src/features/mms_cdc.pkl', 'rb'))
    
    if 'idade' in df.columns:
        df[['idade']] = mms_idade.fit_transform( df[['idade']].values )
    
    if 'cliente_dias_contrato' in df.columns:
        df[['cliente_dias_contrato']] = mms_cdc.fit_transform( df[['cliente_dias_contrato']].values )
    
    return df

def encoder(df):
    
    target_encode_genero = pickle.load( open ('../src/features/target_encode_genero.pkl', 'rb' ) )
    target_encode_codigo_regiao = pickle.load( open ('../src/features/target_encode_codigo_regiao.pkl', 'rb' ) )
    fe_contato_cliente = pickle.load( open ('../src/features/fe_contato_cliente.pkl', 'rb' ) )
    
    if 'genero' in df.columns:
        # genero - OneHotEncoder / TargetEncoder
        target_encode_genero = df.groupby(['genero'])['resposta'].mean()
        df.loc[:, 'genero'] = df['genero'].map(target_encode_genero)
    
    if 'codigo_regiao' in df.columns:
        # codigo_regiao -  One Hot Encoding / Frequency Encoding / Target Encoding / Weighted Target Encoding
        target_encode_codigo_regiao = df.groupby(['codigo_regiao'])['resposta'].mean()
        df.loc[:, 'codigo_regiao'] = df['codigo_regiao'].map(target_encode_codigo_regiao)
    
    if 'idade_veiculo' in df.columns:
        # idade_veiculo - One Hot Encoding / Order Encoding / Frequency Encoding
        df = pd.get_dummies(df, prefix=['idade_veiculo'], columns=['idade_veiculo'])
    
    if 'contato_cliente' in df.columns:
        # contato_cliente - Target Encoding / Frequency Encoding
        fe_contato_cliente = df.groupby(['contato_cliente']).size() / len(df)
        df.loc[:, 'contato_cliente'] = df['contato_cliente'].map(fe_contato_cliente)
    
    return df

def data_prep(df):
    df = normalizacao(df)
    df = reescala(df)
    df = encoder(df)
    
    return df