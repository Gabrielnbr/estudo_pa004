# PA004 - Health Insurance Cross Sell

## Entendimento do Negócio

### Motivação

A empresa é a Insurance ALL, responsável por fornecer somente seguros de saúde.
Com o crescimento da empresa o CEO e os lideres responsáveis resolveram ampliar os tipos de seguros que fornecem. Indo para os seguros automotivos.

### Dados

A empresa fez uma pesquisa com cerca de 380 mil clientes, para saber quem tem interesse em adiquirir o novo produto. Ao final da pesquisa 127 mil clientes não responderam.

Desta forma o time de negócio pensou em fazer uma pesquisa ativa ligando para todos os clientes, mas há uma capacidade de realizar somente 20 mil ligações durante o período da campanha.

### Problema

O time de negócio quer saber quais são os 20 mil clientes têm tendência maior em adquirir o novo produto.

### Perguntas complementares

O time de negócio também tem algumas perguntas a mais para entender melhor como solucionar este problema.

1. Quais são os principais Insights sobre os atributos mais relevantes de clientes interessados em adquirir um seguro de automóvel?
2. Qual a porcentagem de clientes interessados em adquirir um seguro de automóvel, o time de vendas conseguirá contatar fazendo 20.000 ligações?
3. E se a capacidade do time de vendas aumentar para 40.000 ligações, qual a porcentagem de clientes interessados em adquirir um seguro de automóvel o time de vendas conseguirá contatar?
4. Quantas ligações o time de vendas precisa fazer para contatar 80% dos clientes interessados em adquirir um seguro de automóvel?

## Estrutura dos Dados

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

## Acesso aos Dados

A empresa disponibilizou o seu banco de dado Postgres, cujo localiza-se na AWS.

## Roteiro da Solução

1. Conexão com o banco de dados.
2. Limpeza e Tratamento dos dados.
3. Utilização da estatística descritiva para uma noção geral dos dados.
4. Criar hipóteses e verificar as relações Bivariadas e Multivariadas.
5. Preparar os dados para utilização dos Algorítimos de Machine Learnning.
6. Treinar os modelos.
7. Realizar o cross-validation a fim de identificar o melhor modelo.
8. Realizar o fine tuning.
9. Verificar a performance do modelo e traduzir para o time de negócio
   1.  Responder as perguntas complementares.
   2.  Gerar um relatório para o time de negócio explicando as métricas e como o modelo esta performando.
10. Colocar o modelo em produção e desenvolver uma API para que o time de negócio tenha acesso.

## Ferramentas a serem utilizadas

As ferramentas serão:
1. IDE: VSCode com suporte para o Jupter Notebook.
2. Linguagem de programação:
   1. Python para análise de dados e desenvolvimento dos algorítimos de Machine Learnning.
   2. SQL para acesso as informações dos bancos de dados.
3. Produção: Heroku.
4. Versionamento: Git e GitHub.