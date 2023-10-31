import streamlit as st
#from task_prioritization import streamlit_test, streamlit_main
from task_prioritization import *


st.title("Eesa Prototype")
         

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


# def streamlist_test():
#     watch_response = getwatchResponse()
#     history_id = watch_response['historyId'] #Initializing history_id

#     while True:
#         email_data = getlatestEmail(history_id)

#         # Generate the updated value based on the current value
#         watch_response = getwatchResponse()
#         history_id = watch_response['historyId']
#         if email_data == None:
#             pass
#         else:
#             print("Processing...")
#             email_tasks = clean_list(email_extract(email_data))
#             st.info(email_tasks)

#         # Wait for 10 seconds   
#         time.sleep(10)



streamlit_main()
#streamlist_test()