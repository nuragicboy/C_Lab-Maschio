import smtplib
import os
import imap_tools
from imap_tools import MailBox, AND
import time

def getAttachments(mail):
    path = os.path.abspath("Test/")
    attachments=[]
    with MailBox(mail["host"]).login(mail["address"],mail["password"], 'INBOX') as mailbox:
       for msg in mailbox.fetch(AND(seen=False), mark_seen = False):

           for att in msg.attachments:
               print(path.format(att.filename),msg.uid)
               with open(att.filename, 'wb') as f:
                   attachments.append([att.filename,msg.uid])
                   f.write(att.payload)
    return attachments

def markAs(mail, id, flag):
    with MailBox(mail["host"]).login(mail["address"],mail["password"], 'INBOX') as mailbox:
        mailbox.flag(mailbox.uids(id), imap_tools.MailMessageFlags.SEEN, True)

def send(sender,target,message):
    email = smtplib.SMTP(sender["smtp-host"],sender["smtp-port"])
    email.ehlo()
    email.starttls()
    email.login(sender["address"], sender["password"])
    email.sendmail(sender["address"], target["address"], message.encode('utf-8').strip())
    email.quit()
    '''
        print("mi collego alla mail")
        attachments=[None,None]
        while len(attachments)==0:
            messages = self.gmail.get_unread_inbox()
            print(messages)

            if(messages!=[]):
                for message in messages:
                    if message.attachments:
                        for attm in message.attachments:
                            attachments.append(attm.filename,message)
                            attm.save()  # downloads and saves each attachment under it's stored
                                                        # filename. You can download without saving with `attm.download()`
            else:
                print("nessun messaggio con allegati trovato. ritento tra 60 secondi")
                time.sleep(60)
            return (attachments)

    '''