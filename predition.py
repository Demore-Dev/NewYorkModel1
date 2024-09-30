import pandas as pd 
import streamlit as st
import plotly.express as px
import sklearn as skl

# Configurar o layout da página
st.set_page_config(page_title="Mapa de Moradias por Tipo ou Preço")

#lendo o dataset
df = pd.read_csv('NY-House-Dataset.csv')

#Remover todos os espaços, para ficar mais fácil
#de identificar cada tipo
df['TYPE'] = df['TYPE'].str.replace(' ', '', regex=False)

#mostrando as primeiras linhas do dataset,
#para ter uma noção melhor
#print(df.head())

#mostrando todas as colunas, para eu saber 
#quais utilizareI (neste caso, serão "TYPE", "PRICE", "LATITUDE", "LONGITUDE")
#print(df.columns)


# Verificar se há valores nulos nas colunas necessárias
null_columns = df[['TYPE', 'PRICE', 'LATITUDE', 'LONGITUDE']].isnull().any()

# Defina os limites de acordo com os dados do seu dataset
min_price = df['PRICE'].min() #preço mínimo
max_price = df['PRICE'].quantile(0.85) #preço máximo

# Agrupando os tipos de moradia
def map_moradia(tipo):
    if 'houseforsale' in tipo.lower():
        return 'Casa'
    elif 'landforsale' in tipo.lower():
        return 'Terreno'
    else:
        return 'Outro'  # Para qualquer outro tipo que não se encaixe
    
#criando uma nova coluna no dataframe para separar
#as moradias por tipo
df['CATEGORIAS'] = df['TYPE'].apply(map_moradia)

# Botão para alternar entre visualizações
if st.button("Alternar visualização"):
    # Alternar a variável que controla a visualização
    if 'show_by_price' not in st.session_state:
        st.session_state.show_by_price = False
    st.session_state.show_by_price = not st.session_state.show_by_price

# Verificação de valores nulos
if null_columns.any():
    st.error("Existem valores nulos nas seguintes colunas: " + ', '.join(null_columns[null_columns].index))
else:
    # Criar o mapa com Plotly
    if st.session_state.get('show_by_price', False):
        # Visualizar por preço
        fig = px.scatter_mapbox(df, 
                                 lat='LATITUDE', 
                                 lon='LONGITUDE', 
                                 color='PRICE',  # Cor baseada no preço
                                 color_continuous_scale=px.colors.sequential.Viridis,  # Escala de cores do verde ao vermelho
                                 range_color=[min_price, max_price],  # Limites da escala de cor
                                 size=[10] * len(df),
                                 size_max=3,
                                 mapbox_style='carto-positron',
                                 zoom=10)
    else:
        # Visualizar por tipo
        fig = px.scatter_mapbox(df, 
                                 lat='LATITUDE', 
                                 lon='LONGITUDE', 
                                 color='CATEGORIAS',  # Cor baseada no tipo de moradia
                                 color_discrete_sequence=px.colors.qualitative.Plotly,  # Cores qualitativas para tipos
                                 size=[10] * len(df),
                                 size_max=3,
                                 mapbox_style='carto-positron',
                                 zoom=10)

    fig.update_traces(marker=dict(opacity=1))  # Ajuste a opacidade dos marcadores
    st.plotly_chart(fig)

#python -m streamlit run predition.py   
