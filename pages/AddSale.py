# AddSale.py
import streamlit as st
from datetime import date
from models import Sale, SessionLocal, init_db

init_db()
st.set_page_config(page_title="➕ Add Sale", layout="centered")

if st.button("⬅️ Back to Dashboard"):
    st.switch_page("Home.py")

def add_sale(order_date, region, category, sales):
    s = SessionLocal()
    new = Sale(order_date=order_date, region=region, category=category, sales=sales)
    s.add(new)
    s.commit()
    new_id = new.id
    s.close()
    return new_id

st.title("➕ Add New Sale")
with st.form("add_form"):
    od = st.date_input("Order Date", value=date.today())
    reg = st.text_input("Region")
    cat = st.text_input("Category")
    amt = st.number_input("Sales", min_value=0.0, step=1.0)
    sub = st.form_submit_button("Add Record")
    if sub:
        rid = add_sale(od,reg,cat,float(amt))
        st.success(f"✅ Added record with ID {rid}")
        st.rerun()
