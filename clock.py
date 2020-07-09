from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client
import os
import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
#c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
c.execute("SELECT * FROM user_birthday")

print(c.fetchall())

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
recipient = '+919404838807'
client = Client(account_sid, auth_token)
msg_body="running"

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    message = client.messages \
                .create(
                     body=msg_body,
                     from_='whatsapp:'+twilio_whatsapp_number,
                     to='whatsapp:'+recipient
                 )

    print(message.sid)



@sched.scheduled_job('cron',day_of_week='*', hour=00, minute=00)
def scheduled_job():
    message = client.messages \
                .create(
                     body=msg_body,
                     from_='whatsapp:'+twilio_whatsapp_number,
                     to='whatsapp:'+recipient
                 )

    print(message.sid)

sched.start()

##########################################################################
'''
message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12058138131',
                     to='+919404838807'
                 )

print(message.sid)
'''
