import pickle

import numpy                as np
import pandas               as pd
import seaborn              as sns
import matplotlib.patches   as mpatches

from matplotlib import pyplot as plt


from scipy                  import stats
from IPython.display        import Image
from IPython.core.display   import HTML

# Supressão de Notação Científica
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', '{:.4f}'.format)

# Corrigir Gráficos Jupter

'''def jupyter_settings():
    plt.style.use( 'bmh' )
    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams['font.size'] = 12

    display( HTML( '<style>.container { width:100% !important; }</style>') )
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.set_option( 'display.expand_frame_repr', False )

jupyter_settings()
'''
df3 = pickle.load( open( "data/interim/df2_feature.pkl", "rb" ) )
def printi():
    print(df3.head())

def grafico_a():
    plt.subplot(2,2,1)
    sns.boxplot(x='resposta', y='idade', data=df3)

    aux1 = df3.loc[df3['resposta'] == 0, 'idade']
    plt.subplot(2,2,3)
    sns.histplot(x=aux1)

    aux2 = df3.loc[df3['resposta'] == 1, 'idade']
    plt.subplot(2,2,4)
    sns.histplot(x=aux2)
    plt.show()

def grafico_b():
    plt.subplot(3,2,1)
    sns.boxplot(x='resposta', y='premio_anual', data=df3)

    aux1 = df3[df3['premio_anual'] < 80000]
    plt.subplot(3,2,2)
    sns.boxplot(x='resposta', y='premio_anual', data=aux1)

    aux2 = df3.loc[df3['resposta'] == 0, 'premio_anual']
    plt.subplot(3,2,3)
    sns.histplot(x=aux2)

    aux3 = df3.loc[df3['resposta'] == 1, 'premio_anual']
    plt.subplot(3,2,4)
    sns.histplot(x=aux3)

    # Filto pelo valor do premio_anual #
    aux4 = df3[(df3['premio_anual'] > 10000) & (df3['premio_anual'] < 80000)]

    aux5 = aux4.loc[aux4['resposta'] == 0, 'premio_anual']
    plt.subplot(3,2,5)
    sns.histplot(x=aux5)

    aux6 = aux4.loc[aux4['resposta'] == 1, 'premio_anual']
    plt.subplot(3,2,6)
    sns.histplot(x=aux6)
    plt.show()

def grafico_c():

    aux1 = df3[['cnh', 'resposta']].groupby(['resposta']).sum().reset_index()
    plt.subplot(1,2,1)
    sns.barplot(x='resposta', y='cnh', data=aux1, ci= True)

    aux1['cnh_percent'] = aux1['cnh'] / aux1['cnh'].sum()
    plt.subplot(1,2,2)
    sns.barplot(x='resposta', y='cnh_percent', data=aux1, ci= True)
    plt.show()

printi()
#grafico_a()
#grafico_b()
grafico_c()