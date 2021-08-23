from simplegmail import Gmail
import time

class GmailMonitor:
    def __init__(self):
        self.gmail = Gmail()

    def run(self):
        attachments=[]
        while len(attachments)==0:
            messages = self.gmail.get_unread_inbox()
            print(messages)

            if(messages!=[]):
                for message in messages:
                    if message.attachments:
                        for attm in message.attachments:
                            attachments.append(attm.filename)
                            attm.save()  # downloads and saves each attachment under it's stored
                                                        # filename. You can download without saving with `attm.download()`
                    #message.mark_as_read()
            else:
                time.sleep(600)
            return (attachments)