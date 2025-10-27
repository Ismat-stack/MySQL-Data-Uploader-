## 📊 MySQL Data Uploader (Streamlit App)

A simple Streamlit web application that lets you upload CSV or Excel files directly into a MySQL database.
You can connect to your database, preview your data, and upload it into an existing table — or let the app automatically create a new one.

## 🚀 Features

✅ Connect securely to a MySQL database

✅ Upload CSV or Excel files

✅ Automatically create new tables (if they don’t exist)

✅ Preview your data before uploading

✅ Bulk-insert data into MySQL using executemany()

✅ Easy to deploy and use


## 🧰 Technologies Used

Streamlit
 – Web UI framework

Pandas
 – Data handling

MySQL Connector for Python
 – MySQL connection

## 📦 Install the required dependencies

pip install streamlit

pip install pandas

pip install mysql-connector-python

pip install openpyxl

## ▶️ Run the App

Once dependencies are installed, start the Streamlit app with:
streamlit run mysql_connector.py
Then open your browser at http://localhost:8501

## ⚙️ How to Use

Enter MySQL Connection Details
Host (e.g., localhost or 127.0.0.1)

MySQL Username & Password

Database Name

Upload Your File

Supported file types: .csv or .xlsx

The app reads and previews your data automatically.

Choose Table Name

Specify an existing table or a new one (it will be created if it doesn’t exist).

Upload Data

Click ⬆️ Upload Data to MySQL

The app inserts all records into the specified table.

## 🗄️ Database Table Creation Logic

If the target table doesn’t exist, the app automatically creates one with:

id (auto-increment primary key)

All other columns as TEXT type (for flexible imports)

You can modify the column data types later in MySQL if needed.

## 🧠 Example

Uploading a CSV file named sales_data.csv with the following columns:

Date	Product	Quantity	Price

2024-01-01	Widget A	10	19.99

2024-01-02	Widget B	5	9.99

Will create a MySQL table like:

CREATE TABLE uploaded_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` TEXT,
    `Product` TEXT,
    `Quantity` TEXT,
    `Price` TEXT
);

# 🧩 Customization

Change default table name: modify the value parameter in
table_name = st.text_input("Enter table name to upload data into:", value="uploaded_data")

Adjust column data types in the CREATE TABLE query.

Add validation or transformation logic before uploading.

## 🐞 Troubleshooting

Authentication failed: Check MySQL username/password.

Connection refused: Ensure your MySQL server is running.

Permission denied: User might not have CREATE or INSERT privileges.

Excel file not uploading: Make sure openpyxl is installed.

## 📜 License
This project is licensed under the MIT License — feel free to use, modify, and share.

## 💡 Author
Khan Ismat 

Your Name
📧 [your.email@example.com
]
