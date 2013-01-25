import pygame, sys, ctypes
from pygame.locals import *
import time
import os
import re
import mpylayer


#### TABLE IS THE LIST READ FROM THE RAW TABLE.TXT##################

table=[]

########### MAKING TABLE LIST REFERENCABLE#####################
in_table=[]


pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((900, 600), 0, 32)
pygame.display.set_caption('Email')

# set up the colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
ROSY=(70,130,180)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

# draw on the surface object
DISPLAYSURF.fill(WHITE)


myfont = pygame.font.SysFont("Inconsolata", 30)
myfont1 = pygame.font.SysFont("Inconsolata", 33)
myfont2 = pygame.font.SysFont("Inconsolata", 45)
#CONTROLLING NUMNBER OF ELEMENTS IN THE IN_TABLE

i=0

#index for how frequenctly i wanna read from table.txt

l=0

################### READ FROM INDEX FILE#####################################################


def read_from_index_file():
  f=open('/home/nfs_local/index.txt','r')
  e=int(f.read())
  f.close()
  return e



########################### VIDEO DISPLAY ###########################


def video(filename): 
  print filename 
  path='/home/nfs_local/'+filename
  if os.path.isfile(path):
    mp = mpylayer.MPlayerControl()
    mp.loadfile(path)
    time.sleep(10)
  else:
    print 'file not exist'
    return
  return


#####################   DISPLAY THE NOTICE.PNG FILES O SCREEN###############################


def display_notice(i):
      path='/home/nfs_local/'+in_table[i][3]
      if 'mp4' in path:
        video(in_table[i][3])
      else: 
        if os.path.isfile(path):
          noticeImg = pygame.image.load(path)
          noticex = 20
          noticey = 80
          DISPLAYSURF.blit(noticeImg, (noticex, noticey))
          pygame.display.update()
          time.sleep(10)        
        else:
          time.sleep(1)
          return
      return


##################  PRINT THE MSG,SUBJECT AND ITS CONTENT ON THE SCREEN #############################33

def print_label(i):  
  label1 = myfont1.render('Sub '+str(in_table[i][2]), 1, BLACK)
  label = myfont.render('msg '+str(in_table[i][1]), 1, ROSY)
  DISPLAYSURF.blit(label1, (10,15))
  DISPLAYSURF.blit(label, (10,45))
  pygame.display.update()  
 




#####################   READING THE TABLE FILE FROM TABLE.TXT ####################################3



def read_complete_table_file():    
  f=open('/home/nfs_local/table.txt','r')
  for line in f:
      table.append(line)
  f.close()
  return


#####################   PARSING THE TABLE LIST 'STRUCTURE' TO MAIN IT REFERENCABLE EASILY########################


def parsing_data_from_table():
    for i in range(len(table)):
      obj=re.match( r'((\d{1,}),(.*),(.*),(.*).*)', table[i])
      if obj==None:continue
      else:
        msg_no=obj.group(2)
        msg_sender=obj.group(3)
        msg_valid=obj.group(4)
        msg_attach=obj.group(5)
        in_table.append([int(msg_no),msg_sender,msg_valid,msg_attach])
    return
       



####################       READING DATA FROM THE MSG_NO READ FROM THE INDEX FILE ##################################3

def read_complete_in_table():
    read_complete_table_file() 
    parsing_data_from_table()
    return 

#################              READING FROM INDEX FILE THE MSG_NO TO DISPLAY#######################################



def read_from_index():
    f=open('/home/nfs_local/index.txt','r')
    index=int(f.read())
    f.close()
    return index


##################               THE PYGAME MAIN LOOP       ####################################################


 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()    
    read_complete_in_table()
    if i==len(in_table):
      i=0
    d=read_from_index_file()    
    if d==in_table[i][0]:
      print_label(i)
      pygame.display.update()
      m=0
      if m==0:
        r=pygame.draw.rect(DISPLAYSURF,WHITE, (380,20,800,600),2)
        DISPLAYSURF.fill(WHITE,r)
        pygame.display.update()
        display_notice(i)
        m=1
    DISPLAYSURF.fill(WHITE)       
    i+=1
    table=[]
    in_table=[]
    pygame.display.update()



