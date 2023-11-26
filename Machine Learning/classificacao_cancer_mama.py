# -*- coding: utf-8 -*-
"""Classificacao_Cancer_Mama.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ISQT78C_FeCDxm-k6Y1B-yyLH1ch48x

#MVP: Dataset do Câncer de *Mama*
###Carregamento e exploração inicial do dataset relacionado ao câncer de mama, onde haverá o retorno do diagnostico.
"""

# configuração para não exibir os warnings
import warnings
warnings.filterwarnings("ignore")

# Imports necessários
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

"""## Carga do Dataset
Carregamento e Exploração Inicial do Dataset:
<br>

Descrição: <br>

* Carregamento do dataset relacionado ao câncer de mama.
* Transformação do diagnóstico para valores numéricos: Benigno (B) = 0, Maligno (M) = 1.
* Reorganização das colunas, movendo 'diagnosis' para o final.
Visualização das primeiras linhas do dataset.

<br>

Propósito:
* Preparação inicial do conjunto de dados para análise e modelagem.
"""

import pandas as pd

# Informa a URL de importação do dataset
url = "https://raw.githubusercontent.com/FelipeAmorimReis/CancerMama-MVP-MachineLearning/main/CSV/breast-cancer-wisconsin-data/data.csv"

# Lê o arquivo, ignorando a última coluna, pois não continha informações úteis para a análise
dataset = pd.read_csv(url, delimiter=',', usecols=lambda column: column != 'Unnamed: 32')

 # Alterando retorno, onde: Beligno: 0 | Maligno: 1
dataset['diagnosis'] = dataset['diagnosis'].map({'B': 0, 'M': 1})

# Reorganiza as colunas, movendo 'diagnosis' para o final
dataset = dataset[[col for col in dataset.columns if col != 'diagnosis'] + ['diagnosis']]

# Mostra todas as colunas
pd.set_option('display.max_columns', None)

# Mostra as primeiras linhas do dataset
dataset.head()

"""
## Separação em conjunto de treino e conjunto de teste com holdout

Descrição:

* Definição do tamanho do conjunto de teste (20% do dataset).
* Utilização de uma semente aleatória para garantir reproducibilidade.
* Separação dos conjuntos de treino e teste utilizando a técnica de holdout com estratificação.
* Parâmetros e configurações para a validação cruzada com estratificação.

<br>
Propósito:

* Divisão dos dados em conjuntos de treino e teste para treinamento e avaliação dos modelos."""

test_size = 0.20 # tamanho do conjunto de teste
seed = 7 # semente aleatória

# Separação em conjuntos de treino e teste
array = dataset.values
X = array[:,0:31]
y = array[:,31]
X_train, X_test, y_train, y_test = train_test_split(X, y,
    test_size=test_size, shuffle=True, random_state=seed, stratify=y) # holdout com estratificação

# Parâmetros e partições da validação cruzada
scoring = 'accuracy'
num_particoes = 10
kfold = StratifiedKFold(n_splits=num_particoes, shuffle=True, random_state=seed) # validação cruzada com estratificação

"""## Modelagem e Inferência

# Avaliação de Modelos:

Descrição:

* Definição de uma semente global para garantir a reprodutibilidade.
* Criação de modelos de classificação, incluindo KNN, Decision Tree, Naive Bayes e SVM.
* Avaliação dos modelos por meio da validação cruzada com estratificação.
* Exibição de um boxplot comparativo dos desempenhos dos modelos.

<br>
Propósito:

* Análise comparativa inicial dos modelos em termos de acurácia.
"""

np.random.seed(7) # definindo uma semente global

# Lista que armazenará os modelos
models = []

# Criando os modelos e adicionando-os na lista de modelos
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

# Listas para armazenar os resultados
results = []
names = []

# Avaliação dos modelos
for name, model in models:
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# Boxplot de comparação dos modelos
fig = plt.figure(figsize=(15,10))
fig.suptitle('Comparação dos Modelos')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""### Criação e avaliação de modelos: dados padronizados e normalizados


Descrição:

* Definição de uma semente global para garantir a reprodutibilidade.
* Criação de pipelines para cada algoritmo de classificação, aplicando diferentes transformações nos dados.
* Algoritmos utilizados: KNN, Árvore de Classificação, Naive Bayes e SVM.
* Transformações aplicadas: Original, Padronizado (StandardScaler) e Normalizado (MinMaxScaler).
* Avaliação dos modelos por meio da validação cruzada com estratificação.
* Exibição de um boxplot comparativo dos desempenhos dos modelos.

<br>
Propósito:

* Analisar o impacto das transformações de dados nos modelos de classificação, permitindo a escolha da abordagem mais adequada.
"""

np.random.seed(7) # definindo uma semente global para este bloco

# Listas para armazenar os armazenar os pipelines e os resultados para todas as visões do dataset
pipelines = []
results = []
names = []


# Criando os elementos do pipeline

# Algoritmos que serão utilizados
knn = ('KNN', KNeighborsClassifier())
cart = ('CART', DecisionTreeClassifier())
naive_bayes = ('NB', GaussianNB())
svm = ('SVM', SVC())

# Transformações que serão utilizadas
standard_scaler = ('StandardScaler', StandardScaler())
min_max_scaler = ('MinMaxScaler', MinMaxScaler())


# Montando os pipelines

# Dataset original
pipelines.append(('KNN-orig', Pipeline([knn])))
pipelines.append(('CART-orig', Pipeline([cart])))
pipelines.append(('NB-orig', Pipeline([naive_bayes])))
pipelines.append(('SVM-orig', Pipeline([svm])))

# Dataset Padronizado
pipelines.append(('KNN-padr', Pipeline([standard_scaler, knn])))
pipelines.append(('CART-padr', Pipeline([standard_scaler, cart])))
pipelines.append(('NB-padr', Pipeline([standard_scaler, naive_bayes])))
pipelines.append(('SVM-padr', Pipeline([standard_scaler, svm])))

# Dataset Normalizado
pipelines.append(('KNN-norm', Pipeline([min_max_scaler, knn])))
pipelines.append(('CART-norm', Pipeline([min_max_scaler, cart])))
pipelines.append(('NB-norm', Pipeline([min_max_scaler, naive_bayes])))
pipelines.append(('SVM-norm', Pipeline([min_max_scaler, svm])))

# Executando os pipelines
for name, model in pipelines:
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %.3f (%.3f)" % (name, cv_results.mean(), cv_results.std()) # formatando para 3 casas decimais
    print(msg)

# Boxplot de comparação dos modelos
fig = plt.figure(figsize=(25,6))
fig.suptitle('Comparação dos Modelos - Dataset orginal, padronizado e normalizado')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names, rotation=90)
plt.show()

"""### Otimização dos hiperparâmetros

Descrição:

* Definição de uma semente global para garantir a reprodutibilidade.
* Criação de pipelines para o KNN considerando diferentes transformações nos dados: Original, Padronizado (StandardScaler) e Normalizado (MinMaxScaler).
* Especificação de um conjunto de hiperparâmetros a serem avaliados por meio do GridSearchCV.
* Avaliação dos modelos com validação cruzada e busca pelos melhores hiperparâmetros.
* Exibição da melhor configuração encontrada para cada abordagem de dados.

<br>

Propósito:

* Otimizar os hiperparâmetros do KNN para melhorar seu desempenho, considerando diferentes transformações de dados.

"""

# Tuning do KNN

np.random.seed(7) # definindo uma semente global para este bloco

pipelines = []

# Definindo os componentes do pipeline
knn = ('KNN', KNeighborsClassifier())
standard_scaler = ('StandardScaler', StandardScaler())
min_max_scaler = ('MinMaxScaler', MinMaxScaler())

pipelines.append(('knn-orig', Pipeline(steps=[knn])))
pipelines.append(('knn-padr', Pipeline(steps=[standard_scaler, knn])))
pipelines.append(('knn-norm', Pipeline(steps=[min_max_scaler, knn])))

param_grid = {
    'KNN__n_neighbors': [1,3,5,7,9,11,13,15,17,19,21],
    'KNN__metric': ["euclidean", "manhattan", "minkowski"],
}

# Prepara e executa o GridSearchCV
for name, model in pipelines:
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=kfold)
    grid.fit(X_train, y_train)
    # imprime a melhor configuração
    print("Sem tratamento de missings: %s - Melhor: %f usando %s" % (name, grid.best_score_, grid.best_params_))

"""## Finalização do Modelo

Descrição:

* Padronização do conjunto de treino usando o scaler ajustado a esse conjunto.
* Treinamento do modelo KNN com os hiperparâmetros otimizados (manhattan distance, 17 vizinhos).
* Padronização do conjunto de teste utilizando o mesmo scaler.
* Predição das classes no conjunto de teste e cálculo da acurácia.

<br>
Propósito:

* Avaliar o desempenho do modelo KNN otimizado utilizando o conjunto de testes.
"""

# Avaliação do modelo com o conjunto de testes

# Preparação do modelo
scaler = StandardScaler().fit(X_train) # ajuste do scaler com o conjunto de treino
rescaledX = scaler.transform(X_train) # aplicação da padronização no conjunto de treino
model = KNeighborsClassifier(metric='manhattan', n_neighbors=17)
model.fit(rescaledX, y_train)

# Estimativa da acurácia no conjunto de teste
rescaledTestX = scaler.transform(X_test) # aplicação da padronização no conjunto de teste
predictions = model.predict(rescaledTestX)
print(accuracy_score(y_test, predictions))

# Preparação do modelo com TODO o dataset
scaler = StandardScaler().fit(X) # ajuste do scaler com TODO o dataset
rescaledX = scaler.transform(X) # aplicação da padronização com TODO o dataset
model.fit(rescaledX, y)

"""## Simulando a aplicação do modelo em dados não vistos"""

# Novos dados - não sabemos a classe!
data_entrada = {
    'id': [800, 801, 802],
    'radius_mean': [10, 25, 3],
    'texture_mean': [5, 30, 3],
    'perimeter_mean': [50, 150, 3],
    'area_mean': [200, 1500, 3],
    'smoothness_mean': [0.1, 0.2, 3],
    'compactness_mean': [0.05, 0.3, 3],
    'concavity_mean': [0.1, 0.4, 3],
    'concave points_mean': [0.05, 0.2, 3],
    'symmetry_mean': [0.1, 0.3, 3],
    'fractal_dimension_mean': [0.05, 0.2, 3],
    'radius_se': [0.1, 1.0, 3],
    'texture_se': [0.1, 1.5, 3],
    'perimeter_se': [1, 10, 3],
    'area_se': [10, 100, 3],
    'smoothness_se': [0.005, 0.02, 3],
    'compactness_se': [0.005, 0.03, 3],
    'concavity_se': [0.01, 0.05, 3],
    'concave points_se': [0.005, 0.03, 3],
    'symmetry_se': [0.01, 0.03, 3],
    'fractal_dimension_se': [0.002, 0.01, 3],
    'radius_worst': [12, 30, 3],
    'texture_worst': [10, 35, 3],
    'perimeter_worst': [70, 200, 3],
    'area_worst': [300, 2000, 3],
    'smoothness_worst': [0.1, 0.3, 3],
    'compactness_worst': [0.05, 0.4, 3],
    'concavity_worst': [0.1, 0.5, 3],
    'concave points_worst': [0.05, 0.3, 3],
    'symmetry_worst': [0.1, 0.4, 3],
    'fractal_dimension_worst': [0.05, 0.3, 3],
}

atributos_entrada = [
    'id', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
    'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
    'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
    'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst',
    'symmetry_worst', 'fractal_dimension_worst'
]
entrada_novos_dados = pd.DataFrame(data_entrada, columns=atributos_entrada)


array_entrada = entrada_novos_dados.values
X_entrada = array_entrada[:,0:31].astype(float)

# Padronização nos dados de entrada usando o scaler utilizado em X
rescaledEntradaX = scaler.transform(X_entrada)
print(rescaledEntradaX)

# Predição de classes dos dados de entrada
saidas = model.predict(rescaledEntradaX)
print(saidas)