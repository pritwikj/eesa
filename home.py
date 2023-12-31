import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx
import sqlite3
from datetime import datetime
import time
from task_prioritization import *
import threading


# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Create the tasks table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_email TEXT,
            task_list TEXT,
            timestamp DATETIME
        )
    ''')

    conn.commit()
    conn.close()
    

# Function to add or update a master task list for a client in the database
def add_or_update_master_task_list(client_name, client_email, task_list):
    conn = sqlite3.connect('task_database.db')
    c = conn.cursor()

    # Check if the client exists in the database
    c.execute('SELECT * FROM tasks WHERE client_name = ?', (client_name,))
    existing_client = c.fetchone()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if existing_client:
        # Update the existing client's task list and timestamp
        c.execute('''
            UPDATE tasks
            SET task_list = ?,
                timestamp = ?
            WHERE client_name = ?
        ''', (task_list, timestamp, client_name))
    else:
        # Insert the new client and their task list
        c.execute('''
            INSERT INTO tasks (client_name, client_email, task_list, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (client_name, client_email, task_list, timestamp))

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

# Not used currently but may be in the future
# def contract_helper(client_name, client_email):
#     master_task_list = ''
#     placeholder_c = st.empty()
#     with st.spinner(f"Processing contract for {client_name}... Do not exit page"):
#         preclean = prioritize_tasks(contract_extract())
#         master_task_list += clean_list(preclean)
#     placeholder_c.info("Contract processed!")
#     time.sleep(2)
#     placeholder_c.empty()

#     # Add the master task list to the database
#     add_or_update_master_task_list(client_name, client_email, master_task_list)
    

def email_helper(history_id, client_email):
    email_data = getlatestEmail(history_id, client_email)
    if email_data is not None:
        email_tasks = clean_list(email_extract(email_data))
        return email_tasks
    else:
        return None

def pull_emails(history_id, client_name, client_email, master_task_list):
    email_tasks = email_helper(history_id, client_email)
    if email_tasks is not None:
        master_task_list2 = clean_list(update_master_tasks(master_task_list, email_tasks)) 
        add_or_update_master_task_list(client_name, client_email, master_task_list2)
    else:
        pass


def pull_calls(client_name, client_email, master_task_list):
    call_data = ""
    call_tasks = call_extract() #put call_data as parameter once transcript data is available
    master_task_list2 = clean_list(update_master_tasks(master_task_list, call_tasks)) 
    add_or_update_master_task_list(client_name, client_email, master_task_list2)



def main():
    conn = sqlite3.connect('task_database.db')
    initialize_database()

    # Get the existing clients from the database
    existing_clients = set()
    c = conn.cursor()
    c.execute('SELECT DISTINCT client_name FROM tasks')
    result = c.fetchall()
    existing_clients.update(client[0] for client in result)
    
    # Get the existing email addresses from the database
    existing_emails = set()
    c.execute('SELECT DISTINCT client_email FROM tasks')
    result = c.fetchall()
    existing_emails.update(email[0] for email in result)
    

    # Streamlit interface for adding a new client
    if 'new_client' not in st.session_state:
        st.session_state.new_client = ''

    def submit_client():
        st.session_state.new_client = st.session_state.c_widget
        st.session_state.c_widget = ''
    
    if 'new_email' not in st.session_state:
        st.session_state.new_email = ''

    def submit_email():
        st.session_state.new_email = st.session_state.e_widget
        st.session_state.e_widget = ''

    st.sidebar.text_input("Add a new client:", key='c_widget', on_change=submit_client)
    new_client = st.session_state.new_client
    
    st.sidebar.text_input("Add the client's email:", key='e_widget', on_change=submit_email)
    client_email = st.session_state.new_email




    if new_client != "" and new_client not in existing_clients and client_email != "" and client_email not in existing_emails:
        placeholder_add = st.empty()
        placeholder_add.info(f"Added new client: {new_client}")
        time.sleep(2)
        placeholder_add.empty()
        existing_clients.add(new_client)
        existing_emails.add(client_email)

        # Start a background thread for the new client
        background_thread = threading.Thread(target=background_task, args=(new_client, client_email,))
        add_script_run_ctx(background_thread)
        background_thread.start()

    clients = st.sidebar.selectbox("Select a client", list(existing_clients), index=0)

    if clients == None:
        st.write("Start adding your clients on the left side!")
    else:
        if 'title' in st.session_state:
            st.session_state['title'].empty()
        else:
            st.session_state['title'] = st.empty()

        st.session_state['title'].title("Client: " + clients)

        if 'placeholder' in st.session_state:
            st.session_state['placeholder'].empty()
        else:
            st.session_state['placeholder'] = st.empty()

        st.session_state['placeholder'].empty()
        
        retrieved_task_list = get_master_task_list(clients)
        if retrieved_task_list is None:
            #contract_helper(clients, client_email)
            #time.sleep(5)
            add_or_update_master_task_list(clients, client_email, "No tasks yet")
        
        while True:
            retrieved_task_list = get_master_task_list(clients)

            st.session_state['placeholder'].empty()
            st.session_state['placeholder'].write(retrieved_task_list)
            time.sleep(5)




# Background task to update the client's task list
def background_task(client_name, client_email):
    watch_response = getwatchResponse()
    history_id = watch_response['historyId']
    while True:
        retrieved_task_list = get_master_task_list(client_name)

        if retrieved_task_list is not None:
            pull_emails(history_id, client_name, client_email, retrieved_task_list)
            #retrieved_task_list = get_master_task_list(client_name)
            #pull_calls(client_name, client_email, retrieved_task_list)
            watch_response = getwatchResponse()
            history_id = watch_response['historyId']

        time.sleep(5)




if __name__ == '__main__':
    main()