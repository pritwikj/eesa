import streamlit as st
import sqlite3
from datetime import datetime
import time
from task_prioritization import *
import threading


# Function to initialize the database
def initialize_database(conn):
    #conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Create the tasks table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            task_list TEXT,
            timestamp DATETIME
        )
    ''')

    conn.commit()
    #conn.close()

# Function to add a master task list for a client to the database
def add_master_task_list(client_name, task_list, conn):
    #conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Insert the task list into the database with the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO tasks (client_name, task_list, timestamp) VALUES (?, ?, ?)', (client_name, task_list, timestamp))

    conn.commit()
    #conn.close()

# Function to update the master task list for a client in the database
def update_master_task_list(client_name, new_task_list, conn):
    #conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Update the task_list for the given client
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''
        UPDATE tasks
        SET task_list = ?,
            timestamp = ?
        WHERE client_name = ?
    ''', (new_task_list, timestamp, client_name))

    conn.commit()
    #conn.close()

# Function to get the master task list for a client from the database
def get_master_task_list(client_name, conn):
    #conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Select the latest task list for the given client
    c.execute('''
        SELECT task_list
        FROM tasks
        WHERE client_name = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (client_name,))
    
    result = c.fetchone()

    #conn.close()

    return result[0] if result else None



#@st.cache_data(show_spinner=False)
def contract_helper(client_name, conn):
    master_task_list = ''
    placeholder = st.empty()
    with st.spinner(f"Processing contract for {client_name}... Do not exit page"):
        preclean = prioritize_tasks(contract_extract())
        master_task_list += clean_list(preclean)
    placeholder.info("Contract processed!")
    time.sleep(1)
    placeholder.empty()

    # Add the master task list to the database
    add_master_task_list(client_name, master_task_list, conn)
    

def email_helper(history_id):
    client_email = "pritwik@skoruz.com"
    email_data = getlatestEmail(history_id, client_email)
    if email_data is not None:
        st.write(f"Processing emails pt.2...")
        email_tasks = clean_list(email_extract(email_data))
        return email_tasks
    return None

def pull_emails(history_id, client_name, master_task_list, conn):
    email_tasks = email_helper(history_id)

    if email_tasks is None:
        master_task_list2 = master_task_list
    else:
        st.write(f"Processing emails pt.3...")
        master_task_list2 = clean_list(update_master_tasks(master_task_list, email_tasks))

    if master_task_list2 != master_task_list:
        update_master_task_list(client_name, master_task_list2, conn)
        master_task_list = master_task_list2
    else:
        pass



# Function to run the main application
def main():    
    conn = sqlite3.connect('task_database.db')

    initialize_database(conn)

    # Get the existing clients from the database
    existing_clients = set()
    c = conn.cursor()
    c.execute('SELECT DISTINCT client_name FROM tasks')
    result = c.fetchall()
    existing_clients.update(client[0] for client in result)
    #conn.close()

    # Streamlit interface for adding a new client
    new_client = st.text_input("Add a new client:")
    if new_client not in existing_clients:
        st.write(f"Added new client: {new_client}")
        existing_clients.add(new_client)

    clients = st.selectbox("Select a client", list(existing_clients), index=0)

    if clients == "":
        st.write("Start adding your clients in the settings page!")
    else:
        retrieved_task_list = get_master_task_list(clients, conn)
        if retrieved_task_list is None:
            contract_helper(clients, conn)

        placeholder = st.empty()
        watch_response = getwatchResponse()
        history_id = watch_response['historyId']
        while True:
            pull_emails(history_id, clients, retrieved_task_list, conn)

            # Retrieve and display the master task list from the database
            retrieved_task_list = get_master_task_list(clients, conn)
            placeholder.empty()
            placeholder.write(retrieved_task_list)
            watch_response = getwatchResponse()
            history_id = watch_response['historyId']
            time.sleep(10)



if __name__ == '__main__':
    main()