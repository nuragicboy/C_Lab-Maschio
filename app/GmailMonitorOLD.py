import imaplib
import base64
import os
import email

class GmailMonitor:
    def __init__(self):
        self.imap_url = 'imap.gmail.com'
        self.user = "clabmaschio@gmail.com"
        self.password = "cantinemaschio"
        self.label = "Inbox"
        self.search_criteria = ""

    def run(self):
        mail = imaplib.IMAP4_SSL(self.imap_url, 993)
        mail.login(self.user, self.password)
        mail.select()

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()

        for num in data[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]  # converts byte literal to string removing b''
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)  # downloading attachments
            for part in email_message.walk():
                # this part comes from the snipped I don't understand yet...
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filePath = os.path.join('./Test', fileName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    return './Test/'+fileName
        return ""
"""
        for num in data[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]  # converts byte literal to string removing b''
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)  # downloading attachments
            for part in email_message.walk():
                # this part comes from the snipped I don't understand yet...
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filePath = os.path.join('/Users/sanketdoshi/python/', fileName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName,
                                                                                                     subject=subject,
                                                                                                     uid=latest_email_uid.decode(
                                                                                                         'utf-8')))
"""