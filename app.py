import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Indonesian Coffee Shop Dashboard", layout="wide"
)

st.title("Indonesian Coffee Shop & F and B Consumer Trends Dashboard")
st.markdown(
    "Interactive analytics dashboard tracking daily transactions, menu category"
    " popularity, digital payment adoption, and customer satisfaction across"
    " Indonesian coffee shops."
)


# Fungsi untuk memuat dataset CSV
@st.cache_data
def load_coffee_data():
  filename = "indonesia_coffee_shop_sales.csv"
  if os.path.exists(filename):
    df = pd.read_csv(filename)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df
  else:
    return pd.DataFrame()


df = load_coffee_data()

if df.empty:
  st.warning(
      "Dataset file (`indonesia_coffee_shop_sales.csv`) not found. Please ensure"
      " the CSV file is uploaded."
  )
else:
  # Sidebar Filters
  st.sidebar.header("Filter Options")

  cities = sorted(df["city"].unique())
  selected_cities = st.sidebar.multiselect(
      "Select Cities:", options=cities, default=cities
  )

  categories = sorted(df["menu_category"].unique())
  selected_categories = st.sidebar.multiselect(
      "Select Menu Category:", options=categories, default=categories
  )

  payment_methods = sorted(df["payment_method"].unique())
  selected_payments = st.sidebar.multiselect(
      "Select Payment Method:", options=payment_methods, default=payment_methods
  )

  # Filter DataFrame
  filtered_df = df[
      (df["city"].isin(selected_cities))
      & (df["menu_category"].isin(selected_categories))
      & (df["payment_method"].isin(selected_payments))
  ]

  # Executive Metrics Overview
  st.subheader("Executive Performance Summary")
  col1, col2, col3, col4 = st.columns(4)

  total_rev = filtered_df["total_revenue_idr"].sum() if not filtered_df.empty else 0
  total_trx = len(filtered_df)
  avg_ticket = total_rev / total_trx if total_trx > 0 else 0
  avg_rating = (
      filtered_df["customer_rating"].mean() if not filtered_df.empty else 0
  )

  with col1:
    st.metric(label="Total Revenue", value=f"Rp {total_rev:,.0f}")
  with col2:
    st.metric(label="Total Transactions", value=f"{total_trx:,} Orders")
  with col3:
    st.metric(label="Avg. Ticket Size (ATS)", value=f"Rp {avg_ticket:,.0f}")
  with col4:
    st.metric(label="Avg. Customer Rating", value=f"{avg_rating:.2f} / 5.0")

  st.markdown("---")

  # Visualizations Layout
  col_a, col_b = st.columns(2)

  with col_a:
    st.subheader("Revenue by Menu Category")
    if not filtered_df.empty:
      cat_rev = (
          filtered_df.groupby("menu_category")["total_revenue_idr"]
          .sum()
          .reset_index()
      )
      fig_cat = px.bar(
          cat_rev,
          x="menu_category",
          y="total_revenue_idr",
          color="menu_category",
          title="Total Revenue per Category (IDR)",
          labels={
              "menu_category": "Category",
              "total_revenue_idr": "Revenue (IDR)",
          },
      )
      st.plotly_chart(fig_cat, use_container_width=True)

  with col_b:
    st.subheader("Payment Method Preferences")
    if not filtered_df.empty:
      pay_share = (
          filtered_df.groupby("payment_method")["total_revenue_idr"]
          .sum()
          .reset_index()
      )
      fig_pay = px.pie(
          pay_share,
          names="payment_method",
          values="total_revenue_idr",
          title="Payment Method Share",
          hole=0.4,
      )
      st.plotly_chart(fig_pay, use_container_width=True)

  # Timeline Trend
  st.subheader("Daily Coffee Sales Revenue Trend")
  if not filtered_df.empty:
    daily_trend = (
        filtered_df.groupby("transaction_date")["total_revenue_idr"]
        .sum()
        .reset_index()
    )
    fig_time = px.line(
        daily_trend,
        x="transaction_date",
        y="total_revenue_idr",
        title="Transaction Revenue Over Time",
        labels={
            "transaction_date": "Date",
            "total_revenue_idr": "Revenue (IDR)",
        },
    )
    st.plotly_chart(fig_time, use_container_width=True)

  # Raw Data Expander
  with st.expander("View Raw Coffee Shop Sales Dataset"):
    st.dataframe(df, use_container_width=True)
