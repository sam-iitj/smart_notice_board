import imaplib
import poplib
import mimetypes
import os
import time
import email
import re
from email import *

msg_list = []




############################################# Server_init #################################################

def server_init():
  k=0
  if k==0:  
    try:
      M = imaplib.IMAP4_SSL("imap.gmail.com")
      time.sleep(5)
    except Exception, e:
      k=1
      print "Oops!  network connectivity is not there"
      time.sleep(5)
  if k==1: M=server_init()
  else:
    return M

#############################################Create table###################################################
def create_table(msg_no,sender,msg_sub,file_list):
  d=open('/home/nfs/table.txt','a')
  matchObj = re.match( r'(.*).*(valid *: *(\d{1,}).*)', msg_sub)
  if matchObj :
    entry = str(msg_no)+','+str(sender)+','+str(matchObj.group(1))+','+str(file_list)+'\n'
  else:
    entry = str(msg_no)+','+str(sender)+','+str(msg_sub)+','+str(file_list)+'\n'
  d.write(entry)
  d.close()

def write_index(msg_no):
  d=open('/home/nfs/index.txt','w')
  d.write(str(msg_no))
  d.close()

def schedule():
  for j in range(len(msg_list)):
    if msg_list[j][2]<=0:
      msg_list[j][3]= -1

  for i in range(len(msg_list)): 
      if msg_list[i][3]!=-1:
        print write_index(msg_list[i][0])
        print msg_list[i]
      if msg_list[i][2]>0:
        msg_list[i][2]-=60
      check_new_mail()
      time.sleep(30)
      
def create_msg_list(num,msg_date,msg_sub):
  in_time = time.mktime(email.utils.parsedate(msg_date))
  if 'valid' in msg_sub or 'Valid' in msg_sub or 'VALID' in msg_sub:
    if 'days' in msg_sub or 'Days' in msg_sub or 'DAYS' in msg_sub:
      matchObj = re.match( r'(.*).*(valid *: *(\d{1,}).*)', msg_sub)
      validity= int(matchObj.group(3))*86400
    if 'hours' in msg_sub or 'Hours' in msg_sub or 'HOURS' in msg_sub:
      matchObj = re.match( r'(.*).*(valid *: *(\d{1,}).*)', msg_sub)
      validity= int(matchObj.group(3))*3600      
    msg_list.append([num,int(in_time),int(validity),int(1)])
  else:
    validity = 1*86400
    msg_list.append([num,int(in_time),int(validity),int(1)])
  print msg_list


########################################### CHECK NEW MAIL #########################################################


def check_new_mail():
  try:
    M.select()
  except Exception, e:
    e=1
    print "authentication mode is not supporting .  Try again..."
    print login()
    M.select()
  typ, data = M.search(None,'UnSeen')
  for num in data[0].split():
      file_list=''	
      typ, data = M.fetch(num, '(RFC822)')
      raw_email = data[0][1]
      email_message = email.message_from_string(raw_email)
      msg_date = email_message['Date']
      msg_sub = email_message['Subject']
      from_add = email_message['From']
      print from_add
      if from_add == 'here will come address of the mail whose request you want to process':####like name<name@dd.com>
          create_msg_list(num,msg_date,msg_sub)
          for part in email_message.walk():
              if part.get_content_maintype() == 'multipart':
                  continue
              filename = part.get_filename()
	      if filename:
		if file_list == '':
		  file_list = filename
		else :
		  file_list = file_list+','+filename
                fp = open(os.path.join('/home/nfs', filename), 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
          create_table(num,from_add,msg_sub,file_list)
  return 'mail_entered_box' 
  

############################################### LOGIN #####################################################

def login():
  m=0
  if m==0:  
    try:
      M.login("email_address", "email_password")
      time.sleep(5)
    except Exception, e:
      m=1
      print "Oops!  The authentication credentials were wrong.  Try again..."
      time.sleep(5)
  if m==1:login()
  else:
    print check_new_mail()
    return "login_successfully"

server_init()
M = imaplib.IMAP4_SSL("imap.gmail.com")
print login()

while 1:
  schedule()
     
M.close()
M.logout()
