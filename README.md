# 0.0 Orientações

Este é um projeto de Machine Learning Supervisionado de Classificação, especificamente Learn-to-Rank. Seu objetivo é ordenar um conjunto de clientes com tendência a consumir um tipo de serviço, a fim de maximizar o tempo e os recursos para vender a mais clientes.

O projeto utiliza dados de seguro de saúde para auxiliar na venda de seguros automotivos. Em vez de classificar o interesse, o modelo ordena os clientes por probabilidade de conversão permitindo que o time de vendas se concentre em contatos mais promissores.

Links para este projeto:
- API: O modelo está disponível na nuvem do Render por meio do `https://estudo-pa004.onrender.com/predict`
- Base e Dados: A base de dados não se encontra mais disponível online, deixei na pasta dados/data e dados/raw
- Aplicação WEB: Este projeto encontra-se no google sheets [[LINK]](https://docs.google.com/spreadsheets/d/1fT8jgWiZAWIL3uFHkqCe5A0ioZvgG4f__XKRMrQOQNU/edit?gid=909962563#gid=909962563) e no Looker Stúdio [[LINK]](https://datastudio.google.com/reporting/bf08327e-d1da-4d19-a61c-192d631e738f)

# 1.0 Problema de Negócio

A Insurrance ALL é uma empresa do mercado de saúde que fornece seguros de saúde. Com o crescimento da empresa, ela está estudando ampliar ao mercado de seguros automotivos.

A fim de avaliar o potencial do seu produto, a empresa realizou uma pesquisa com aproximadamente 380 mil clientes, mas 127 mil não responderam.

Desta forma o time de negócio pensou em fazer uma campanha ativa para entrar em contato com os clientes, mas essa campanha está limitada a 20.000 ligações.

O problema que temos que resolver é classificar os clientes em ordem de maior probabilidade de interesse em adquirir seguro automotivo, permitindo maior chance de conversão dos 20.000 clientes.

# 2.0 Premissas de Negócio

Para este projeto foram considerada as seguintes premissas:

1. O time de venda possui capacidade operacional limitada a 20.000 ligações.
2. O custo de cada ligação é 2,50.
3. A operação realiza 2.000 ligações por dia.
4. A receita média estimada por cliente convertido foi estimada em R$ 2.000,00.

## 2.1 Perguntas de Negócio

Para complementar o estudo, o time de negócio fez 3 perguntas a serem respondidas:

1. Quais são os principais insights sobre os atributos mais relevantes de clientes interessados em adquirir seguro automotivo?
2. Qual porcentagem de clientes interessados o time de vendas conseguirá contatar fazendo 20.000 ligações?
3. Se a capacidade aumentar para 40.000 ligações, qual porcentagem de clientes interessados o time de vendas conseguirá contatar?
4. Quantas ligações são necessárias para contatar 80% dos clientes interessados?

## 2.2 Descrição dos Dados

A tabela está disponível da seguinte forma:

| Coluna | Tradução | Descrição |
| ------ | -------- | --------- |
| Id | Id | Identificador único do cliente. |
| Gender | genero | Gênero do cliente. |
| Age | idade | idade do cliente. |
| Driving License | cnh | 0, o cliente não tem permissão para dirigir e 1, o cliente tem para dirigir ( CNH – Carteira Nacional de Habilitação )
| Region Code | codigo_regiao | Código da região do cliente. |
| Previously Insured | seguro_previo_automovel | 0, o cliente não tem seguro de automóvel e 1, o cliente já tem seguro de automóvel. |
| Vehicle Age | idade_veiculo | Idade do veículo. |
| Vehicle Damage | veiculo_danificado | 0, cliente nunca teve seu veículo danificado no passado e 1, cliente já teve seu veículo danificado no passado. |
| Anual Premium | premio_anual | Quantidade que o cliente pagou à empresa pelo seguro de saúde anual. |
| Policy sales channel | contato_cliente | Código anônimo para o canal de contato com o cliente. |
| Vintage | cliente_dias_contrato | Número de dias que o cliente se associou à empresa através da compra do seguro de saúde. |
| Response | resposta | 0, o cliente não tem interesse e 1, o cliente tem interesse. |

## 2.3 Acesso aos Dados

Os dados não estão mais disponíveis para consulta, mas foram extraídos de um banco PostgreSQL disponibilizado na AWS.

# 3.0 Estratégia da Solução

Para o desenvolvimento da solução foi adotada a metodologia CRISP-DM, permitindo iterar sobre vários ciclos a fim de alcançar um melhor entendimento do problema, buscar otimizar o modelo e seus resultados.

## 3.1 Metodologia

1. Entendimento do negócio: definição do problema, limitação operacional do time comercial e perguntas complementares.
2. Coleta de dados: conexão com o banco PostgreSQL e união das tabelas necessárias.
3. Limpeza dos dados: renomeação de colunas, ajuste de tipos e verificação de dados nulos.
4. Feature engineering: criação de atributos derivados para representar faixa etária, categorias de prêmio anual e tempo de contrato em semanas e meses.
5. Análise exploratória: investigação da distribuição dos atributos e relação com a variável resposta.
6. Preparação dos dados: normalização, reescala e encoding das variáveis.
7. Seleção de atributos: uso de ExtraTreesClassifier para identificar as variáveis mais relevantes.
8. Treinamento dos modelos: comparação entre modelos de classificação e rankeamento por probabilidade.
9. Avaliação de performance: uso de Precision@k, Recall@k, lift e tradução das métricas para impacto de negócio.
10. Publicação da solução: criação de uma API Flask para receber clientes e retornar a probabilidade de interesse.

## 3.2 Produto Final

O produto final à Área de Ciência de Dados é uma API que recebe os dados em JSON e retorna uma coluna `prediction` com a probabilidade de interesse no seguro automotivo.

O produto final à Área do Comercial é um Google Sheets com integração a essa API que o usuário pode, através de um botão, fazer a predição de um conjunto de clientes.

O produto final à Área de Negócio é um Looker Studio informando como está o andamento da campanha com métricas da Campanha e Financeira.

## 3.3 Ferramentas Utilizadas

Para construir a solução à Área de Ciência de Dados foram utilizadas as seguintes ferramentas:

- Python
- Pandas e NumPy
- Scikit-learn
- XGBoost
- Flask
- Requests
- PostgreSQL
- Jupyter Notebook no VSCode
- Git e GitHub
- Render para hospedagem da API

Para construir a solução à Área do Comercial foram utilizadas as seguintes ferramentas:

- Google Sheets
- App Scripts

Para construir a solução à Área de Negócio foram utilizadas as seguintes ferramentas:

- Looker Studio

# 4.0 Análise dos Dados

A base completa possui 381.109 linhas e 12 atributos após a união e limpeza inicial. Não foram encontrados valores nulos nas colunas utilizadas.

A taxa média de clientes interessados é baixa, aproximadamente 12,3% na base geral e 12,49% na base de validação. Isso confirma que uma abordagem aleatória desperdiçaria muitos contatos, pois a maioria dos clientes não tem interesse no produto.

Algumas características relevantes identificadas na análise:

1. A maior parte dos clientes possui CNH.
2. A base possui proporção semelhante entre clientes com e sem histórico de veículo danificado.
3. A idade média dos clientes está próxima de 39 anos.
4. O prêmio anual apresenta alta dispersão e presença de valores extremos.
5. A variável `seguro_previo_automovel` é relevante para identificar clientes com menor propensão de compra, pois clientes que já possuem seguro automotivo tendem a ter menor necessidade do novo produto.

## 4.1 Insights de Negócio

Foram levantadas hipóteses sobre perfil do cliente, veículo e seguro. As principais dimensões investigadas foram:

| Dimensão | Hipótese analisada | Uso na solução |
| -- | -- | -- |
| Cliente | Clientes entre 35 e 65 anos poderiam responder mais "sim" na pesquisa. | A idade foi usada no modelo e também transformada em faixa etária. |
| Cliente | Clientes de determinadas regiões poderiam ter comportamento diferente. | O código da região foi mantido e codificado por target encoding. |
| Veículo | Clientes com veículo danificado poderiam ter maior interesse em seguro automotivo. | A variável `veiculo_danificado` foi selecionada entre os atributos finais. |
| Veículo | A idade do veículo poderia influenciar a propensão de compra. | A variável foi tratada e usada nas etapas intermediárias de modelagem. |
| Seguro | Clientes sem seguro automotivo prévio poderiam apresentar maior propensão. | A variável `seguro_previo_automovel` foi mantida no modelo final. |
| Contrato | O tempo de relacionamento com a empresa poderia influenciar a resposta. | Foram criadas as features `semanas_contrato` e `meses_contrato`. |

# 5.0 Modelos de Machine Learning Utilizados

Foram testados modelos de classificação com foco em ordenação por probabilidade. Os algoritmos avaliados foram:

1. DummyClassifier, usado como baseline.
2. KNeighborsClassifier.
3. RandomForestClassifier.
4. LogisticRegression.
5. XGBClassifier.

Como o problema de negócio é priorizar clientes para contato, os modelos foram avaliados principalmente por Precision@k e Recall@k.

# 6.0 Seleção do Modelo de Machine Learning

## 6.1 Seleção de Atributos

A seleção de atributos foi realizada com ExtraTreesClassifier. As variáveis mais importantes identificadas foram:

| Ordem | Atributo | Importância |
| -- | -- | -- |
| 1 | premio_anual | 0,18 |
| 2 | idade | 0,16 |
| 3 | cliente_dias_contrato | 0,11 |
| 4 | semanas_contrato | 0,11 |
| 5 | meses_contrato | 0,11 |
| 6 | codigo_regiao | 0,11 |
| 7 | veiculo_danificado | 0,07 |
| 8 | contato_cliente | 0,07 |
| 9 | seguro_previo_automovel | 0,05 |

As features finais utilizadas no modelo foram:

- `premio_anual`
- `idade`
- `cliente_dias_contrato`
- `semanas_contrato`
- `meses_contrato`
- `codigo_regiao`
- `veiculo_danificado`
- `contato_cliente`
- `seguro_previo_automovel`

## 6.2 Métricas dos Algoritmos

Na primeira avaliação com validação cruzada, os modelos apresentaram os seguintes resultados:

| Modelo | Precision@k Mean | Precision@k STD | Recall@k Mean | Recall@k STD |
| -- | -- | -- | -- | -- |
| DummyClassifier | 0,12101 | 0,00111 | 0,44600 | 0,00409 |
| KNeighborsClassifier | 0,25056 | 0,00122 | 0,92349 | 0,00454 |
| RandomForestClassifier | 0,25680 | 0,00103 | 0,94649 | 0,00384 |
| LogisticRegression | 0,25717 | 0,00060 | 0,94743 | 0,00220 |
| XGBClassifier | 0,26157 | 0,00109 | 0,96408 | 0,00406 |

Após essa etapa, os modelos KNN e DummyClassifier foram retirados das próximas análises. O KNN apresentou bom desempenho, mas tinha maior custo de memória e menor adequação para produção. O DummyClassifier foi mantido apenas como referência de baseline.

## 6.3 Fine Tuning

Foram realizados testes de fine tuning com Random Search para XGBClassifier, LogisticRegression e RandomForestClassifier.

Os melhores resultados de Recall@k encontrados foram:

| Modelo | Recall@k Mean |
| -- | -- |
| XGBClassifier | 0,966382 |
| XGBClassifier | 0,966014 |
| XGBClassifier | 0,965952 |
| RandomForestClassifier | 0,964571 |
| RandomForestClassifier | 0,963466 |
| RandomForestClassifier | 0,962974 |
| LogisticRegression | 0,951492 |
| LogisticRegression | 0,950326 |
| LogisticRegression | 0,950264 |

## 6.4 Modelo Final

O modelo final escolhido foi o XGBClassifier.

Os critérios de escolha foram:

1. Melhor desempenho na métrica principal Recall@k.
2. Boa performance nos primeiros decis da curva lift.
3. Menor tamanho em memória em comparação com o RandomForestClassifier após o fine tuning.
4. Boa adequação para deploy em API.

Parâmetros selecionados para o XGBClassifier:

| Parâmetro | Valor |
| -- | -- |
| n_estimators | 200 |
| learning_rate | 0,01 |
| max_depth | 10 |
| min_child_weight | 5 |
| subsample | 0,8 |
| colsample_bytree | 0,6 |
| scale_pos_weight | 3 |

# 7.0 Resultado de Negócio 

## 7.1 Performance do Modelo Final

Na validação holdout, o XGBClassifier apresentou:

| Modelo | Precision@k | Recall@k |
| -- | -- | -- |
| XGBClassifier | 0,267999 | 0,965411 |

Na validação cruzada, o modelo apresentou:

| Modelo | Precision@k Mean | Precision@k STD | Recall@k Mean | Recall@k STD |
| -- | -- | -- | -- | -- |
| XGBClassifier | 0,26250 | 0,000374 | 0,96707 | 0,001367 |

Em comparação aos outros modelos, foi o resultado mais adequado ao problema.

## 7.2 Curva Lift

No Top 40% da base, o XGBClassifier apresentou lift de 1,44. Isso significa que, ao priorizar os clientes pelo modelo, a campanha encontra interessados em uma concentração aproximadamente 1,44 vezes maior do que uma abordagem aleatória.

| Modelo | Top % | Lift | Precision | Recall |
| -- | -- | -- | -- | -- |
| XGBClassifier | 40% | 1.432 | 0,398705 | 0,319143 |
| RandomForestClassifier | 40% | 1.429 | 0,391882 | 0,313682 |

No primeiro decil da validação, o XGBClassifier concentrou 2.280 clientes interessados em 5.717 contatos, com precision de 39,88%.

![LINK CURVA LIFT](reports\figures\xbg_lift_curve.png)

## 7.3 Threshold Operacional

Antes da tradução financeira, foi avaliado o uso de threshold para transformar probabilidades em decisão operacional.

O threshold de 0,45 foi selecionado como ponto de equilíbrio entre precision e recall. Nesse corte, o modelo preserva 74,5% dos positivos reais e exige aproximadamente 3 contatos para encontrar 1 cliente interessado.

| Métrica | Valor |
| -- | -- |
| Threshold | 0,45 |
| Total previsto para contato | 15.878 |
| Precision | 0,335 |
| Recall | 0,745 |
| F1-score | 0,462 |
| Verdadeiros positivos | 5.320 |
| Falsos positivos | 10.558 |
| Falsos negativos | 1.821 |
| Verdadeiros negativos | 39.465 |

Para uso direto da campanha, a recomendação principal continua sendo ordenação por score e seleção de Top k conforme capacidade operacional.

![LINK THRESHOLD](reports\figures\thrashold.png)

## 7.3 Resultado para 20.000 Ligações

Com 20.000 ligações, o modelo prioriza aproximadamente 34,99% da base de validação e captura 6.168 clientes interessados.

| Métrica | Resultado |
| -- | -- |
| Clientes contatados | 20.000 |
| Percentual da base contatada | 34,99% |
| Interessados capturados no Top 20k | 6.168 |
| Percentual dos interessados reais capturados | 86,37% |
| Taxa de interesse no Top 20k | 30,84% |
| Contatos por interessado | 3,24 |

Até o volume de 20.000 contatos, o modelo ainda apresenta lift de aproximadamente 1,6 vezes em relação à escolha aleatória.

![LINK RESULTADO 20K](reports\figures\resultado_20k.png)

## 7.4 Tradução Financeira

Considerando as premissas de R$ 2,50 por ligação, 2.000 ligações por dia e R$ 2.000,00 de receita estimada por cliente convertido, a campanha de 20.000 contatos apresenta o seguinte resultado:

| Métrica | Com modelo | Sem modelo |
| -- | -- | -- |
| Contatos realizados | 20.000 | 20.000 |
| Dias de operação | 10,00 | 10,00 |
| Custo total das ligações | R$ 50.000,00 | R$ 50.000,00 |
| Contatos por interessado | 3,24 | 8,01 |
| Custo por interessado | R$ 8,11 | R$ 20,01 |
| Interessados alcançados | 6.168 | 2.498 |
| Taxa de interesse | 30,84% | 12,49% |
| Receita estimada | R$ 12.336.000,00 | R$ 4.996.851,17 |
| Receita líquida após ligações | R$ 12.286.000,00 | R$ 4.946.851,17 |
| Receita por contato | R$ 616,80 | R$ 249,84 |
| Receita incremental | R$ 7.339.148,83 | R$ 0,00 |
| Multiplicador de receita | 2,47x | 1,00x |

Para obter os mesmos 6.168 interessados de forma aleatória, seriam necessárias aproximadamente 49.375 ligações. Portanto, o uso do modelo economiza cerca de 29.375 ligações, R$ 73.437,74 em custo operacional e 14,69 dias de operação.

## 7.5 Cenários Operacionais

A principal pergunta do negócio era entender o resultado com 20.000 ligações. Além disso, foram avaliados cenários complementares para 40.000 ligações e para captura de 80% dos clientes interessados.

| Cenário | Ligações | % da base de validação | Interessados capturados | % dos interessados reais | Precision |
| -- | -- | -- | -- | -- | -- |
| Campanha principal | 20.000 | 34,99% | 6.168 | 86,37% | 30,84% |
| Capacidade ampliada | 40.000 | 69,97% | 7.136 | 99,93% | 17,84% |
| Meta de 80% dos interessados | 17.727 | 31,01% | 5.713 | 80,00% | 32,23% |

Com isso, a recomendação operacional é utilizar o ranking do modelo até o limite de capacidade da campanha. Para capturar 80% dos interessados, o time precisaria realizar aproximadamente 17.727 ligações. Caso a capacidade suba para 40.000 ligações, o modelo praticamente esgota os interessados identificáveis na base de validação, mas com menor eficiência marginal nos contatos adicionais.

# 8.0 Aplicação em Produção

A solução foi publicada como uma API Flask. O endpoint `/predict` recebe um JSON com um ou mais clientes, executa o pipeline de limpeza, feature engineering e preparação dos dados, e retorna a probabilidade de interesse na coluna `prediction`.

Endpoint disponível:

```text
https://estudo-pa004.onrender.com/predict
```

O projeto entregou uma solução de priorização comercial para cross-sell de seguro automotivo. A abordagem por score resolve melhor o problema de negócio do que uma classificação simples, pois permite ordenar os clientes e adequar a campanha à capacidade real do time de vendas.

Com 20.000 ligações, o modelo captura 86,37% dos clientes interessados na base de validação, contra uma expectativa de 12,49% de taxa média em uma abordagem sem priorização. Em termos financeiros, a solução estima um incremento de R$ 7,34 milhões de receita em relação ao cenário aleatório, mantendo o mesmo custo operacional de ligações.

A primeira versão em produção já permite que a área de negócio use o modelo para priorizar campanhas, reduzir desperdício de contatos e aumentar a eficiência comercial.

# 10.0 Próximos Passos de Melhoria

Os principais pontos de melhoria são:

1. Criar uma aplicação web ou dashboard para que o time comercial faça upload da base e baixe a lista priorizada.
2. Automatizar no relatório final o cálculo de cenários para qualquer volume de ligações escolhido pelo time de negócio.
3. Exportar e versionar as imagens de EDA, curva lift, curva de ganho e receita acumulada para enriquecer o README.
4. Monitorar a performance do modelo em produção, comparando conversões reais com as probabilidades previstas.
5. Criar logs de requisição e resposta da API para auditoria e melhoria contínua.
6. Testar novas abordagens de rankeamento, como modelos específicos de learning to rank.
7. Reavaliar as premissas financeiras com dados reais de ticket médio, conversão e custo operacional.
8. Melhorar o tratamento de erros da API e adicionar testes automatizados para o pipeline de produção.

# 11.0 Aprendizados do Projeto

Os principais aprendizados deste projeto foram:

1. A principal foi isolar as funções e criar um pipeline próprio. Apesar de saber que existem funções no pandas e sklearn para construção de pipelines, optei por construir o meu na mão para todas as partes do código.
2. Algo que já faço com frequência e gosto muito é separar os notebooks dos projetos, tanto para otimizar o trabalho com o CRISP-DM, quanto para economizar recursos da minha máquina (que não é tão potente).
3. Nem todo problema de negócio utilizará as métricas padrões. Apesar dos modelos serem "padrões", os problemas diferenciam-se e suas métricas também. Neste caso, tive que modificar a métrica para uma que se adaptaria ao modelo.

# 12.0 Contatos

<ul class="actions">
    <table>
        <tr>
            <th><i class="fa-solid fa-folder-tree"></i><a href="https://gabriel-nobre-galvao.notion.site/Portf-lio-de-Projetos-em-Dados-51dd21d9aadb4a278f3f015992c92ee9?source=copy_link"> Portfólio de Projetos</a></th>
            <th><i class="fa-brands fa-linkedin"></i><a href="https://www.linkedin.com/in/gabriel-nobre-galvao/"> Linkedin</a></th>
            <th><i class="fa-brands fa-medium"></i><a href="https://medium.com/@gabrielnobregalvao"> Medium</a></th>
            <th><i class="fa-brands fa-github"></i><a href="https://github.com/Gabrielnbr"> GitHub</a></th>
            <th><i class="fa-solid fa-envelope"></i><a href="mailto:gabrielnobregalvao@gmail.com"> E-mail</a></th>
        </tr>
    </table>
</ul>