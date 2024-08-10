# Import des librairies 
import pandas as pd 
import streamlit as st
from tools import * 
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container
import matplotlib.pyplot as plt 
import plotly.express as px

# Import du fichier excel

st.set_page_config(
    page_title="Dashboard Projet Streamlit", 
    page_icon=":bar_chart:", 
    layout="wide")

st.header("Streamlit Dashboard Projet Streamlit", divider=True)
st.subheader("Global Sales Analytics")



df = file_load_excel("./datasets/billing.xlsx")

df_cleaned = clean_data(df)

# Nombre de produits


# Nombre de commandes 
total_orders = df_cleaned.invoice_no.nunique()


# Nombre de States 
total_states = df_cleaned.state.nunique()

# Nombre de pays 
total_countries = df_cleaned.country.nunique()

# nombre de categories de produits 
total_categories = df_cleaned.category.nunique()


# CA global
global_ca = df_cleaned["total_price"].sum()

# CA moyen 
mean_ca = df_cleaned["total_price"].mean()
# Profit global
global_profit = df_cleaned["profit"].sum()


# CA par produit

# print(df_cleaned.groupby("product_id")["total_price"].sum().sort_values(ascending=False))
# print(df_cleaned.groupby("product_id")["total_price"].sum())
# CA par categorie 
# print(df_cleaned.groupby("category")["total_price"].sum().sort_values(ascending=False))
# Nbr commande par état 
# print(df_cleaned.groupby("state")["invoice_no"].count().sort_values(ascending=False))
# Nbr commande par pays
print(df_cleaned.groupby("country")["invoice_no"].count().sort_values(ascending=False))

# evolution du CA dans le temps (mois, annee, ...)
# print(df_cleaned.groupby("product_name")["invoice_no"].count().nlargest(3))
# top 3 produits les plus vendus
# top 3 produits qui font le plus de CA
# df_cleaned.groupby("product_id")["total_price"].sum().nlargest(3)
# top 3 states qui font le plus de CA 
# top 3 categories les plus frequemment achetees
# Le mois le plus profitable 


with st.sidebar:

    st.sidebar.image("./assets/logo.png")

    st.sidebar.header("Dashboard Options")
    st.sidebar.title("Filters")

    st.sidebar.subheader("Countries")
    country=st.sidebar.multiselect(
        "SELECT COUNTRY",
        options=df_cleaned["country"].unique(),
        default=df_cleaned["country"].unique(),
    )

    st.sidebar.subheader("Years")
    year=st.sidebar.multiselect(
        "SELECT YEAR",
        options=df_cleaned["year"].unique(),
        default=df_cleaned["year"].unique(),
    )


    st.sidebar.subheader("Categories")
    category=st.sidebar.multiselect(
        "SELECT Category",
        options=df_cleaned["category"].unique(),
        default=df_cleaned["category"].unique(),
    )

    df_selection=df_cleaned.query(
        "country==@country & category ==@category & year ==@year"
    )






st.title("Main KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Total Products", value=get_total_products(df_selection), delta="All products")
col2.metric(label="Total Orders", value=total_orders, delta="All orders")
col3.metric(label="Total States", value=total_states, delta="All states")
col4.metric(label="Total Countries", value=total_countries, delta="All countries")

style_metric_cards()


st.title("Top Sales")

col1, col2 = st.columns(2)

with col1: 
    with chart_container(df_selection):

        profit_by_cat = (
            df_selection.groupby('category')['profit'].sum()
            .sort_values(ascending=False)
            .reset_index(drop=False)
        )
        # st.write(profit_by_cat)
        st.bar_chart(profit_by_cat, y="profit")
        # fig = px.bar(profit_by_cat, x="category", y="profit", color="category", title="Category Profit")
        # fig.update_layout(legend_title="Country", legend_y=0.9)
        # fig.update_traces(textposition="outside",textfont_size=16, textangle=0, texttemplate="%{y:,.0f}")
        # st.plotly_chart(fig, use_container_width=True)


with col2:
    with chart_container(df_selection):
        
        profit_by_cat = df_selection.groupby('category')['profit'].sum().sort_values(ascending=False).reset_index()
        st.dataframe(profit_by_cat)

        fig = px.pie(profit_by_cat, values="profit", names="category", title="Category Profit", hole=0.5)
        # fig = px.pie(df_selection, values="total_price", names="category", title="Category Sales", hole=0.5)
        fig.update_layout(legend_title="Les Category", legend_y=0.9)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)


with st.container():
    # Aggregate profit by order_date
    profit_by_date = df_selection.groupby('order_date')['profit'].sum().reset_index()
    # Plotting
    st.title('Profit Evolution Over Time')

    
    fig = px.area(
        profit_by_date, 
        x='order_date', 
        y='profit',
        title='Profit Over Time',
        labels={'profit': 'Profit', 'order_date': 'Order Date'},
        template='plotly_dark',  # You can try 'plotly', 'seaborn', 'ggplot2', etc.
    )

    # Customize the layout and style
    fig.update_layout(
        xaxis_title='Order Date',
        yaxis_title='Profit ($)',
        title_font_size=24,
        title_font_family='Arial',
        title_x=0.5,  # Center the title
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
    )

    # Optional: Add hover mode and line settings
    fig.update_traces(
        line=dict(color='royalblue'),
        hovertemplate='Date: %{x}<br>Profit: $%{y:,.2f}<extra></extra>',
    ) 

    st.plotly_chart(fig)



with st.expander("datasets"):
    data_to_show = st.multiselect("Select columns to display", df_cleaned.columns, default=["invoice_no", "product_id", "product_name", "category", "order_qty", "country", "state", "total_price", "profit", "order_date"])
    st.dataframe(df_selection[data_to_show], use_container_width=True)













