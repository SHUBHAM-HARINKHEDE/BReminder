from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client
import datetime,os
from sqlalchemy import create_engine,MetaData,Table,Column,Integer, String,Date,extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import smtplib

#engine = create_engine('sqlite:///db.sqlite3', echo = False)
engine = create_engine(os.environ.get('DATABASE_URL'), echo = False)
Base = declarative_base(engine)

#email config
USERNAME = os.environ.get('EMAIL_HOST_USER')
PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


class User(Base):
    id = Column("id", Integer,primary_key=True)
    email = Column("email", String(15))
    __tablename__ = 'auth_user'
    __table_args__ = {'autoload': True}

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
default_cell_number = os.environ.get('CELL_PHONE_NUMBER')
client = Client(account_sid, auth_token)
msg_body_title='Birthdays today:' 

#send msg if recipient != None 
def send_msg(msg_body,recipient):
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

#send email if recipient != None 
def send_mail(msg_body,recipient):
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(USERNAME,PASSWORD)
        smtpserver.sendmail(USERNAME, recipient, msg_body)
        smtpserver.close()
    except Exception as e:
        print("Email not sent:",str(e))
    
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
    recipient=default_cell_number
    email_recipient=USERNAME
    message_body='Hello, there!'                        
    for row in result:
        print(row[1].user_id,row[0].fname,row[1].mobile,row[1].whatsapp)
        if user !=row[1].user_id:
            send_msg(message_body,recipient)
            user=row[1].user_id
            recipient=row[1].whatsapp
            user_details=session.query(User).filter(User.id==row[1].user_id).first()
            email_recipient=user_details.email
            message_body=msg_body_title+ "\n" +str(row[0].fname)+" "+str(row[0].mname)+" "+str(row[0].lname)+"("+str(row[0].dob)+")"
        else:
            message_body=message_body+"\n"+str(row[0].fname or '')+" "+str(row[0].mname or '')+" "+str(row[0].lname or '')+"("+str(row[0].dob)+")"
    #send message
    send_msg(message_body,recipient)
    #send email
    msg_header="""Subject: Birthdays today\n"""
    message_body=msg_header+message_body
    send_mail(message_body,email_recipient)

sched = BlockingScheduler()

#sends reminder @00:00 IST
@sched.scheduled_job('cron',day_of_week='*', hour=00, minute=00)
def scheduled_job():
    try:
        print("in process")
        today_birthday()
        print("done")
    except Exception as e:
        print(e)

sched.start()
