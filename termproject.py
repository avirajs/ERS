#makes cards in tuples
"""
Written by: Darren Ting(darrent) and Aviraj Sinha (avirajs)
Functionality: To play, use a,s,k,l for player 1 place and slap,
and player 2 place and slap respectively
We also used multiple modules:
PIL: http://www.pythonware.com/products/pil/
pyaudio: https://people.csail.mit.edu/hubert/pyaudio/
TKinter
and wave
We imported pictures from the following:
http://all-free-download.com/free-vector/free-vector-playing-cards.html
http://www.kardify.com/2013/05/designers-joshua-m-smiths-playing-card.html
http://www.homess.link/other-design/wood-table-top-texture/
http://i.imgur.com/xsKUETn.gif
and http://cooldesktop.blogspot.com/2011/06/space-planets-comets-and-galaxy_08.html
We also used the following song on WAV: Final Destination Suber SMash Bros Brawl Theme
And the following fonts: Alien League, Castellar
We also utilized multithreaded programming for background music and object oriented programming for cards
warning: background music only ends when song ends or if the game ends regardless of if the prrogram closes or not
"""
import random
from Tkinter import *

#shuffle
import wave


from threading import Thread
def run():
    # create the root and the canvas
    global canvas
    global root
    global card
    global backsong
    root = Tk()
    canvas = Canvas(root, width=800, height=800)
    backsong = wave.open('brawl.wav', 'rb')
    splash()
    
    canvas.pack()
    
    root.resizable(width=0, height=0)  # makes window non-resizable
    # Set up canvas data and call init
    
    # set up events
    # and launch the app
    root.mainloop()  
    # This call BLOCKS (so your program waits until you close the window!)
def splash():
    photo = PhotoImage(file = "wood.gif")
    canvas.create_image(400,400,image = photo)
    label = Label(image = photo)
    label.image = photo
    canvas.create_text(400,20,text="Egyptian Rat Screw",font = "Castellar 30")
    button=Button(root,text='Play New Game',command=gamebegin)
    button.pack()
    canvas.create_text(400,200,text="Player 1: \n Press a to place a card \n Press s to slap a card",font = "Castellar 30")
    canvas.create_text(400,600,text="Player 2: \n Press k to place a card \n Press l to slap a card",font = "Castellar 30")
def music(chunk):
    global gameovr
    global backsong
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(backsong.getsampwidth()),
                    channels = backsong.getnchannels(),
                    rate = backsong.getframerate(),
                    output = True)
     # read data (based on the chunk size)
    data = backsong.readframes(chunk)
    
        # play stream (looping from beginning of file to the end)
    while data != '':
            # writing to the stream is what *actually* plays the sound.
        if gameovr:
            stream.close()
            backsong.close()
            p.terminate()
        stream.write(data)
        data = backsong.readframes(chunk)
        
    stream.close()
    backsong.close()
    p.terminate()

       
def init():
    class Struct: pass
    global gameovr
    global dis
    gameovr = False
    dis = False
    canvas.data = Struct()
    canvas.data.cardLength=175
    canvas.data.cardWidth=100
    canvas.data.xplayer1 = 100 #the top-left
    canvas.data.yplayer1 = 500
    canvas.data.xplayer2 = 500
    canvas.data.yplayer2 = 100
    canvas.data.xdeck1=300
    canvas.data.ydeck1=350
    canvas.data.xdeck2=350
    canvas.data.ydeck2=350
    canvas.data.xdeck3=400
    canvas.data.ydeck3=350
    cards=[]
    for n in xrange(2, 11):
        cards.append((str(n),'h'))
    cards.append(('j','h'))
    cards.append(('q','h'))
    cards.append(('k','h'))
    cards.append(('a','h'))
    for n in xrange(2,11):
        cards.append((str(n),'s'))
    cards.append(('j','s'))
    cards.append(('q','s'))
    cards.append(('k','s'))
    cards.append(('a','s'))
    for n in xrange(2,11):
        cards.append((str(n),'c'))
    cards.append(('j','c'))
    cards.append(('q','c'))
    cards.append(('k','c'))
    cards.append(('a','c'))
    for n in xrange(2,11):
        cards.append((str(n),'d'))
    cards.append(('j','d'))
    cards.append(('q','d'))
    cards.append(('k','d'))
    cards.append(('a','d'))
    random.shuffle(cards)
    canvas.data.p1=player(cards[0:26], "Player One")
    canvas.data.p2=player(cards[26:52], "Player Two")
    canvas.data.pile = pile([])
    canvas.data.burnpile = pile([])
    global counter
    counter = 0
    global facetime
    global fc
    global lim
    fc=0
    lim=0
    facetime=False#########
def gamebegin():
    global canvas
    global backsong
    #restarts
    backsong.rewind()
    init()
    canvas.delete(ALL)
    
    cd= canvas.data
    root.bind("<Key>", keyPressed)
    a = Thread(target=music,args = (1024,))
    a.start()
    photo = PhotoImage(file = "gg.gif")
    canvas.create_image(400,400,image = photo)
    label = Label(image = photo)
    label.image = photo
    canvas.create_text(0,0,text = "Player Two Card Count: " + \
                            str(canvas.data.p2.cardcount()), \
                       font=('Alien League', 20), fill = 'white', anchor = 'nw')
    canvas.create_text(650,650,text = "Player One Card Count: " + \
                            str(canvas.data.p1.cardcount()), \
                       font=('Alien League', 20), fill = 'white', anchor = 'se')
    photo = PhotoImage(file = "back.gif")
    canvas.create_image(0,800,image = photo, anchor = 'sw')
    label = Label(image = photo)
    label.image = photo
    canvas.create_text(800,350, text = "Pile Card Count: 0", \
                       font=('Alien League', 20),  anchor = 'e')
    #draw player 2's card
    canvas.create_image(800,0,image = photo, anchor = 'ne')
    label = Label(image = photo)
    label.image = photo
    #the deck
    global end
    end = 0
def drawCards():
    global cd
    cd = canvas.data
    print len(canvas.data.pile.cards)
    if len(canvas.data.pile.cards)==1:
        photo = PhotoImage(file = "%s.gif"%(''.join(canvas.data.pile.cards[0])))
    
        canvas.create_image(cd.xdeck1-cd.cardWidth/2,cd.ydeck1+cd.cardLength/2,image = photo, anchor = 'sw')
        label = Label(image = photo)
        label.image = photo

    elif len(canvas.data.pile.cards)==2:
            
            photo = PhotoImage(file = "%s.gif"%(''.join(canvas.data.pile.cards[-2])))
    
            canvas.create_image(cd.xdeck1-cd.cardWidth/2,cd.ydeck1+cd.cardLength/2,image = photo, anchor = 'sw')
            label = Label(image = photo)
            label.image = photo
            photo = PhotoImage(file = "%s.gif"%(''.join(canvas.data.pile.cards[-1])))    
            canvas.create_image(cd.xdeck2-cd.cardWidth/2,cd.ydeck2+cd.cardLength/2,image = photo, anchor = 'sw')
            label = Label(image = photo)
            label.image = photo
    elif len(canvas.data.pile.cards)>=3:
            photo = PhotoImage(file = "%s.gif"%(''.join(canvas.data.pile.cards[-3])))
            canvas.create_image(cd.xdeck1-cd.cardWidth/2,cd.ydeck1+cd.cardLength/2,image = photo, anchor = 'sw')
            label = Label(image = photo)
            label.image = photo
            photo = PhotoImage(file = "%s.gif"%(''.join(canvas.data.pile.cards[-2])))    
            canvas.create_image(cd.xdeck2-cd.cardWidth/2,cd.ydeck2+cd.cardLength/2,image = photo, anchor = 'sw')
            label = Label(image = photo)
            label.image = photo
            photo = PhotoImage(file = "%s.gif"%(''.join(canvas.data.pile.cards[-1])))
    
            canvas.create_image(cd.xdeck3-cd.cardWidth/2,cd.ydeck3+cd.cardLength/2,image = photo, anchor = 'sw')
            label = Label(image = photo)
            label.image = photo
def redrawAll():
    global gameovr
    global counter
    global dis
    cd = canvas.data
    if gameovr!=True:
        if not dis:
            canvas.delete(ALL)
            
        
            photo = PhotoImage(file = "gg.gif")
            canvas.create_image(400,400,image = photo)
            label = Label(image = photo)
            label.image = photo
            canvas.create_text(800,350, text = "Pile Card Count: "+ str(len(cd.pile.cards)), \
                               font=('Alien League', 20), anchor = 'e')
            
            canvas.create_text(350,10,text = "Burn Pile: "+ \
                            str(len(cd.burnpile.cards)), \
                       font=('Alien League', 15), fill = 'white', anchor = 'nw')
            canvas.create_text(0,0,text = "Player Two Card Count: " + \
                                    str(canvas.data.p2.cardcount()), \
                               font=('Alien League', 20), fill = 'White', anchor = 'nw')
            canvas.create_text(650,650,text = "Player One Card Count: " + \
                                    str(canvas.data.p1.cardcount()), \
                               font=('Alien League', 20), fill = 'white', anchor = 'se')
        global canvas
        global last
        
       # draw player 1s card
        if dis:############################################################3
            dis=False
            photo = PhotoImage(file = "%s.gif"%(''.join(last[0]+last[1])))#u might need to change this
            for x in range(0,len(last)):
                print last[x]
            canvas.create_image(cd.xdeck3+50-cd.cardWidth/2,cd.ydeck3+cd.cardLength/2,image = photo, anchor = 'sw')
            label = Label(image = photo)
            label.image = photo
        photo = PhotoImage(file = "back.gif")
        
        canvas.create_image(0,800,image = photo, anchor = 'sw')
        label = Label(image = photo)
        label.image = photo
        #draw player 2's card
        
        canvas.create_image(800,0,image = photo, anchor = 'ne')
        label = Label(image = photo)
        label.image = photo
        drawCards()
    #the deck
    
def keyPressed(event):
      global counter
      global facetime
      if (event.keysym == "s"):
        canvas.data.p1.slap()
      elif (event.keysym == "l"):
        canvas.data.p2.slap()
      elif(event.keysym=="a"):
        if counter%2==0:
            counter=0
            canvas.data.p1.place(canvas.data.pile)
            if not facetime:
                counter=1
        else:
            canvas.data.p1.burn(canvas.data.burnpile)
            
      elif(event.keysym=="k"): 
        if counter%2==1:
            counter=1
            canvas.data.p2.place(canvas.data.pile)
            if not facetime:
                counter=0
        else:
            canvas.data.p2.burn(canvas.data.burnpile)
    
      elif(event.keysym=="r"):
            backsong.rewind()
            init() #restarts by calling init again
      redrawAll()
def gameover(name):
    canvas.delete(ALL)
    photo = PhotoImage(file = "wood.gif")
    canvas.create_image(400,400,image = photo)
    label = Label(image = photo)
    label.image = photo
    print 'in'
    canvas.create_text(0,0, text = "Game is Over! " + name+ " \n loses!!! \n press the New Game Button \n To restart!", \
                       font=('Alien League', 50),fill = "black", anchor = 'nw')
    root.unbind("<Key>")
    root.bind("r", keyPressed)
    photo = PhotoImage(file = "test.gif")
    canvas.create_image(400,600,image = photo)
    label = Label(image = photo)
    label.image = photo
class Card:
    def __init__(self, val, fimg, isface, bimg):
        self.value = val
        self.image = img
        self.isface = isface
        self.backim = bimg
class player:
    def __init__(self, cards, name):
        self.cards= cards
        self.name = name
    def cardcount(self):
        return len(self.cards)
    def slap(self):
        global counter
        if canvas.data.pile.check()==True:
            counter+=1
            self.winpile(canvas.data.pile)
            self.winpile(canvas.data.burnpile)
        else:
            self.burn(canvas.data.burnpile)
    def place(self,pile):
        global gameovr
        if self.cardcount()==0:
             gameovr = True
             gameover(self.name)
        else:
            global facetime
            global fc
            global lim
            global counter
            global last#################
            global dis############
            last=self.cards.pop()#################
            pile.cards.append(last)################
            
            #finds the strength of the face card
            if pile.isface():
                lim=pile.faceval()
                facetime=True
                fc=0
            #changes move after initial face card challenge
            if fc==0 and facetime:
                counter+=1
            #once the face card wins deck
            if fc==lim and lim!=0:
                dis=True
                if counter==0:
                    counter+=1
                    canvas.data.p1.winpile(canvas.data.pile)
                    canvas.data.p1.winpile(canvas.data.burnpile)
                    lim = 0
                    fc = 0
                if counter==1:
                    counter+=1
                    canvas.data.p2.winpile(canvas.data.pile)
                    canvas.data.p2.winpile(canvas.data.burnpile)
                    lim = 0
                    fc = 0
                facetime=False
                fc=0
            else:
                fc+=1
            
    def winpile(self, pile):
        self.cards.reverse()
        self.cards.extend(pile.cards)
        pile.cards = []
        print self.cardcount()
        self.cards.reverse()
    def burn(self, pile):
        pile.cards.reverse()
        pile.cards.append(self.cards.pop())
        pile.cards.reverse()
        print self.cardcount()
        if self.cardcount()==0:
             global gameovr
             gameovr = True
             gameover(self.name)
class pile:
    def __init__(self, cards):
        self.cards = cards
    def faceval(self):
        if self.cards[-1][0]=="a":
                return 4
        elif self.cards[-1][0]=="k":
                return 3
        elif self.cards[-1][0]=="q":
                return 2
        elif self.cards[-1][0]=="j":
                return 1
    def isface(self):
        
        if len(self.cards)>0 and self.cards[-1][0].isalpha():
            return True
        else:
            return False
    def check(self):
        if len(self.cards)>=2:
            if self.cards[-1][0]==self.cards[-2][0]:
                return True
            elif len(self.cards)>2 and self.cards[-1][0]==self.cards[-3][0]:
                return True
            else:
                return False
        elif len(self.cards)==1:
            return False
        else:
            return True


run()
