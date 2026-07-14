
import streamlit as st
import pandas as pd
import pymysql

st.set_page_config(page_title="Customer CRM", page_icon="📊", layout="wide")

# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Deepanshu@123",   # Change this
        database="crm_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# -----------------------------
# CRUD Functions
# -----------------------------
# Add Customer
def add_customer_db(customer_id, name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    INSERT INTO customers (id, name, email, phone)
    VALUES ('{customer_id}', '{name}', '{email}', '{phone}')
    """

    cursor.execute(query)
    conn.commit()
    conn.close()

# View Customers
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT *FROM customers """
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data


# Search Customer
def search_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    SELECT *
    FROM customers
    WHERE id = '{customer_id}'
    """

    cursor.execute(query)
    customer = cursor.fetchone()

    conn.close()
    return customer

# Update Customer
def update_customer_db(customer_id, name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    UPDATE customers
    SET
        name = '{name}',
        email = '{email}',
        phone = '{phone}'
    WHERE id = '{customer_id}'
    """

    cursor.execute(query)
    conn.commit()
    conn.close()



# Delete Customer
def delete_customer_db(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    DELETE FROM customers
    WHERE id = '{customer_id}'
    """

    cursor.execute(query)
    conn.commit()
    conn.close()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📊 CRM System")
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard","➕ Add Customer","📋 View Customers","🔍 Search Customer","✏ Update Customer","🗑 Delete Customer"]
)

# -----------------------------
# Dashboard
# -----------------------------
if menu == "🏠 Dashboard":
    st.title("📊 Customer CRM")
    customers = get_customers()
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Customers", len(customers))
    c2.metric("Active Users", len(customers))
    c3.metric("Database","MySQL")
    st.divider()
    if customers:
        st.dataframe(pd.DataFrame(customers), use_container_width=True)
    else:
        st.info("No customer data available.")

# -----------------------------
# Add Customer
# -----------------------------
elif menu == "➕ Add Customer":
    st.title("➕ Add Customer")
    with st.form("add", clear_on_submit=True):
        cid = st.text_input("Customer ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        submit = st.form_submit_button("Add Customer")
        if submit:
            try:
                add_customer_db(cid,name,email,phone)
                st.success("Customer Added Successfully!")
            except pymysql.err.IntegrityError:
                st.error("Customer ID already exists!")
            except Exception as e:
                st.error(str(e))

# -----------------------------
# View Customers
# -----------------------------
elif menu == "📋 View Customers":
    st.title("📋 Customer List")
    customers = get_customers()
    if customers:
        st.dataframe(pd.DataFrame(customers), use_container_width=True, hide_index=True)
    else:
        st.warning("No Customers Found.")

# -----------------------------
# Search Customer
# -----------------------------
elif menu == "🔍 Search Customer":
    st.title("🔍 Search Customer")
    cid = st.text_input("Customer ID")
    if st.button("Search"):
        customer = search_customer(cid)
        if customer:
            st.success("Customer Found")
            st.json(customer)
        else:
            st.error("Customer Not Found.")

# -----------------------------
# Update Customer
# -----------------------------
elif menu == "✏ Update Customer":
    st.title("✏ Update Customer")
    cid = st.text_input("Customer ID")
    if cid:
        customer = search_customer(cid)
        if customer:
            name = st.text_input("Name", customer["name"])
            email = st.text_input("Email", customer["email"])
            phone = st.text_input("Phone", customer["phone"])
            if st.button("Update"):
                update_customer_db(cid,name,email,phone)
                st.success("Customer Updated Successfully!")
        else:
            st.error("Customer Not Found.")

# -----------------------------
# Delete Customer
# -----------------------------
elif menu == "🗑 Delete Customer":
    st.title("🗑 Delete Customer")
    cid = st.text_input("Customer ID")
    if st.button("Delete"):
        if search_customer(cid):
            delete_customer_db(cid)
            st.success("Customer Deleted Successfully!")
        else:
            st.error("Customer Not Found.")
