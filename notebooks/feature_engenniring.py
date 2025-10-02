import pandas as pd


def fe(df):
    if "idade_veiculo" in df.columns:
        df['idade_veiculo'] = df['idade_veiculo'].apply(lambda x: 1 if x == '< 1 Year' else
                                                          2 if x == '1-2 Year' else 3)
    
    if "veiculo_danificado" in df.columns:
        df['veiculo_danificado'] = df['veiculo_danificado'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    return df