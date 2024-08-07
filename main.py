# Import des librairies 
import pandas as pd 
import streamlit as st
from tools import * 

# Import du fichier excel

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


st.header("COhorte One| Dashboard Projet Streamlit", divider=True)
st.subheader("Global Sales Analytics")

st.title("Main KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Total Products", value=get_total_products(df_cleaned))
col2.metric(label="Total Orders", value=total_orders)
col3.metric(label="Total States", value=total_states)
col4.metric(label="Total Countries", value=total_countries)


st.title("Top Sales")

col1, col2 = st.columns(2)

col1.bar_chart(df_cleaned[["product_name", "country", "state", "profit"]], x="product_name", y="profit", color="country")

col2.bar_chart(df_cleaned.groupby("category")["total_price"].sum().nlargest(10).sort_values(ascending=False), horizontal=True)


st.line_chart(df_cleaned[["order_date", "total_price"]], x="order_date", y="total_price", x_label="Date", y_label="CA")

st.title("Top Products")
st.dataframe(df_cleaned)













