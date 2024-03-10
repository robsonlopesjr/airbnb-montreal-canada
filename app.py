import streamlit as st
import pandas as pd
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

    # SIDEBAR
    st.sidebar.header("Parâmetros")
    info_sidebar = st.sidebar.empty()  # Serão mostradas o total de registros

    room_type_filter = st.sidebar.multiselect(
        label='Tipo de imóvel',
        options=df.room_type.unique().tolist(),
        default=df.room_type.unique().tolist()
    )

    st.sidebar.markdown("""
    A base de dados de pode ser acessada em http://insideairbnb.com/get-the-data/
    """)

    # Main area

    filtered_df = df[df.room_type.isin(room_type_filter)]

    info_sidebar.info("{} registros selecionados.".format(filtered_df.shape[0]))

    tab1, tab2 = st.tabs(['Visão Gerencial', 'Visão Geográfica'])

    with tab1:
        with st.container():
            st.header("Métricas")

            col1, col2 = st.columns(2)
            with col1:
                col1.metric('Média de Preços:', "CAD ${:.2f}".format(filtered_df.price.mean()))

            with col2:
                col2.metric('Mínimo de noites (média):', "{:.2f}".format(filtered_df.minimum_nights.mean()))

        with st.container():
            st.write("Qual o tipo de imóvel mais alugado no Airbnb?")

            value_counts = filtered_df.room_type.value_counts()
            percentagem = (filtered_df.room_type.value_counts() / filtered_df.shape[0]) * 100
            st.table({
                'Room Type': value_counts.index,
                '%': percentagem.values
            })

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                col1.write("Quais as 5 localidades mais caras?")
                col1.table(filtered_df.groupby(['neighbourhood']).price.mean().sort_values(ascending=False)[:5])

            with col2:
                col2.write("Quais as 5 localidades mais baratas?")
                col2.table(filtered_df.groupby(['neighbourhood']).price.mean().sort_values(ascending=True)[:5])

        with st.container():
            st.write("Qual a correlação existente entre as análises")
            # montar matriz de correlação
            corr = filtered_df[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
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

    with tab2:
        houses = filtered_df[['id', 'price', 'latitude', 'longitude']]

        # excluindo entradas com dados faltantes
        houses.dropna(axis=0, inplace=True)

        fig = px.scatter_mapbox(
            houses,
            lat='latitude',
            lon='longitude',
            size='price',
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=30,
            zoom=10
        )

        fig.update_layout(mapbox_style='open-street-map')
        fig.update_layout(height=600, margin={'r': 0, 'l': 0, 't': 0, 'b': 0})
        st.plotly_chart(fig)


if __name__ == "__main__":
    init()
