import streamlit as st
from task_prioritization import *


class Client:
    def __init__(self, name, email_address):
        self.name = name
        self.email_address = email_address
    
    def streamlit_test(self):
        st.write(self.name)
        st.write(self.email_address)


        watch_response = getwatchResponse()
        history_id = watch_response['historyId'] #Initializing history_id

        while True:
            email_data = getlatestEmail(history_id, client_email)
            # Generate the updated value based on the current value
            watch_response = getwatchResponse()
            history_id = watch_response['historyId']
            
            if email_data == None:
                pass
            else:
                st.write("Processing pt.2...")
                email_tasks = clean_list(email_extract(email_data))
                st.info(email_tasks)
                # st.write("Processing pt.3...")
                # master_task_list2 = clean_list(update_master_tasks(master_task_list, email_tasks))

            # Wait for 10 seconds
            time.sleep(10)
    def streamlit_test2(self):
        st.write(self.name)
        st.write(self.email_address)


client_name = st.text_input("Input your client's name here:")
client_email = st.text_input("Input your client's email here:")

if client_email != '':
    st.session_state['clients'][client_name] = Client(client_name, client_email)
    st.session_state['dropdown'].append(client_name)