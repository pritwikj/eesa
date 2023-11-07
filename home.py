import streamlit as st
from task_prioritization import *

class Client:
    def __init__(self, name, email_address):
        self.name = name
        self.email_address = email_address

    def email_helper(_self, history_id, client_email):
        email_data = getlatestEmail(history_id, client_email)
        # Generate the updated value based on the current value
        watch_response = getwatchResponse()
        history_id = watch_response['historyId']

        if email_data != None:
            st.write("Processing pt.2...")
            email_tasks = clean_list(email_extract(email_data))
            st.info(email_tasks)
            return email_tasks
   

    def streamlit_test(_self):
        st.write(_self.name)
        st.write(_self.email_address)
        varchar = 0
        while varchar < 10:
            st.session_state['master_tasks'][_self.name] = "print test"
            st.info(st.session_state['master_tasks'][_self.name])
            varchar += 1
            time.sleep(5)


    #@st.cache_data(show_spinner=False)
    def contract_helper(_self):
        master_task_list = ''
        placeholder = st.empty()
        with st.spinner("Processing contract... Do not exit page"):
            preclean = prioritize_tasks(contract_extract())
            master_task_list += clean_list(preclean)
        placeholder.info("Contract processed!")
        time.sleep(1)
        placeholder.empty()
        return master_task_list



    #@st.cache_data
    def streamlit_test2(_self):
        # st.write(_self.name)
        # st.write(_self.email_address)

        client_email = _self.email_address

        if st.session_state['master_tasks'][_self.name] == 'No tasks yet':
            st.write("empty list")
            master_task_list = _self.contract_helper()
            st.session_state['master_tasks'][_self.name] = master_task_list
        else:
            master_task_list = st.session_state['master_tasks'][_self.name]

        watch_response = getwatchResponse()
        history_id = watch_response['historyId'] #Initializing history_id
        

        while True:
            email_tasks = _self.email_helper(history_id, client_email)
            
            # Generate the updated value based on the current value
            watch_response = getwatchResponse()
            history_id = watch_response['historyId']
            
            if email_tasks == None:
                master_task_list2 = master_task_list
            else:
                st.write("Processing pt.3...")
                master_task_list2 = clean_list(update_master_tasks(master_task_list, email_tasks))

            if master_task_list2 != master_task_list:
                st.session_state['master_tasks'][_self.name] = master_task_list2
                st.info(st.session_state['master_tasks'][_self.name])

                master_task_list = master_task_list2
            else:
                pass

        
            # Wait for 10 seconds
            time.sleep(10)






st.title("Eesa")
if 'clients' not in st.session_state:
    st.session_state['dropdown'] = ["Overview"]
    st.session_state['clients'] = {}
    st.session_state['master_tasks'] = {}
    

client_select = st.sidebar.selectbox("Select a client to display tasks for", st.session_state['dropdown'])


if client_select != "Overview":
    if st.session_state['master_tasks'][client_select] == '':
        st.session_state['master_tasks'][client_select] = "No tasks yet"

    st.info(st.session_state['master_tasks'][client_select])

    st.session_state['clients'][client_select].streamlit_test2()

else:
    st.info("Start adding your clients in the settings page!")













def streamlit_main():
    client_email= st.text_input("Input your client's email address here:")
    st.write("Processing...")
    master_task_list = ''
    preclean = prioritize_tasks(contract_extract())
    master_task_list += clean_list(preclean)


    watch_response = getwatchResponse()
    history_id = watch_response['historyId'] #Initializing history_id

    st.info(master_task_list)

    while True:
        email_data = getlatestEmail(history_id, client_email)
        # Generate the updated value based on the current value
        watch_response = getwatchResponse()
        history_id = watch_response['historyId']
        
        if email_data == None:
            master_task_list2 = master_task_list
        else:
            st.write("Processing pt.2...")
            email_tasks = clean_list(email_extract(email_data))
            st.info(email_tasks)
            st.write("Processing pt.3...")
            master_task_list2 = clean_list(update_master_tasks(master_task_list, email_tasks))

        if master_task_list2 != master_task_list:
            st.info(master_task_list2)
            master_task_list = master_task_list2

        else:   
            pass
        # Wait for 10 seconds
        time.sleep(10)






