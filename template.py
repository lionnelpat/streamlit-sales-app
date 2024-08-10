import pandas as pd 
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container
import matplotlib.pyplot as plt 
import plotly.express as px


st.set_page_config(
    page_title="Page title", 
    page_icon=":bar_chart:", 
    layout="wide")



def header():
    col1, col2 = st.columns([1,3])
    with col1:
        st.image("./assets/logo.png")

    with col2:
        st.title("Streamlit Dashboard Projet Streamlit")
        st.subheader("Global Sales Analytics")

def sidebar():

    with st.sidebar:

        st.image("./assets/logo.png")

        st.header("Dashboard Options")

        st.sidebar.subheader("Countries")
        country=st.sidebar.selectbox(
            "SELECT filter one",
            options=("USA", "CANADA", "FRANCE"),
        )

        st.sidebar.subheader("Years")
        year=st.sidebar.multiselect(
            "SELECT YEAR",
            options=[2018, 2019, 2020],
            default=[2018, 2019, 2020],
        )

        st.sidebar.subheader("Months")
        month=st.sidebar.multiselect(
            "SELECT MONTH",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            default=[1, 2, 3, 4],
        )
        st.divider()

def metrics():
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="Total Products", value="19", delta="All products")
    col2.metric(label="Total Orders", value="100", delta="All orders")
    col3.metric(label="Total States", value="20", delta="All states")
    col4.metric(label="Total Countries", value="5", delta="All countries")

    style_metric_cards()


@st.cache_data
def df_cleaned():
    df = pd.read_excel("./datasets/billing.xlsx" )
    df.dropna(axis=0, how="all", inplace=True)
    df.rename(columns={
        "Invoice No": "invoice_no",
        "Product ID": "product_id",
        "Product Name": "product_name",
        "Product Category": "category",
        "Order Quantity": "order_qty",
        "Country": "country",
        "State": "state",
        "Total Price": "total_price",
        "Profit": "profit",
        "Order Date": "order_date"
    }, inplace=True)

    return df

def datasets():

    df = df_cleaned()
    with st.expander("View Dataset"):
        df_selected = st.multiselect("SELECT COLUMNS", df.columns, default=["country"])
        st.dataframe(df[df_selected])


def bar_chart():
    
    df = df_cleaned()
    with chart_container(df):
        fig = px.bar(df, x="category", y="invoice_no")

        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Orders",
            title="Category Orders",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title="Country",
            legend_y=0.9
        )
        st.plotly_chart(fig)


if __name__ == "__main__":

    header()

    sidebar()

    with st.container():
        metrics()

        datasets()

        bar_chart()