import streamlit as st
import sqlite3
from datetime import datetime
import time
from task_prioritization import *


# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('task_database.db')
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
    conn.close()

# Function to add a master task list for a client to the database
def add_master_task_list(client_name, task_list):
    conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Insert the task list into the database with the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO tasks (client_name, task_list, timestamp) VALUES (?, ?, ?)', (client_name, task_list, timestamp))

    conn.commit()
    conn.close()

# Function to update the master task list for a client in the database
def update_master_task_list(client_name, new_task_list):
    conn = sqlite3.connect('task_database.db')
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
    conn.close()

# Function to get the master task list for a client from the database
def get_master_task_list(client_name):
    conn = sqlite3.connect('task_database.db')
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

    conn.close()

    return result[0] if result else None

@st.cache_data(show_spinner=False)
def contract_helper():
    client_name = "Test 1"
    master_task_list = ''
    placeholder = st.empty()
    with st.spinner("Processing contract... Do not exit page"):
        preclean = prioritize_tasks(contract_extract())
        master_task_list += clean_list(preclean)
    placeholder.info("Contract processed!")
    time.sleep(1)
    placeholder.empty()

    # Add the master task list to the database
    add_master_task_list(client_name, master_task_list)

    #return master_task_list

def email_helper(history_id, client_email):
    email_data = getlatestEmail(history_id, client_email)
    # Generate the updated value based on the current value
    # watch_response = getwatchResponse()
    # history_id = watch_response['historyId']

    if email_data != None:
        st.write("Processing pt.2...")
        email_tasks = clean_list(email_extract(email_data))
        return email_tasks
    
def pull_emails(history_id, master_task_list):
    email_address = "pritwik@skoruz.com"
    client_name = "Test 1"
    client_email = email_address
    email_tasks = email_helper(history_id, client_email)

    
    # # Generate the updated value based on the current value
    # watch_response = getwatchResponse()
    # history_id = watch_response['historyId']
    
    if email_tasks == None:
        master_task_list2 = master_task_list
    else:
        st.write("Processing pt.3...")
        master_task_list2 = clean_list(update_master_tasks(master_task_list, email_tasks))

    if master_task_list2 != master_task_list:
        update_master_task_list(client_name, master_task_list2)
        master_task_list = master_task_list2
    else:
        pass

# Function to run the main application
def main():
    initialize_database()    

    retrieved_task_list = get_master_task_list("Test 1")
    if retrieved_task_list is None:
        contract_helper()
    st.write(retrieved_task_list)


    placeholder = st.empty()
    watch_response = getwatchResponse()
    history_id = watch_response['historyId']
    while True:
        pull_emails(history_id, retrieved_task_list)

        # Retrieve and display the master task list from the database
        retrieved_task_list = get_master_task_list("Test 1")
        placeholder.empty()
        placeholder.write(retrieved_task_list)
        watch_response = getwatchResponse()
        history_id = watch_response['historyId']
        time.sleep(10)

if __name__ == '__main__':    
    main()
