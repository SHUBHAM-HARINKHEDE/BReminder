from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client
import datetime,os
from sqlalchemy import create_engine,MetaData,Table,Column,Integer, String,Date,extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3', echo = False)

Base = declarative_base(engine)

class Profile(Base):
    user_id = Column("user_id", Integer)
    mobile = Column("mobile", String(15))
    whatsapp = Column("whatsapp_number", String(15))
    __tablename__ = 'user_profile'
    __table_args__ = {'autoload': True}

class Birthday(Base):
    user_id = Column("user_id", Integer)
    fname = Column("fname", String(50))
    mname = Column("mname", String(50))
    lname = Column("lname", String(50))
    dob = Column("dob", Date())
    
    __tablename__ = 'user_birthday'
    __table_args__ = {'autoload': True}

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
client = Client(account_sid, auth_token)
msg_body_title='Birthdays today:' 

#send msg if recipient != None 
def send_msg(msg_body,recipient):
    if recipient == None:
        return
    try:
        message = client.messages \
                        .create(
                            body=msg_body,
                            from_='whatsapp:'+twilio_whatsapp_number,
                            to='whatsapp:'+recipient
                        )
        print(message.sid)
    except Exception as e:
        print("message not sent:",str(e))
#fetch todays birthdays calls send_msg function
def today_birthday():
    Session = sessionmaker(bind = engine)
    session = Session()
    today = datetime.date.today()
    
    result = session.query(Birthday,Profile).filter(Birthday.user_id==Profile.user_id,
                                                    extract('day', Birthday.dob)==today.day,
                                                    extract('month', Birthday.dob)==today.month,
                                                    (Profile.whatsapp !=None),            
                                                    ).order_by(Profile.user_id)
                                        
                                            
    user=None  
    recipient=None 
    message_body='test'                        
    for row in result:
        print(row[1].user_id,row[0].fname,row[1].mobile,row[1].whatsapp)
        if user !=row[1].user_id:
            send_msg(message_body,recipient)
            user=row[1].user_id
            recipient=row[1].whatsapp
            message_body=msg_body_title+ "\n" +row[0].fname
        else:
            message_body=message_body+"\n"+row[0].fname
    send_msg(message_body,recipient)

sched = BlockingScheduler()
#sends reminder @00:00 IST
@sched.scheduled_job('cron',day_of_week='*', hour=00, minute=00)
def scheduled_job():
    try:
        today_birthday()
    except Exception as e:
        print(e)

sched.start()
