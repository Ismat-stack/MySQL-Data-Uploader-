import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- Streamlit Page Config ---
st.set_page_config(page_title="MySQL Data Uploader", page_icon="📊", layout="wide")

st.title("📊 Upload CSV or Excel Data into MySQL Database")

st.write("""
This app allows you to connect to your **MySQL database** and upload data from a CSV or Excel file 
into an existing table (or create a new one automatically).
""")

# --- Step 1: MySQL Connection Form ---
st.subheader("🔐 Enter MySQL Connection Details")

with st.form("db_connection_form"):
    host = st.text_input("Host (e.g. localhost or 127.0.0.1)")
    user = st.text_input("MySQL Username")
    password = st.text_input("MySQL Password", type="password")
    database = st.text_input("Database Name")
    connect_button = st.form_submit_button("🔗 Connect to Database")

# --- Step 2: Connect to Database ---
if connect_button:
    if not host or not user or not password or not database:
        st.error("⚠️ Please fill in all connection details.")
    else:
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if conn.is_connected():
                st.success(f"✅ Connected successfully to `{database}`!")
                st.session_state["db_conn"] = {
                    "host": host,
                    "user": user,
                    "password": password,
                    "database": database
                }
                conn.close()
        except Error as e:
            st.error(f"❌ Connection failed: {e}")

# --- Step 3: Upload CSV or Excel File ---
if "db_conn" in st.session_state:
    st.subheader("📁 Upload CSV or Excel File")

    uploaded_file = st.file_uploader("Choose your CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_name = uploaded_file.name

        # Read file with Pandas
        try:
            if file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")
            df = None

        if df is not None:
            st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns.")
            st.dataframe(df.head(10))

            table_name = st.text_input("Enter table name to upload data into:", value="uploaded_data")

            if st.button("⬆️ Upload Data to MySQL"):
                config = st.session_state["db_conn"]
                try:
                    conn = mysql.connector.connect(**config)
                    cursor = conn.cursor()

                    # Dynamically create table if it doesn't exist
                    cols = ", ".join([f"`{col}` TEXT" for col in df.columns])
                    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (id INT AUTO_INCREMENT PRIMARY KEY, {cols})"
                    cursor.execute(create_table_query)

                    # Prepare insert query dynamically
                    placeholders = ", ".join(["%s"] * len(df.columns))
                    insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{c}`' for c in df.columns])}) VALUES ({placeholders})"

                    # Convert all rows to list of tuples
                    data = [tuple(str(x) if pd.notna(x) else None for x in row) for row in df.values]

                    cursor.executemany(insert_query, data)
                    conn.commit()

                    st.success(f"✅ Successfully uploaded {cursor.rowcount} records to `{table_name}`!")

                    cursor.close()
                    conn.close()
                except Error as e:
                    st.error(f"❌ Database error: {e}")
                except Exception as e:
                    st.error(f"⚠️ Unexpected error: {e}")
