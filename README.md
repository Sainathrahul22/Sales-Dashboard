📊 Superstore Sales Dashboard

An interactive data analytics dashboard built with Streamlit, Plotly, and SQLAlchemy for exploring and managing Superstore sales data.

✨ Features

✅ Interactive Dashboard – Key metrics & visualizations (bar, pie, line charts)
✅ Smart Filters – Filter by region, category, date range, or search keywords
✅ Data Management (CRUD) – Add, edit, and delete sales records
✅ Download Options – Export filtered data as CSV or Excel
✅ Multi-Page Navigation – Clean and organized page-based app
✅ Real-Time Updates – Every change reflects instantly across all pages

⚙️ Tech Stack

Frontend/UI: Streamlit

Visualizations: Plotly

Database: SQLite with SQLAlchemy ORM

Data Handling: Pandas

🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/Sainathrahul22/Sales-Dashboard
cd superstore-sales-dashboard

2️⃣ Create a Virtual Environment
python -m venv sales_env
source sales_env/bin/activate   # On Mac/Linux
sales_env\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the App
streamlit run Home.py

📂 Project Structure
superstore-sales-dashboard/
│── Home.py               # Main dashboard page
│── models.py             # Database models & session
│── sales.db              # SQLite database
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
│
└── pages/                # Multi-page app
    │── AddSale.py        # Add sales record
    │── EditDelete.py     # Edit/Delete records
    │── Download.py       # Download filtered data

📌 Future Enhancements

🔐 User authentication (role-based access)

📊 More advanced analytics (forecasting, clustering, etc.)

☁️ Cloud deployment (Streamlit Cloud / Heroku / AWS)

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork this repo and submit a pull request.

📜 License

This project is licensed under the MIT License – you’re free to use and modify it.