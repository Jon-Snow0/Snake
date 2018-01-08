#########################################
# Programmer: Matthew Paulin
# Date: November 27, 2016
# Description: This program is a snake Game.
#########################################
''' reset variables after restart, add apples, apple sizing and poison apples, saw blades, sound, boost'''
import pygame
pygame.init()
import random as r
import time
import math as m
step=20 #grid size
width = 50*step #screen width
height  = 35*step #screen height
screen=pygame.display.set_mode((width,height))
delay=60

#different size fonts
font = pygame.font.SysFont("Ariel Black",50)
font1 = pygame.font.SysFont("Ariel Black",100)
font2 = pygame.font.SysFont("Ariel Black",250)

score=0 #score

#colors
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
GREY= (128,128,128)
outline=0 #outline

#loading and resizing the images for the snake's head and body
snakeHU = pygame.image.load("snakeHU.png")
snakeHU = snakeHU.convert_alpha()
snakeHD = pygame.image.load("snakeHD.png")
snakeHD = snakeHD.convert_alpha()
snakeHR = pygame.image.load("snakeHR.png")
snakeHR = snakeHR.convert_alpha()
snakeHL = pygame.image.load("snakeHL.png")
snakeHL = snakeHL.convert_alpha()
snakeBU = pygame.image.load("snakeBU.png")
snakeBU = snakeBU.convert_alpha()
snakeBR = pygame.image.load("snakeBR.png")
snakeBR = snakeBR.convert_alpha()
snakeHU = pygame.transform.scale(snakeHU, (step,step+step//2))
snakeHD = pygame.transform.scale(snakeHD, (step,step+step//2))
snakeHR = pygame.transform.scale(snakeHR, (step+step//2,step))
snakeHL = pygame.transform.scale(snakeHL, (step+step//2,step))
snakeBU = pygame.transform.scale(snakeBU, (step,step))
snakeBR = pygame.transform.scale(snakeBR, (step,step))

#loading the images for the start and end screens, poison apples, and obstacles
snakeintro=pygame.image.load("snakeintro.png")
snakeintro = snakeintro.convert_alpha()
snakeintro = pygame.transform.scale(snakeintro, (width-100,height-100))
snakeend=pygame.image.load("snakeend.png")
snakeend = snakeend.convert_alpha()
snakeend = pygame.transform.scale(snakeend,(width-100,height-100))
papple = pygame.image.load('papple.png')
papple = papple.convert_alpha()
papple = pygame.transform.scale(papple, (step,step))
saw = pygame.image.load('saw.png')
saw = saw.convert_alpha()
saw = pygame.transform.scale(saw, (step*3,step*3))

sawx=[] #list of sawblades' coordinate
sawy=[] #list of sawblades' coordinate

#loading and resizing a list of apples
apple = [pygame.image.load('apple.png')]
apple[0] = apple[0].convert_alpha()
apple[0] = pygame.transform.scale(apple[0], (step,step))

string = 'movingimage' #string to help with loading the gif background
images=[] # list for the background gif's frames
#loafing and resizing the background gif's frames
for i in range(28):
    images.append(pygame.image.load(string+str(i)+'.png'))
    images[i] = images[i].convert_alpha()
    images[i] = pygame.transform.scale(images[i], (width,height))

#Horizontal and vertical speeds
HSPEED = step
VSPEED = step

#setting the coordinates for the  first apple and poison apple
applex=[r.randint(1,49)*step-int(step/2)]
appley=[r.randint(1,34)*step-int(step/2)]
papplex=r.randint(1,49)*step-int(step/2)
pappley=r.randint(1,34)*step-int(step/2)

#loading all the music and sound effects
##pygame.mixer.music.load('dummy.wav')  #
##pygame.mixer.music.set_volume(0.4)      # 
##pygame.mixer.music.play(loops = -1)     #
grow = pygame.mixer.Sound('grow.wav')   # 
grow.set_volume(0.8)
shrink = pygame.mixer.Sound('shrink.wav')   # 
shrink.set_volume(0.8)
gameoversound = pygame.mixer.Sound('gameover.wav')   # 
gameoversound.set_volume(0.8)

#setting initial speed so that snake moves up
speedX = 0
speedY = -VSPEED

#setting the initial position of the snake
segx = [300]*3
segy = [640, 640+VSPEED, 640+2*VSPEED]

#dimentions of a rectangle used for the start button on the start screen
rx=width/2-125
ry=height/2+150
rw=250
rh=100

#setting the initial size of the apple
appler=[step]
#set to choose the size of the apple from
applewidthset=(step,step*3)
#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#
def redraw_screen(frame): #takes the frame of the gif background as a parameter
    global timer
    screen.blit(images[frame], (0,0)) #displaying the gif
    for i in range(len(applex)): #displays all the apples
        screen.blit(apple[i], (applex[i],appley[i]))
    for i in range(len(sawx)):#displays all the saws
        screen.blit(saw, (sawx[i],sawy[i]))
    screen.blit(papple, (papplex,pappley))#displays the poison apples
    pygame.display.update()#updates the display
    #displays images for the snake's segments
    for i in range(1,len(segx)): 
        if(speedY<0):
            screen.blit(snakeHU, (segx[0]-int(step/2),segy[0]-int(step/2)))
        elif(speedY>0):
            screen.blit(snakeHD, (segx[0]-int(step/2),segy[0]-int(step/2)))
        elif(speedX<0):
            screen.blit(snakeHL, (segx[0]-int(step/2),segy[0]-int(step/2)))
        else:
            screen.blit(snakeHR, (segx[0]-int(step/2),segy[0]-int(step/2)))
        if speedX != 0:
            screen.blit(snakeBU, (segx[i]-int(step/2),segy[i]-int(step/2)))
        else:
            screen.blit(snakeBR, (segx[i]-int(step/2),segy[i]-int(step/2)))

    #displaying score and timer
    text = font.render('Score: '+str(score), 1, (0,255,0))
    text1=font.render('Timer: '+str(timer), 1, (0,255,0))
    screen.blit(text,(width-175,25))
    screen.blit(text1,(25,25))
    
    pygame.display.update()             # display must be updated, in order
                                        # to show the drawings

#---------------------------------------#
# the main program begins here          #
#---------------------------------------#
inPlay = True
print ("Use the arrows and the space br.")#instructions
frame=0 
gameover=0 #start screen
while inPlay:

# check for events

    for event in pygame.event.get():    # check for any events
        if event.type == pygame.QUIT:       # If user clicked close
             inPlay = False                # Flag that we are done so we exit this loop
    # update the screen 
    if gameover==0: #Start screen, draws an image and a start button and moves to the main screen after the user presses start
        pygame.draw.rect(screen, GREY, ((0,0),(width,height)),outline) #background
        screen.blit(snakeintro, (50,50)) #snake image
        pygame.draw.rect(screen, BLACK, ((rx,ry),(rw,rh)),outline)  #rect for the start button
        txtCLR = (r.randint(0,255),r.randint(0,255),r.randint(0,255)) #text color
        welcome=font2.render('snake', 1, txtCLR) #Title
        start=font1.render('START', 1, WHITE) #start text
        #displaying font
        screen.blit(start,(rx+12,ry+25))
        screen.blit(welcome,(width/2-75,100))

        #gets the position of the cursor and if mouse is pressed, sets all variables to their starting values and moves to the main screen
        (mx,my)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mx>=rx and mx<=rx+rw and my>=ry and my<=ry+rh:
                counter=20
                startTime=time.time()
                boost=0
                gameover=1
        pygame.display.update() #updates the display
        
    elif gameover==1: #Main screen, draws all objects including the snake, the background, moves to the end screen when the snake dies or the time runs out

        timer=round(counter-(time.time()-startTime),1) #timer counting down
        boost+=1 #keeps adding to the boost variable
        keys = pygame.key.get_pressed()
        # act upon key events
        if keys[pygame.K_LEFT] and speedX==0: #move left
            speedX = -HSPEED
            speedY = 0
        if keys[pygame.K_RIGHT]and speedX==0:#move right
            speedX = HSPEED
            speedY = 0
        if keys[pygame.K_UP]and speedY==0:#move up
            speedX = 0
            speedY = -VSPEED
        if keys[pygame.K_DOWN]and speedY==0:#move down
            speedX = 0
            speedY = VSPEED

        #if the user eats a poison apple; reduce size, reduce score, reduce time left, new position for the apple
        if segx[0]-papplex>=0 and segx[0]-papplex<step and segy[0]-pappley>=0 and segy[0]-pappley<step:
            shrink.play()
            score-=1
            counter-=2
            segx.pop()
            segy.pop()
            papplex=r.randint(1,49)*step-int(step/2)
            pappley=r.randint(1,34)*step-int(step/2)
            if len(segx)<3: # if the size is too small, end the game
                gameoversound.play()
                gameover=2
                
        #if the snake runs into an obstacle, end the game
        for i in range(len(sawx)):
            if segx[0]-sawx[i]>=0 and segx[0]-sawx[i]<3*step and segy[0]-sawy[i]>=0 and segy[0]-sawy[i]<3*step:
                gameoversound.play()
                gameover=2

        #if the snake eats an apple; grow, play grow sound, add to time left, add to score, speeds up
        for i in range(len(applex)):
            if segx[0]-applex[i]>=0 and segx[0]-applex[i]<appler[i] and segy[0]-appley[i]>=0 and segy[0]-appley[i]<appler[i]:         # if space bar is pressed, add a segment:
                grow.play()
                for k in range(int(appler[i]/step)): 
                    segx.append(segx[-1])           # assign the same x and y coordinates
                    segy.append(segy[-1])
                    # as those of the last segment
                if len(segx)%2==0:
                    delay-=3
                score+=int(appler[i]/step)
                counter+=3
                if boost<20:#if two apples have been eaten in a short span of time, add more to time left
                    counter+=2
                boost=0 
                appler[i]=(applewidthset[r.randint(0,1)]) #new position for the apple

                #if apple is smaller, random position on sceen
                if appler[i]==step:
                        applex[i]=(r.randint(1,49)*step-int(step/2))
                        appley[i]=(r.randint(1,34)*step-int(step/2))
                #if apple is bigger, random position on sceen
                else:
                    applex[i]=(r.randint(3,47)*step-int(step/2))
                    appley[i]=(r.randint(3,31)*step-int(step/2))
                #loading and resizing each apple in the list
                apple[i]=(pygame.image.load('apple.png'))
                apple[i] = apple[i].convert_alpha()
                apple[i]=pygame.transform.scale(apple[i], (appler[i],appler[i]))

                #adds more apples
                if len(segx)>=13 and len(applex)==1 or len(segx)>=23 and len(applex)==2:
                    appler.append(applewidthset[r.randint(0,1)])
                    apple.append(pygame.image.load('apple.png'))
                    apple[-1] = apple[-1].convert_alpha()
                    apple[-1]=pygame.transform.scale(apple[-1], (appler[-1],appler[-1]))
                    if appler[-1]==step:
                        applex.append(r.randint(1,49)*step-int(step/2))
                        appley.append(r.randint(1,34)*step-int(step/2))
                    else:
                        applex.append(r.randint(3,47)*step-int(step/2))
                        appley.append(r.randint(3,31)*step-int(step/2))
                #adds more saws
                if len(sawx)<m.floor(len(segx)/10):
                    sawx.append(r.randint(3,47)*step-int(step/2))
                    sawy.append(r.randint(3,31)*step-int(step/2))
                    for i in range(len(sawx)):
                        for k in range(len(applex)):
                            if applex[k]-sawx[i]>=0 and applex[k]-sawx[i]<3*step and appley[k]-sawy[i]>=0 and appley[k]-sawy[i]<3*step:
                                sawx[i]=(r.randint(3,47)*step-int(step/2))
                                sawy[i]=(r.randint(3,31)*step-int(step/2))
                            if papplex-sawx[i]>=0 and papplex-sawx[i]<step and pappley-saw[i]>=0 and pappley-sawy[i]<step:
                                sawx[i]=(r.randint(3,47)*step-int(step/2))
                                sawy[i]=(r.randint(3,31)*step-int(step/2))
        #if the snake runs into itself: game over
        for i in range(1,len(segx)):
            if segx[0]==segx[i] and segy[0]==segy[i] and len(segx)>3:
                gameover=2
        #if the timer runs out: game over
        if timer<=0:
            gameoversound.play()
            gameover=2
        #if the snake runs into the walls: game over
        if segx[0]<=0 or segx[0]>=width or segy[0]<=0 or segy[0]>=height:
            gameoversound.play()
            gameover=2
        if frame==27:#loops the gif
            frame=-1
        frame+=1#moves to next gif frame
        # move all segments
        for i in range(len(segx)-1,0,-1):   # start from the tail, and go backwards:
            segx[i]=segx[i-1]               # every segment takes the coordinates
            segy[i]=segy[i-1]               # of the previous one
        # move the head
        segx[0] = segx[0] + speedX
        segy[0] = segy[0] + speedY
        for i in range(len(applex)): #tries to avoid overlapping of objects
            for j in range(len(applex)):
                if applex[i] != applex[j] and appley[i] != appley[j]:
                    if applex[i]-applex[j]>=0 and applex[i]-applex[j]<appler[j] and appley[i]-appley[j]>=0 and appley[i]-appley[i]<appler[j]:
                        if appler[i]==step:
                            applex[i]=(r.randint(1,49)*step-int(step/2))
                            appley[i]=(r.randint(1,34)*step-int(step/2))
                        else:
                            applex[i]=(r.randint(3,47)*step-int(step/2))
                            appley[i]=(r.randint(3,31)*step-int(step/2))
                    if applex[i]-papplex>=0 and applex[i]-papplex<appler[i] and appley[i]-pappley>=0 and appley[i]-pappley<appler[i]:
                        if appler[i]==step:
                            applex[i]=(r.randint(1,49)*step-int(step/2))
                            appley[i]=(r.randint(1,34)*step-int(step/2))
                        else:
                            applex[i]=(r.randint(3,47)*step-int(step/2))
                            appley[i]=(r.randint(3,31)*step-int(step/2))
        redraw_screen(frame) #call redraw function
    elif gameover==2: #End screen; resets all variable and has a restart button that if pressed, will restart
        pygame.mixer.music.stop()#stop the music
        #resetting variables
        delay=60
        sawx=[]
        sawy=[]
        papplex=r.randint(1,49)*step-int(step/2)
        pappley=r.randint(1,34)*step-int(step/2)
        applex=[r.randint(1,49)*step-int(step/2)]
        appley=[r.randint(1,34)*step-int(step/2)]
        speedX = 0
        speedY = -VSPEED
        segx = [300]*3
        segy = [640, 640+VSPEED, 640+2*VSPEED]
        
        pygame.draw.rect(screen, GREY, ((0,0),(width,height)),outline)#backgroun
        screen.blit(snakeend, (50,50))#snake picture
        pygame.draw.rect(screen, BLACK, ((rx-50,ry),(rw+100,rh)),outline)#rect for button
        txtCLR = (r.randint(0,255),r.randint(0,255),r.randint(0,255)) #random text color
        #displays game over, scorem and restart text
        welcome=font1.render('Game Over', 1, txtCLR)
        scorestr='Your score was: '+str(score)
        scoretxt=font1.render(scorestr, 1, BLACK)
        start=font1.render('RESTART', 1, WHITE)
        screen.blit(start,(rx-50+15,ry+25))
        screen.blit(scoretxt,(325,250))
        screen.blit(welcome,(width/2-75,100))

        #gets mouse's position, if mouse pressed on the button, restart
        (mx,my)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mx>=rx and mx<=rx+rw and my>=ry and my<=ry+rh:
                #resets all remaining variables
                startTime=time.time()
                pygame.mixer.music.play(loops = -1)
                score=0
                counter=20
                gameover=1
        pygame.display.update() #updates display
    pygame.time.delay(delay) #framerate of pygame window
pygame.mixer.music.stop() #stop the music
pygame.quit() #quit pygame
