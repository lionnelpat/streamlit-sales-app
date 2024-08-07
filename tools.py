import pandas as pd

def file_load_excel(data_path): 
    try:
        return pd.read_excel(data_path)
    except FileNotFoundError:
        print("File not found")
        None
    except ModuleNotFoundError:
        print("Module not found")
        None

def clean_data(df): 
    cleanned_df = df.dropna(axis=0, how="all")
    cleanned_df = cleanned_df.rename(columns={
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
    })

    cleanned_df["year"] = cleanned_df["order_date"].dt.year
    cleanned_df["month"] = cleanned_df["order_date"].dt.month
    cleanned_df["day"] = cleanned_df["order_date"].dt.day

    return cleanned_df

def get_total_products(df):
    return df.product_id.nunique()