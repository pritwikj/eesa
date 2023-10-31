import time
import openai
from emails import getwatchResponse, getlatestEmail

# Set up YOUR OpenAI API key
openai.api_key = "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"
# Set MODEL to "gpt-3.5-turbo"
model = "gpt-3.5-turbo" #try gpt4
# Set temperature
temperature = 0.1

#Extract tasks from emails and assign each of them an urgency score
def email_extract(content1): 
    message_list1 = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message = {"role": "system", "content": "You are a busy Customer Success manager at a startup and you deal with many clients"}

    message_list1.append(system_message)

    user_message = {"role": "user", "content": "Extract, in a concise unnumbered list, the relevant action task(s) that you have to do from this client's emails: " + content1 +\
    "You do not need to list obvious actions. If appropriate, consolidate similar tasks into one task. DO NOT add extra tasks. Based on the context of the email, assign a number between 1-10 for how urgent the task needs to be completed. Tasks that require immediate attention to the \
    customer's current operations should be given a higher score. Tasks that are for future plans (like feature requests) should be given lower scores. \
    Give reasoning for each score. Here is an example: -Schedule a discovery call with XYZ Corporation's key stakeholders to understand their specific \
    goals, challenges, and requirements (10). This task has a (10) at the end because it is of utmost importance."}

    message_list1.append(user_message)

    # Send the message to the bot
    response_message = openai.ChatCompletion.create(model=model, messages=message_list1, temperature=temperature)

    # Get the response from the bot
    response = response_message.choices[0].message.content

    return response


def call_extract(): 
    """Extract tasks from call transcripts and assign each of them an urgency score"""

    message_list2 = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message2 = {"role": "system", "content": "You are a busy Customer Success manager at a startup and you deal with many clients"}

    message_list2.append(system_message2)

    content2 = """Customer: Hi, this is John from ACME Inc. I hope I'm not catching you at a bad time?

    Customer Success Manager (CSM): Hi John, not at all! I'm always here to assist you. How can I help you today?

    Customer: Great to hear that. We've been using your software for a while now, and I have a few concerns that I'd like to discuss.

    CSM: Of course, John, I'm here to address any concerns you might have. Please feel free to share your thoughts.

    Customer: Well, first, we've noticed a few performance issues in the software, especially when we're running larger data sets. It's been affecting our team's efficiency.

    CSM: I'm sorry to hear that, John. Let me make a note of this issue. Can you provide more details about when and where you're experiencing these performance problems? Any specific tasks or modules that seem to be causing the slowdown?

    Customer: It mainly happens when we run data reports and perform data imports. It can be quite frustrating, especially during peak business hours.

    CSM: I appreciate you sharing that information. We take performance issues seriously, and I'll immediately escalate this to our technical team. They'll investigate the root cause and work on improving the software's performance. In the meantime, is there anything specific you'd like to do to mitigate this, or any urgent reports we can assist with?

    Customer: Thanks for your prompt response. Yes, we have some critical reports to run, and these delays are affecting our decision-making process. If we could get some assistance in optimizing these reports, that would be great.

    CSM: Absolutely, John. I'll arrange for our technical team to reach out to you within the next 24 hours to work on optimizing those reports. In the meantime, let's see if there are any quick fixes we can implement. Would you be available for a screen-sharing session later today to go through the reports in more detail?

    Customer: That works for me. Also, we've recently hired a few new team members, and it's been a bit challenging for them to get up to speed with your software. Do you have any training materials or resources that could help with onboarding?

    CSM: We certainly do, John. I can provide you with access to our comprehensive onboarding materials, including video tutorials and user guides. Additionally, we can set up a dedicated training session for your new team members. Would you like me to send over those resources and schedule a training session?

    Customer: That would be fantastic. Thanks for being so responsive, and it's reassuring to know you're taking our concerns seriously.

    CSM: You're very welcome, John. We highly value your feedback and are committed to ensuring that your experience with our software is as smooth as possible. Is there anything else you'd like to discuss today, or any other concerns on your mind?

    Customer: No, that's it for now. Thanks for your help. I appreciate it.

    CSM: It's been a pleasure assisting you, John. If you ever have more questions or concerns, don't hesitate to reach out. Have a great day!"""

    user_message2 = {"role": "user", "content": "This is a transcript of a meeting you had with a client: " + content2 + "\n \n Extract, in an unnumbered \
    list, the 3 main relevant specific task(s) that you have to do from this transcript. Based on the context of the transcript, assign a number between 1-10 for how urgent \
    the task needs to be completed. Tasks that require immediate attention to the customer's current operations should be given a higher score. Tasks that are \
    for future plans (like feature requests) should be given lower scores. Give reasoning for each score. Here is an example: -Schedule a discovery call with XYZ \
    Corporation's key stakeholders to understand their specific goals, challenges, and requirements (10). This task has a (10) at the end because it is of utmost importance."}

    message_list2.append(user_message2)

    # Send the message to the bot
    response_message2 = openai.ChatCompletion.create(model=model, messages=message_list2, temperature=temperature)

    # Get the response from the bot
    response2 = response_message2.choices[0].message.content

    return response2


def support_extract():
    """Extract tasks from support tickets and assign each of them an urgency score"""

    message_list3 = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message3 = {"role": "system", "content": "You are a busy Customer Success manager at a startup and you deal with many clients"}

    message_list3.append(system_message3)

    content3 = """
    Subject: Urgent: Issue with Account Access

    Ticket ID: #12345
    Priority: High

    Hello,

    I hope this message finds you well. My name is Adam from ACME Inc., and I am a user of your platform. I have been experiencing some issues with accessing my account, and I'm in need of your assistance urgently.

    Details of the issue:

    I am unable to log in to my account.
    Whenever I attempt to reset my password, I do not receive the password reset email.
    I have tried using different browsers and devices, but the issue persists.
    This problem is causing significant disruption to my work, and I need to access my account as soon as possible. I would appreciate it if you could help me resolve this issue promptly.

    Please let me know what information you require from me to investigate and resolve this matter. I can be reached at adam@ACME.com.

    Thank you for your prompt attention to this matter. I look forward to your response.

    Best regards,
    Adam
    """

    user_message3 = {"role": "user", "content": "This is a support ticket that a client has raised:" + content3 + "\n \n Extract, in an unnumbered \
    list, the 3 primary relevant specific task(s) that you have to do in order to resolve this ticket. Based on the context of the ticket, assign a number between 1-10 for how urgent \
    the task needs to be completed. Tasks that require immediate attention to the customer's current operations should be given a higher score. Tasks that are \
    for future plans (like feature requests) should be given lower scores. Give reasoning for each score. Here is an example: -Schedule a discovery call with XYZ \
    Corporation's key stakeholders to understand their specific goals, challenges, and requirements (10). This task has a (10) at the end because it is of utmost importance."}

    message_list3.append(user_message3)

    # Send the message to the bot
    response_message3 = openai.ChatCompletion.create(model=model, messages=message_list3, temperature=temperature)

    # Get the response from the bot
    response3 = response_message3.choices[0].message.content

    return response3



def contract_extract():
    """Extract tasks from contracts and assign each of them an urgency score"""

    message_list4 = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message4 = {"role": "system", "content": "You are a busy Customer Success manager at a startup and you deal with many clients"}

    message_list4.append(system_message4)

    content4 = """

    ---
    Software Sales Agreement

    This Software Sales Agreement (the "Agreement") is made and entered into on this 24th day of October, 2023 (the "Effective Date"), by and between:

    **TechSolutions Inc.**
    a Delaware Corporation
    ("Supplier")

    and

    **ACME Inc.**
    a Texas LLC
    ("Client")

    (collectively referred to as the "Parties").

    **WHEREAS**, Supplier has developed a software solution, as further described in Exhibit A (the "Software"), which Client wishes to purchase for its business operations.

    **NOW, THEREFORE**, in consideration of the mutual covenants contained herein, the Parties agree as follows:

    ## 1. Software License

    1.1 **Grant of License.** Supplier grants Client a non-exclusive, non-transferable, and revocable license to use the Software for the purposes of its business operations.

    1.2 **License Term.** The initial license term shall begin on the Effective Date and continue for a period of 12 months. The Parties agree that each renewal shall be set to occur on the 24th day of October of each year following the expiration of the prior term, with the first renewal taking place on the 24th day of October, 2024. A Customer Success Manager will follow up with Client to discuss renewal options at least 90 days prior to the expiration of each term.

    1.3 **License Restrictions.** Client may not sublicense, lease, sell, or otherwise transfer the Software or any portion thereof to any third party. Client shall not reverse engineer, decompile, or disassemble the Software.

    ## 2. Software Support and Updates

    2.1 **Support Services.** Supplier will provide Client with 24/7 technical support during the term of this Agreement. Client may be required to pay additional fees for premium support services, as described in Exhibit B.

    2.2 **Software Updates.** Supplier shall provide Client with any updates, bug fixes, and new versions of the Software at no additional cost during the license term.

    ## 3. Payment

    3.1 **Fees.** In consideration for the license and support services, Client shall pay Supplier the fees as described in Exhibit C.

    3.2 **Payment Terms.** Client shall make payments within 30 days of receiving an invoice from Supplier.

    ## 4. Confidentiality

    4.1 **Confidential Information.** Both Parties agree to keep confidential any non-public information disclosed by the other Party during the course of this Agreement.

    4.2 **Exceptions.** The confidentiality obligations do not extend to information that is in the public domain or that is independently developed by the receiving Party.

    ## 5. Term and Termination

    5.1 **Term.** This Agreement shall commence on the Effective Date and shall continue until terminated by either Party in accordance with the terms herein.

    5.2 **Termination for Cause.** Either Party may terminate this Agreement in the event of a material breach by the other Party if such breach remains uncured after 30 days' notice.

    ## 6. Miscellaneous

    6.1 **Entire Agreement.** This Agreement constitutes the entire agreement between the Parties concerning the subject matter hereof and supersedes all prior and contemporaneous agreements, proposals, and understandings, whether written or oral.

    6.2 **Governing Law.** This Agreement shall be governed by and construed in accordance with the laws of the state of Delaware.

    **IN WITNESS WHEREOF**, the Parties hereto have executed this Software Sales Agreement as of the Effective Date.

    **TechSolutions Inc.**
    By: John Smith
    Name: John Smith
    Title: CEO

    **ACME Inc.**
    By: Jane Doe
    Name: Jane Doe
    Title: CFO

    ---
    """

    user_message4 = {"role": "user", "content": "This is a contract that your company has with a client:" + content4 + "\n \n The date today is July 24th, 2024. Extract, in an unnumbered \
    list, the 3 primary relevant task(s) that you have to do based on this contract. Based on the context of the contract, assign a number between 1-10 for how urgent \
    the task needs to be completed. Tasks that require immediate attention to the customer's current operations should be given a higher score. Tasks that are \
    for future plans (like feature requests) should be given lower scores. Give reasoning for each score. Here is an example: -Schedule a discovery call with XYZ \
    Corporation's key stakeholders to understand their specific goals, challenges, and requirements (10). This task has a (10) at the end because it is of utmost importance."}

    message_list4.append(user_message4)

    # Send the message to the bot
    response_message4 = openai.ChatCompletion.create(model=model, messages=message_list4, temperature=temperature)

    # Get the response from the bot
    response4 = response_message4.choices[0].message.content

    return response4





def prioritize_tasks(content_final):  
    """Take all the tasks and prioritize them into a master task list"""

    message_list_final = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message_final = {"role": "system", "content": "You are a busy Customer Success manager at a startup and you deal with many clients"}

    message_list_final.append(system_message_final)

    #content_final = response + "\n" + response2 + "\n" + response3 + "\n" + response4

    user_message_final = {"role": "user", "content": "These are the tasks that you have for this coming week for one client" + content_final + "\n \n Based on the context \
    of the tasks, each task has a score at the end between 1-10 for how urgent the task needs to be completed. \
    For example, this task: -Schedule a discovery call with XYZ Corporation's key stakeholders to understand their specific goals, challenges, and requirements (10).\
    This task has a (10) at the end because it is of utmost importance. Now, using this urgency score and the provided reasoning, along with your own knowledge and expertise as \
    a Customer Success manager, prioritize the given tasks, and only the given tasks. Tasks that require immediate attention to the customer's current operations (like issues or renewals) should be prioritized. Tasks that are for \
    future plans (like feature requests) should be lesser priority. Keep the list format. Give reasoning for each task's priority positioning."}

    message_list_final.append(user_message_final)

    # Send the message to the bot
    response_message_final = openai.ChatCompletion.create(model=model, messages=message_list_final, temperature=temperature)

    # Get the response from the bot
    response_final = response_message_final.choices[0].message.content

    return response_final





def update_master_tasks(master_task_list, content_update):
    """Update task list every time a new task is detected"""

    message_list_update = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message_update = {"role": "system", "content": "You are a busy Customer Success manager at a startup and you deal with many clients"}

    message_list_update.append(system_message_update)

    #content_update = response_final + "\n" + response_new_update

    user_message_update = {"role": "user", "content": "This is the task list that you have for this coming week for one client. It is ranked from highest \
    priority to lowest:" + master_task_list + "\n \n Based on the context of the tasks, each task has a score at the end between 1-10 for how urgent the task needs to be completed. \
    Example: -Schedule a discovery call with XYZ Corporation's key stakeholders to understand their specific goals, challenges, and requirements (10).\
    This task has a (10) at the end because it is of utmost importance. Now, using the urgency score and the provided reasoning, along with your own knowledge and expertise as \
    a Customer Success manager, insert the following new task(s) into the proper place in the task list based on priority: " + content_update + "Tasks that require immediate attention to \
    the customer's current operations (like issues or renewals) should be higher priority. Tasks that are for future plans (like feature requests) should be lesser priority. \
    Keep the numbered list format. DO NOT create additional tasks; only use the given tasks. Give reasoning for the new task's priority positioning."}

    message_list_update.append(user_message_update)

    # Send the message to the bot
    response_message_update = openai.ChatCompletion.create(model=model, messages=message_list_update, temperature=temperature)

    # Get the response from the bot
    response_updated = response_message_update.choices[0].message.content

    return response_updated

def clean_list(task_list):

    clean_message_list = []

    # Firstly, we need to set up a instruction for the bot to follow
    system_message = {"role": "system", "content": "You are a simple secretary"}

    clean_message_list.append(system_message)

    user_message = {"role": "user", "content": "Given the following text, remove the extra reasoning parts. Remove the number at the end of each task as well. \
    I only want a numbered task list. \n\n" + task_list}

    clean_message_list.append(user_message)

    # Send the message to the bot
    response_message = openai.ChatCompletion.create(model=model, messages=clean_message_list, temperature=temperature)

    # Get the response from the bot
    cleaned_response = response_message.choices[0].message.content

    return cleaned_response

