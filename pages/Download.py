import streamlit as st
import pandas as pd
from models import Sale, SessionLocal, init_db

init_db()
st.set_page_config(page_title="⬇️ Download Sales Data", layout="wide")

if st.button("⬅️ Back to Dashboard"):
    st.switch_page("Home.py")

def get_session():
    return SessionLocal()

def fetch_all_sales():
    s = get_session()
    rows = s.query(Sale).order_by(Sale.id).all()
    s.close()
    data = [{"id": r.id, "order_date": r.order_date, "region": r.region, "category": r.category, "sales": r.sales} for r in rows]
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["id", "order_date", "region", "category", "sales"])

st.title("⬇️ Download Sales Data")
st.markdown("Here you can view all records and download them as CSV or Excel.")

df = fetch_all_sales()

if df.empty:
    st.warning("⚠️ No sales data available to download.")
else:
    # show data table
    show = df.copy()
    show["order_date"] = pd.to_datetime(show["order_date"]).dt.date
    #st.dataframe(show, use_container_width=True)
    st.dataframe(show, width='stretch')

    # download buttons
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="sales_data.csv",
        mime="text/csv"
    )

    excel = pd.ExcelWriter("sales_data.xlsx", engine="xlsxwriter")
    df.to_excel(excel, index=False, sheet_name="Sales")
    excel.close()
    with open("sales_data.xlsx", "rb") as f:
        st.download_button(
            label="📥 Download Excel",
            data=f,
            file_name="sales_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

