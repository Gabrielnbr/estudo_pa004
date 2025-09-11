import pandas as pd
import numpy as np
import seaborn as sns

from scipy              import stats

from matplotlib import pyplot as plt
from IPython.core.display import HTML


def supressao_notacao():
    # Supressão de Notação Científica
    np.set_printoptions(suppress=True)
    pd.set_option('display.float_format', '{:.3f}'.format)

def jupyter_settings(
                    altura: int,
                    largura: int,
                    fonte: int):
    #%matplotlib inline

    plt.style.use( 'bmh' )
    plt.rcParams['figure.figsize'] = [altura, largura]
    plt.rcParams['font.size'] = fonte

    display( HTML( '<style>.container { width:100% !important; }</style>') )
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.set_option( 'display.expand_frame_repr', False )

## Function to reduce the DF size
## It is necessary that after using this code, carefully check the output results for each column.
def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 10242
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 10242
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df

def estatistica_descritiva(df: pd.DataFrame):
    # Medidas de tendência central - Mean, Median
    media = pd.DataFrame(df.apply(np.mean)).T
    mediana = pd.DataFrame(df.apply(np.median)).T

    # Medidas de Dispersão - Std, min, max, range, skew, kurtosis
    desvio_padrao = pd.DataFrame(df.apply(np.std)).T
    minimo = pd.DataFrame(df.apply(np.min)).T
    maximo = pd.DataFrame(df.apply(np.max)).T
    range_ = pd.DataFrame(df.apply(lambda x : x.max() - x.min())).T
    assimetria = pd.DataFrame(df.apply(lambda x : x.skew())).T
    curtosis = pd.DataFrame(df.apply(lambda x : x.kurtosis())).T

    #CV
    cv = pd.DataFrame(df.apply(lambda x : x.std() / x.mean())).T
    iqr = pd.DataFrame(df.apply(lambda x : x.quantile(0.75) - x.quantile(0.25))).T

    estatistica = pd.concat([minimo,
                             maximo,
                             range_,
                             media,
                             mediana,
                             desvio_padrao,
                             iqr,
                             assimetria,
                             curtosis,
                             cv]).T.reset_index()

    estatistica.columns = ['variaveis',
                           'minimo',
                           'maximo',
                           'range',
                           'media',
                           'mediana',
                           'desvio_padrao',
                           'iqr',
                           'assimetria',
                           'curtosis',
                           'cv']

    return estatistica

def visualizacao_dados_categoricos(df):
    for i in df:
        print(f'Atributo: {i}')
        print(f'Total de Valores Únicos: {len(df[i].sort_values().unique())}')
        print(f'Total de Valores não Nulos: {df[i].notnull().sum()}')
        print(f'Total de Valores Nulos: {df[i].isnull().sum()}')
        print(f'Porcentagem Valores Nulos (%) : {df[i].isnull().sum() / len(df[i]) * 100:.2f}%\n')
        print(f'Valores Descritos: {df[i].sort_values().unique().tolist()}\n')
        
        for valor in df[i].sort_values().unique():
            contagem = (df[i] == valor).sum()
            porcentagem = contagem/len(df[i])
            print(f'Contagem de {valor}: {contagem}; Porcentagem em relação ao total:{porcentagem*100:.2f}%')

        sns.countplot(data=df, x=i)
        plt.title(f'Contagem de valores para o atributo {i}')
        plt.show()

        print("----------------------------------------------------------------\n")


def cramer_v(x, y):
    
    cm = pd.crosstab( x, y ).values
    n = cm.sum()
    r, k = cm.shape
    
    chi2 = stats.chi2_contingency(cm)[0]
    chi2corr = max(0, chi2 - (k-1) * (r-1) / (n-1) )
    
    kcorr = k - (k-1)**2/(n-1)
    rcorr = r - (r-1)**2/(n-1)
    
    return np.sqrt( ( chi2corr/n ) / ( min( kcorr-1,rcorr-1 ) ) )