import streamlit as st
import pandas as pd
import plotly.express as px
from models import Sale, SessionLocal, init_db

init_db()
st.set_page_config(page_title="📊 Superstore Sales Dashboard", layout="wide")

def get_session():
    return SessionLocal()

def fetch_all_sales():
    s = get_session()
    rows = s.query(Sale).order_by(Sale.id).all()
    s.close()
    data = [{"id": r.id, "order_date": r.order_date, "region": r.region, "category": r.category, "sales": r.sales} for r in rows]
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["id", "order_date", "region", "category", "sales"])

st.title("📊 Superstore Sales Dashboard")

st.markdown("### 🔗 Quick Navigation")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ Add New Sale"):
        st.switch_page("pages/AddSale.py")
with col2:
    if st.button("✏️ Edit / Delete Records"):
        st.switch_page("pages/EditDelete.py")
with col3:
    if st.button("⬇️ Download Data"):
        st.switch_page("pages/Download.py")

df = fetch_all_sales()

st.sidebar.header("🔍 Filters")
if not df.empty:
    df["order_date"] = pd.to_datetime(df["order_date"])
    regions = ["All"] + sorted(df["region"].dropna().unique())
    categories = ["All"] + sorted(df["category"].dropna().unique())

    region = st.sidebar.selectbox("Region", regions)
    category = st.sidebar.selectbox("Category", categories)

    min_date, max_date = df["order_date"].min(), df["order_date"].max()
    start_date, end_date = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    search = st.sidebar.text_input("Search (Region/Category)").lower()

    filtered = df.copy()
    if region != "All":
        filtered = filtered[filtered["region"] == region]
    if category != "All":
        filtered = filtered[filtered["category"] == category]
    filtered = filtered[(filtered["order_date"].dt.date >= start_date) & (filtered["order_date"].dt.date <= end_date)]
    if search:
        mask = filtered["category"].str.lower().str.contains(search) | filtered["region"].str.lower().str.contains(search)
        filtered = filtered[mask]
else:
    filtered = df

st.markdown("## 📌 Key Metrics")
if not filtered.empty:
    total, count, avg = filtered["sales"].sum(), len(filtered), filtered["sales"].mean()
else:
    total, count, avg = 0, 0, 0

k1, k2, k3 = st.columns(3)
k1.success(f"💰 **Total Sales:** ${total:,.2f}")
k2.info(f"📦 **Orders:** {count}")
k3.warning(f"📊 **Avg Sales:** ${avg:,.2f}")

st.markdown("---")

st.markdown("## 📈 Visual Insights")
if not filtered.empty:
    # Chart 1: Bar Chart
    fig1 = px.bar(filtered.groupby("region", as_index=False)["sales"].sum(), x="region", y="sales", title="Sales by Region", color="region")
    st.plotly_chart(fig1, width='stretch', config={"displayModeBar": True})

    # Chart 2: Pie Chart
    fig2 = px.pie(filtered.groupby("category")["sales"].sum().reset_index(), names="category", values="sales", title="Sales by Category")
    st.plotly_chart(fig2, width='stretch', config={"displayModeBar": True})

    # Chart 3: Line Chart
    monthly = filtered.groupby(filtered["order_date"].dt.to_period("M"))["sales"].sum().reset_index()
    monthly["order_date"] = monthly["order_date"].astype(str)
    fig3 = px.line(monthly, x="order_date", y="sales", title="Monthly Sales Trend", markers=True)
    st.plotly_chart(fig3, width='stretch', config={"displayModeBar": True})
else:
    st.warning("⚠️ No data for selected filters")

'''st.markdown("## 📈 Visual Insights")
if not filtered.empty:
    # Define the configuration once to reuse for all charts
    chart_config = {
        "displayModeBar": True
    }

    # Chart 1: Bar Chart
    fig1 = px.bar(filtered.groupby("region", as_index=False)["sales"].sum(), x="region", y="sales", title="Sales by Region", color="region")
    st.plotly_chart(fig1, width='stretch', config=chart_config)

    # Chart 2: Pie Chart
    fig2 = px.pie(filtered.groupby("category")["sales"].sum().reset_index(), names="category", values="sales", title="Sales by Category")
    st.plotly_chart(fig2, width='stretch', config=chart_config)

    # Chart 3: Line Chart
    monthly = filtered.groupby(filtered["order_date"].dt.to_period("M"))["sales"].sum().reset_index()
    monthly["order_date"] = monthly["order_date"].astype(str)
    fig3 = px.line(monthly, x="order_date", y="sales", title="Monthly Sales Trend", markers=True)
    st.plotly_chart(fig3, width='stretch', config=chart_config)
else:
    st.warning("⚠️ No data for selected filters")'''

'''st.markdown("## 📈 Visual Insights")
if not filtered.empty:
    fig1 = px.bar(filtered.groupby("region", as_index=False)["sales"].sum(), x="region", y="sales", title="Sales by Region", color="region")
    #st.plotly_chart(fig1, config={"displayModeBar": True, "responsive": True}, use_container_width=True)
    #st.plotly_chart(fig1, config={"displayModeBar": True, "responsive": True}, width='stretch')
    st.plotly_chart(fig1, config={"displayModeBar": True}, width='stretch')

    fig2 = px.pie(filtered.groupby("category")["sales"].sum().reset_index(), names="category", values="sales", title="Sales by Category")
    #st.plotly_chart(fig2, config={"displayModeBar": True, "responsive": True}, use_container_width=True)
    #st.plotly_chart(fig2, config={"displayModeBar": True, "responsive": True}, width='stretch')
    st.plotly_chart(fig2, config={"displayModeBar": True}, width='stretch')

    monthly = filtered.groupby(filtered["order_date"].dt.to_period("M"))["sales"].sum().reset_index()
    monthly["order_date"] = monthly["order_date"].astype(str)
    fig3 = px.line(monthly, x="order_date", y="sales", title="Monthly Sales Trend", markers=True)
    #st.plotly_chart(fig3, config={"displayModeBar": True, "responsive": True}, use_container_width=True)
    #st.plotly_chart(fig3, config={"displayModeBar": True, "responsive": True}, width='stretch')
    st.plotly_chart(fig3, config={"displayModeBar": True}, width='stretch')
else:
    st.warning("⚠️ No data for selected filters")'''

st.markdown("---")
st.markdown("## 📋 Sales Records")
if not filtered.empty:
    show = filtered.copy()
    show["order_date"] = pd.to_datetime(show["order_date"]).dt.date
    #st.dataframe(show, use_container_width=True)
    st.dataframe(show, width='stretch')
else:
    st.error("❌ No rows match the filters.")
