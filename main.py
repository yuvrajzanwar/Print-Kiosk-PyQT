import time
from dotenv import load_dotenv
import os
import imaplib
import email
from email.header import decode_header
load_dotenv(dotenv_path=".env" , override=True)

token='0002'
downloaded=False
start_time = time.time()
IMAP_SERVER = os.getenv("IMAP_SERVER")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

x_time=time.time()

while downloaded==False and time.time() - start_time < 120:
    # Search for unseen emails with given TOKEN
    
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    try:
        # Login 
        imap.login(USERNAME, PASSWORD)

        mailbox = 'INBOX'
        imap.select(mailbox)

        since_time=time.strftime('%d-%b-%Y',time.localtime(start_time))
        search_criteria = f'(SINCE "{since_time}")'
        
        status, response = imap.search(None, f'UNSEEN SUBJECT {token} {search_criteria}')

        if status == 'OK':
            # Get the list of email IDs
            email_ids = response[0].split()

            for email_id in email_ids:
                # Fetch the email data
                status, email_data = imap.fetch(email_id, '(RFC822)')
                
                if status == 'OK':
                    
                    # Parse the email message
                    raw_email = email_data[0][1]
                    message = email.message_from_bytes(raw_email)

                    # Decode the subject
                    subject = decode_header(message['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode('utf-8')

                    print('Subject:', subject)
                
                    for part in message.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        filename = part.get_filename()
                        if filename:
                            # Save the attachment
                            open('attachments/'+filename, 'wb').write(part.get_payload(decode=True))
                            print(f"Attachment saved: {filename}")
                    downloaded=True
    except Exception as e:
        print(f"----ERROR{e}----")
    finally:    
        imap.logout()    
    if downloaded==False:
        print("\n--------Waiting for attachment--------")
    time.sleep(1)         

if downloaded==True:
    print("\n--------Downloaded attachment--------")
else:
    print("\n--------System Timeout (30s)--------")
print("\n---------EXITING----------") 



print(f"\n----- TIME:{time.time()-x_time}")

