import streamlit as st
from task_prioritization import *
import home


client_name = st.text_input("Input your client's name here:")
client_email = st.text_input("Input your client's email here:")

if client_email != '':
    st.session_state['clients'][client_name] = home.Client(client_name, client_email)
    st.session_state['master_tasks'][client_name] = ''
    if client_name not in st.session_state['dropdown']:
        st.session_state['dropdown'].append(client_name)
