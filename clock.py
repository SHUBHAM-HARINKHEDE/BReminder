from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client
from os import environ
# Your Account Sid and Auth Token from twilio.com/console
account_sid = environ['TWILIO_ACCOUNT_SID']
auth_token = environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
#c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
c.execute("SELECT * FROM user_birthday")

print(c.fetchall())


sched = BlockingScheduler()
@sched.scheduled_job('cron',day_of_week='*', hour=1, minute=29)
def scheduled_job():
    
    

    '''
    message = client.messages \
                    .create(
                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        from_='+12058138131',
                        to='+919404838807'
                    )
    
    print(message.sid)
    '''
    message = client.messages \
                .create(
                     from_='whatsapp:+14155238886',
                     body='Your appointment is coming up on July 21 at 3PM',
                     to='whatsapp:+919404838807'
                 )
    print(message.sid)
    

sched.start()