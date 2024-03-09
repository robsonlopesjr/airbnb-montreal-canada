import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(
    page_title='Analisando os Dados do Airbnb da cidade de Montreal(Canada)',
    page_icon='📊',
    layout='wide'
)


@st.cache_data
def load_data():
    data = pd.read_csv('./dataset/listings.csv')
    print(data.info())

    return data


def init():
    df = load_data()

    st.write(
        "Q1. Quantos atributos (variáveis) e quantas entradas o conjunto de dados possui? Quais os tipos das variáveis?"
    )

    st.write("Entradas: {}".format(df.shape[0]))
    st.write("Variáveis: {}".format(df.shape[1]))

    st.table(df.dtypes)

    st.write("Q2.Qual a porcentagem de valores ausentes no dataset?")
    df_null = (df.isnull().sum() / df.shape[0]).sort_values(ascending=False) * 100
    st.table(df_null)

    st.write("Q3. Qual o tipo de distribuição das variáveis?")

    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            fig, ax = plt.subplots()
            ax.hist(df.price, bins=15, color='blue', edgecolor='black')
            ax.set_title('price')
            ax.set_xlabel('Price')
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.hist(df.minimum_nights, bins=15, color='blue', edgecolor='black')
            ax.set_title('minimum_nights')
            ax.set_xlabel('Minimum nights')
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

        with col3:
            fig, ax = plt.subplots()
            ax.hist(df.number_of_reviews, bins=15, color='blue', edgecolor='black')
            ax.set_title('number_of_reviews')
            ax.set_xlabel('Number of reviews')
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            fig, ax = plt.subplots()
            ax.hist(df.reviews_per_month, bins=15, color='blue', edgecolor='black')
            ax.set_title('reviews_per_month')
            ax.set_xlabel('Reviews per month')
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.hist(df.calculated_host_listings_count, bins=15, color='blue', edgecolor='black')
            ax.set_title('calculated_host_listings_count')
            ax.set_xlabel('Calculated host listings count')
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

        with col3:
            fig, ax = plt.subplots()
            ax.hist(df.availability_365, bins=15, color='blue', edgecolor='black')
            ax.set_title('availability_365')
            ax.set_xlabel('Availability 365')
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

    st.write("Q4. Qual a média dos preços de aluguel?")
    st.write("CAD ${:.2f}".format(df.price.mean()))

    st.write("Q5. Qual a correlação existente entre as variáveis")
    # montar matriz de correlação
    corr = df[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
               'calculated_host_listings_count', 'availability_365']].corr()
    st.table(corr)

    fig = px.imshow(corr,
                    labels=dict(color="Correlação"),
                    x=corr.index,
                    y=corr.columns,
                    color_continuous_scale='RdBu',
                    zmin=-1, zmax=1)

    fig.update_layout(title='Heatmap de Correlação',
                      width=700,
                      height=600)

    # Adicionar anotações aos quadrados do heatmap
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            fig.add_annotation(x=j, y=i, text=f"{corr.iloc[i, j]:.2f}",
                               font=dict(color='black', size=12),
                               showarrow=False)

    st.plotly_chart(fig)

    st.write("Q6. Qual o tipo de imóvel mais alugado no Airbnb?")
    value_counts = df.room_type.value_counts()
    percentagem = (df.room_type.value_counts() / df.shape[0]) * 100

    st.table({
        'Room Type': value_counts.index,
        'Count': value_counts.values,
        'Percent': percentagem.values
    })

    st.write("Q7. Qual a localidade mais cara do dataset?")
    st.table(df.groupby(['neighbourhood']).price.mean().sort_values(ascending=False))

    houses = df[['id', 'price', 'latitude', 'longitude']]

    # excluindo entradas com dados faltantes
    houses.dropna(axis=0, inplace=True)

    fig = px.scatter_mapbox(
        houses,
        lat='latitude',
        lon='longitude',
        size='price',
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=50,
        zoom=10
    )

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, margin={'r': 0, 'l': 0, 't': 0, 'b': 0})
    st.plotly_chart(fig)

    st.write("Q8. Qual é a média do mínimo de noites para aluguel (minimum_nights)?")
    st.write("Mínimo de noites (média): {:.2f}".format(df.minimum_nights.mean()))


if __name__ == "__main__":
    init()
