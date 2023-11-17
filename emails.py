# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
import re

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

# get watch response (current email history timestamp)
def getwatchResponse():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists.
    if os.path.exists('token.pickle'):
        # Read the token from the file and store it in the variable creds.
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # Set up a watch on the user's mailbox for new messages
    request = {
        "labelIds": ["INBOX"],
        "topicName": "projects/eesa-402505/topics/MyTopic"
    }
    watch_response = service.users().watch(userId='me', body=request).execute()
    
    # You'll need to set up a Pub/Sub topic in Google Cloud and replace the placeholders
    # {your-project-id} and {your-topic-name} with your actual project ID and topic name.

    return watch_response


# Extract emails after a certain timestamp and from one specific client
def getlatestEmail(start_history_id, client_email):
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists.
    if os.path.exists('token.pickle'):
        # Read the token from the file and store it in the variable creds.
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    
    #user_info = service.users().getProfile(userId='me').execute()


    history_list_response = service.users().history().list(userId='me', historyTypes=['messageAdded'], labelId='INBOX', startHistoryId=start_history_id).execute()
    email_data = ""
    #print(history_list_response)
    # Process the history list response to get information about new messages
    if history_list_response.get('history', []) == []:
        return
    for history in history_list_response.get('history', []):
        for message_added in history.get('messagesAdded', []):
            message_id = message_added['message']['id']

            # Retrieve the message details using users().messages().get
            txt = service.users().messages().get(userId='me', id=message_id).execute()

            try:
                payload = txt['payload'] 
                headers = payload['headers'] 

                # Look for Subject and Sender Email in the headers 
                for d in headers: 
                    if d['name'] == 'Subject': 
                        subject = d['value'] 
                    if d['name'] == 'From': 
                        sender = d['value']
    

                email_addy = r'<(.*?)>'
                match = re.search(email_addy, sender)
                if match:
                    email_address = match.group(1)
                else:
                    email_address = "No email address found in the given text."				

                if email_address == client_email:
                # The Body of the message is in Encrypted format. So, we have to decode it. 
                # Get the data and decode it with base 64 decoder. 
                    parts = payload.get('parts')[0] 
                    data = parts['body']['data'] 
                    data = data.replace("-","+").replace("_","/") 
                    decoded_data = base64.b64decode(data) 
                    body = decoded_data.decode("utf-8")

                    #email_data += f"Subject: {subject}\nFrom: {email_address}\nMessage: {body}\n\n"	
                    email_data += f"Subject: {subject}\nMessage: {body}\n\n"	

                else:
                    return
            except: 
                pass

    return email_data 


