# init_db.py
import pandas as pd
from datetime import date
from models import init_db, Sale, SessionLocal

def seed_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    # Normalize column names (lowercase, strip spaces)
    df.columns = [c.strip().lower() for c in df.columns]

    session = SessionLocal()

    records = []
    for _, row in df.iterrows():
        od = pd.to_datetime(row['order date'], errors='coerce',dayfirst=True)
        od = od.date() if not pd.isna(od) else date.today()
        records.append(Sale(
            order_date=od,
            region=str(row['region']),
            category=str(row['category']),
            sales=float(row['sales']) if not pd.isna(row['sales']) else 0.0
        ))

    session.bulk_save_objects(records)
    session.commit()
    session.close()
    print(f"Inserted {len(records)} records from {csv_path}")

if __name__ == "__main__":
    init_db()
    csv_path = "superstore.csv"  # your CSV file
    seed_from_csv(csv_path)
