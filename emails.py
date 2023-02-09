import base64
import smtplib
from email.message import EmailMessage
#import creds as creds
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class email:
    def send_email2(self, to, subject, body):
        try:
            service_account_file = "C:/Users/od7mo/OneDrive/Desktop/py_senior/Senior-project-2/client_secret_18141019418-rmap30313co8u0abvm119anpa7lirfci.apps.googleusercontent.com.json"
            credentials = Credentials.from_service_account_file(
                service_account_file,
                scopes=['https://www.googleapis.com/auth/gmail.send']
            )
            service = build('gmail', 'v1', credentials=credentials)
            message = EmailMessage()
            message.set_content(body)
            message['to'] = to
            message['subject'] = subject
            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        except HttpError as error:
            send_message = None
        return send_message

    def send_email(self,  to, subject, body):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('od.7mod@gmail.com', 'rjtkxrrbtahrwjsc')
        message = f'Subject: {subject}\n\n{body}'
        sender = "od.7mod@gmail.com"
        server.sendmail(sender, to, message)
        server.quit()
        return


    def generate_body(self, student_id, password):
        body = f"""Welcome to Arab American University
        now you can use E-Sevices of Arab American University (AAUP)
         and this is your login info:
         student_id: {student_id}
password: {password}
this password is temporary, you should change it as soon as 
and don't forget or share it with anyone.
"""
        return body

    def send(self, to, student_id, password):
        body = self.generate_body(student_id, password)
        subject = "Welcome to AAUP"
        self.send_email(to, subject, body)
        return
