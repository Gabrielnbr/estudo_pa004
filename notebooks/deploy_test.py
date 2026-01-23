import pickle
import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s [%(name)s]: %(message)s"
)

class HealthInsurance:
    def __init__(self):
        
        self.home_path =                   "E:/3_recursos/2_area/profissional/cursos/22_06.1 - PA004/src/features/"
        self.premio_anual_mms =            self.home_path+"mms_pa.pkl"
        self.idade =                       self.home_path+"mms_idade.pkl"
        self.clientes_dia_contrato_mms =   self.home_path+"mms_cdc.pkl"
        self.semanas_contrato_mms =        self.home_path+"mms_sc.pkl"
        self.meses_contrato_mms =          self.home_path+"mms_mc.pkl"
        self.genero_te =                   self.home_path+"target_encode_genero.pkl"
        self.codigo_regisao_te =           self.home_path+"target_encode_codigo_regiao.pkl"
        self.contato_cliente_fe =          self.home_path+"fe_contato_cliente.pkl"
        
    def data_cleaning(self,  df: pd.DataFrame ) -> pd.DataFrame:
        try:
            new_columns = ['id', 'genero', 'idade', 'codigo_regiao', 'contato_cliente', 'cnh', 'idade_veiculo',
                       'veiculo_danificado', 'seguro_previo_automovel', 'premio_anual', 'cliente_dias_contrato']
            df.columns = new_columns
        except Exception as e:
            return logging.exception(f"Não foi possível renomear as colunas {e}")
        return df
    
    #====================
    # FEATURE ENGINNIRING
    #====================
    
    def _fe_idade_veiculo(self, df):
        """Codifica idade_veiculo em faixas discretas"""
        df['idade_veiculo'] = df['idade_veiculo'].apply(
            lambda x: 1 if x == '< 1 Year' else
                    2 if x == '1-2 Year' else
                    3
        )
        return df

    def _fe_veiculo_danificado(self, df):
        """Transforma variável binária de texto ('Yes'/'No') em 1/0"""
        df['veiculo_danificado'] = df['veiculo_danificado'].apply(
            lambda x: 1 if x == 'Yes' else 0
        )
        return df
    
    def _fe_idade_class_etaria(self, df):
        """Cria faixa etária com base em idade"""
        df['idade_class_etaria'] = df['idade'].apply(
            lambda x: 1 if x <= 35 else
                    2 if (x > 35) and (x <= 65) else
                    3
        )
        return df
    
    def _fe_premio_anual(self, df):
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

    def _fe_semanas_contrato(self, df):
        df['semanas_contrato'] = df['cliente_dias_contrato']/7
        return df

    def _fe_meses_contrato(self, df):
        df['meses_contrato'] = df['cliente_dias_contrato']/30
        return df

    def _fe_contrato(self, df):
        df = self._fe_semanas_contrato(df)
        df = self._fe_meses_contrato(df)
        return df

    def fe(self, df):
    
        dictfe = {
            'idade_veiculo': self._fe_idade_veiculo,
            'veiculo_danificado': self._fe_veiculo_danificado,
            'idade': self._fe_idade_class_etaria,
            'premio_anual': self._fe_premio_anual,
            'cliente_dias_contrato': self._fe_contrato,
        }
    
        for col, fn in dictfe.items():
            if col in df.columns:
                df = fn(df)
            else:
                print(f"[Aviso] Coluna {col} ausente, pulando.")
        return df
    
    #=====================
    # NORMALIZAÇÃO
    #=====================
    
    def _norm_premio_anual(self, df):
        df[['premio_anual']] = np.log1p(df[['premio_anual']])
        return df

    def _normalizacao(self, df):
        
        DICTNORMALIZE = {
        'premio_anual': self._norm_premio_anual
        }
        
        for col, fn in DICTNORMALIZE.items():
            if col in df.columns:
                df = fn(df)
            else:
                print(f"[Aviso] Coluna {col} ausente, pulando.")
        return df

    #============================
    # REESCALA
    #============================

    def _reescala_premio_anual(self, df):
        mms_pa = pickle.load(open(self.premio_anual_mms,'rb'))
        df[['premio_anual']] = mms_pa.transform( df[['premio_anual']].values )
        return df

    def _reescala_idade(self, df):
        mms_idade = pickle.load(open(self.idade, 'rb'))
        df[['idade']] = mms_idade.transform(df[['idade']].values)
        return df

    def _reescala_cdc(self, df):
        mms_cdc = pickle.load(open(self.clientes_dia_contrato_mms, 'rb'))
        df[['cliente_dias_contrato']] = mms_cdc.transform(df[['cliente_dias_contrato']].values)
        return df

    def _reescala_semana_contrato(self, df):
        mms_sc = pickle.load(open(self.semanas_contrato_mms,'rb' ) )
        df[['semanas_contrato']] = mms_sc.transform( df[['semanas_contrato']].values )
        return df

    def _reescala_meses_contrato(self, df):
        mms_mc = pickle.load(open(self.meses_contrato_mms,'rb' ) )
        df[['meses_contrato']] = mms_mc.transform( df[['meses_contrato']].values )
        return df

    def _reescala(self, df):
        
        DICTRESCALE = {
        'premio_anual': self._reescala_premio_anual,
        'idade': self._reescala_idade,
        'cliente_dias_contrato': self._reescala_cdc,
        'semanas_contrato': self._reescala_semana_contrato,
        'meses_contrato': self._reescala_meses_contrato
        }
        
        for col, fn in DICTRESCALE.items():
            if col in df.columns:
                df = fn(df)
            else:
                print(f"[Aviso] Coluna {col} ausente, pulando.")
        return df

    #============================
    # ENCONDER
    #============================

    def _enc_genero(self, df):
        target_encode_genero = pickle.load( open (self.genero_te, 'rb' ) )
        df.loc[:, 'genero'] = df['genero'].map(target_encode_genero)
        return df

    def _enc_codigo_regiao(self, df):
        target_encode_codigo_regiao = pickle.load( open (self.codigo_regisao_te, 'rb' ) )
        df.loc[:, 'codigo_regiao'] = df['codigo_regiao'].map(target_encode_codigo_regiao)
        return df

    def _enc_idade_veiculo(self, df):
        df = pd.get_dummies(df, prefix=['idade_veiculo'], columns=['idade_veiculo'])
        return df

    def _enc_contato_cliente(self, df):
        fe_contato_cliente = pickle.load( open (self.contato_cliente_fe, 'rb' ) )
        df.loc[:, 'contato_cliente'] = df['contato_cliente'].map(fe_contato_cliente)
        return df

    def _encoder(self, df):
        
        DICTENCODER = {
        'genero': self._enc_genero,
        'codigo_regiao': self._enc_codigo_regiao,
        'idade_veiculo': self._enc_idade_veiculo,
        'contato_cliente': self._enc_contato_cliente
        }
        
        for col, fn in DICTENCODER.items():
            if col in df.columns:
                df = fn(df)
            else:
                print(f"[Aviso] Coluna {col} ausente, pulando.")
        return df

    #============================
    # DATA_PREPARATION
    #============================

    def data_prep(self, df):
        df = self._normalizacao(df)
        df = self._reescala(df)
        df = self._encoder(df)
        
        cols_selected = ['premio_anual',
                    'idade',
                    'cliente_dias_contrato',
                    'semanas_contrato',
                    'meses_contrato',
                    'codigo_regiao',
                    'veiculo_danificado',
                    'contato_cliente',
                    'seguro_previo_automovel']
        
        df = df[cols_selected]
        
        return df
    
    def get_prediction(self, model, original_data, test_data):
        pred = model.predict_proba(test_data)[:,1]
        
        original_data['prediction'] = pred
        data_return = original_data[['id','prediction']]
        
        return data_return.to_json( orient = "records", date_format="iso")