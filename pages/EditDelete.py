# EditDelete.py
import streamlit as st
import pandas as pd
from models import Sale, SessionLocal, init_db

init_db()
st.set_page_config(page_title="✏️ Edit & Delete", layout="wide")

if st.button("⬅️ Back to Dashboard"):
    st.switch_page("Home.py")


def fetch():
    s=SessionLocal();rows=s.query(Sale).order_by(Sale.id).all();s.close()
    return pd.DataFrame([{"id":r.id,"order_date":r.order_date,"region":r.region,"category":r.category,"sales":r.sales} for r in rows])

def delete_sale(ids):
    s=SessionLocal()
    for rid in ids:
        row=s.query(Sale).filter(Sale.id==rid).first()
        if row: s.delete(row)
    s.commit();s.close()

def update_sale(rid,od,reg,cat,sales):
    s=SessionLocal();row=s.query(Sale).filter(Sale.id==rid).first()
    if row:
        row.order_date=od;row.region=reg;row.category=cat;row.sales=sales
        s.commit();s.close();return True
    s.close();return False

df=fetch()
st.title("✏️ Edit / 🗑️ Delete Sales")

if df.empty:
    st.info("No records yet.")
else:
    # --- Delete ---
    st.subheader("🗑️ Delete Records")
    opts = df.apply(lambda r: f"{r['id']}: {r['order_date']} — {r['region']} — {r['category']} — ${r['sales']:,.2f}",axis=1).tolist()
    selected = st.multiselect("Select to delete",opts)
    if st.button("Delete Selected"):
        ids = [int(x.split(":")[0]) for x in selected]
        delete_sale(ids)
        st.success(f"Deleted {len(ids)} record(s).")
        st.rerun()

    st.markdown("---")
    # --- Edit ---
    st.subheader("✏️ Edit Record")
    search = st.text_input("🔍 Search (Region/Category)")
    df2 = df[df["region"].str.contains(search,case=False,na=False)|df["category"].str.contains(search,case=False,na=False)] if search else df
    if df2.empty:
        st.warning("No matches.")
    else:
        opts2 = df2.apply(lambda r: f"{r['id']} — {r['region']} — {r['category']} — ${r['sales']:,.2f}",axis=1).tolist()
        sel = st.selectbox("Select record",[""]+opts2)
        if sel:
            rid=int(sel.split("—")[0].strip())
            row=df[df.id==rid].iloc[0]
            with st.form("edit_form"):
                od=st.date_input("Order Date",value=pd.to_datetime(row.order_date))
                reg=st.text_input("Region",value=row.region)
                cat=st.text_input("Category",value=row.category)
                amt=st.number_input("Sales",min_value=0.0,value=float(row.sales),step=1.0)
                sub=st.form_submit_button("Update")
                if sub:
                    if update_sale(rid,od,reg,cat,float(amt)):
                        st.success(f"Updated record {rid}")
                        st.rerun()
