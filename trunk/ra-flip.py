#!/usr/bin/env python

import sys,random
from PyQt4 import QtCore,QtGui,QtSvg

from Ui_field import Ui_Form

delay=0

walls='''\
      \\  
  |   /  '''

sluices='''\
  >  v2   
 5        
 4^  <3   '''

generators='  2          4     '
   
tarpits=' > 2 + *  '
unary=" ' ' , ' ~ "
arith_with_output=' > 2 + *  p   '
ascii_output=' > 8 * P '
terminate='   Q   '

grille1='  2  #  p '
grille2='     #  p '

processor='''\
 3   \\  p   
   / X  +   
   \\    X   
   Q    /   '''

modifier='''\
 >  3    /  
        ~ % '''
        
modified_flippers='\n'.join([r"""  \   \   \     \ """,
                             r'''   @   @   @     ''',
                             r'''  2   3   4      ''',
                             r'''p +   +   /     Q'''])
                             
modified_sluices='\n'.join([r'  > 5  \   p ',
                            r'   @      ~ @',
                            r'       >   <1',
                            r'          ~  ',
                            r'  > 4  /   \ ', 
                            r'   @         ',
                            r'  \         Q'])
  
modified_sluices2='''\
     @v
      ^'''
  
class FieldWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        data=modified_sluices2
        self.ui.field.output=self.ui.output
        self.field=Field(self.ui.field,data=data)
        Ball(self.field,0,0).setSpeed(1)


        QtCore.QObject.connect(self.ui.zoomIn,QtCore.SIGNAL("clicked()"),self.zoomIn)
        QtCore.QObject.connect(self.ui.zoomOut,QtCore.SIGNAL("clicked()"),self.zoomOut)

        self.zoomIn()
        self.zoomIn()
        self.zoomIn()

        self.field.run()
        
    def zoomIn(self):
        self.ui.field.scale(1.2,1.2)

    def zoomOut(self):
        self.ui.field.scale(1/1.2,1/1.2)
        
        
class Field(QtCore.QObject):
    def __init__(self,widget,width=15,height=15,data=None):
        QtCore.QObject.__init__(self)
        self.scene=QtGui.QGraphicsScene()
        widget.setScene(self.scene)
        self.widget=widget
        self.balls=[]
        self.terminate=False
        if not data:
            self.width=width
            self.height=height
            self.objects=[ [ None for x in range (0,self.width) ] for x in range(0,self.height)]
            self.setupBoard()
        else:
            self.loadData(data)

    def output(self,data):
        self.widget.output.append(data)
            
    def loadData(self,data):
        lines=data.split('\n')
        self.width=len(lines[0])
        self.height=len(lines)
        self.objects=[ [ None for y in range (0,self.height) ] for x in range(0,self.width)]
        self.setupBoard()
        y=0
        for line in lines:
            x=0
            for char in line:
                if char=='|':
                    VertWall(self,x,y)
                elif char=='-':
                    HorizWall(self,x,y)
                elif char=='\\':
                    BSlashWall(self,x,y)
                elif char=='/':
                    SlashWall(self,x,y)
                elif char=='>':
                    RightSluice(self,x,y)
                elif char=='<':
                    LeftSluice(self,x,y)
                elif char=='^':
                    UpSluice(self,x,y)
                elif char=='v':
                    DownSluice(self,x,y)
                elif char in "123456789":
                    Generator(self,x,y,char)
                elif char=='0':
                    ZeroGen(self,x,y)
                elif char=='+':
                    PlusTarpit(self,x,y)
                elif char=='*':
                    MulTarpit(self,x,y)
                elif char=='~':
                    Negate(self,x,y)
                elif char=='\'':
                    Increment(self,x,y)
                elif char==',':
                    Decrement(self,x,y)
                elif char=='.':
                    Reset(self,x,y)
                elif char=='p':
                    NumOut(self,x,y)
                elif char=='P':
                    CharOut(self,x,y)
                elif char=='Q':
                    Terminate(self,x,y)
                elif char=='#':
                    Grille(self,x,y)
                elif char=='X':
                    Processor(self,x,y)
                elif char=='@':
                    Always(self,x,y)
                elif char=='~':
                    Odd(self,x,y)
                elif char=='%':
                    Random(self,x,y)
                else:
                    TextObject(self,x,y,char)
                x+=1 
            y+=1
            
        
        
    def setupBoard(self):
        for i in range(0,self.width):
            for j in range(0,self.height):
                FlipObject(self,i,j)
                pass
        self.objects=[ [ None for y in range (0,self.height) ] for x in range(0,self.width)]
                
        
    def addItem(self,item):
        if isinstance(item,Ball):
            self.balls.append(item)
        else:
            self.objects[item.x][item.y]=item
        self.scene.addItem(item.graphicsItem())
        
    def ballCount(self):
        c=0
        for ball in self.balls:
            if isinstance(ball,Ball):
                c+=1
        return c
        
    def run(self):
        if ( not self.terminate ) and self.ballCount():
            self.doMove()
            self.timer=QtCore.QTimer.singleShot(delay,self.run)
        
    def doMove(self):
        print "doMove"
        for x in range(0,self.width):
            for y in range(0,self.height):
                object=self.objects[x][y]
                if object:
                    object.animated=False


        # Move them balls simultaneously
                    
        for ball in self.balls:
            if not ball: continue
            ball.animated=False
        
        for i in range(0,100):
            for i in range(0,len(self.balls)):
                ball=self.balls[i]
                if not ball: continue
                ball.item.moveBy(ball.sx/10.,ball.sy/10.)
            QtGui.qApp.processEvents()

        for ball in self.balls:
            if not ball: continue
            ball.animate()

                    
        for x in range(0,self.width):
            for y in range(0,self.height):
                object=self.objects[x][y]
                if object:
                    object.animate()

        for i in range(0,len(self.balls)):
            ball=self.balls[i]
            if not ball: continue
            obj=self.objects[ball.x][ball.y]
            if obj:
                obj.handle(ball)
                    
                    
class Modifier:
    def mvalue(self,v):
        # Objects by default don't modify
        return 0
                    
class FlipObject:
    def __init__(self,field,x,y):
        self.animated=False
        self.field=field
        self.x=x
        self.y=y
        self.field.addItem(self)
    def graphicsItem(self):
        self.item=QtGui.QGraphicsRectItem(QtCore.QRectF(10*self.x,10*self.y,10,10))
        self.item.setZValue(0)
        return self.item
        
    def animate(self):
        if self.animated:
            return
        self.animated=True
        
    def handle(self,ball):
        return
                
class Ball(FlipObject):
    def __init__(self,field,x,y,value=0):
        self.value=value
        FlipObject.__init__(self,field,x,y)

    def setValue(self,v):
        self.item2.setText(str(v))
        self.value=v
        
    def kill(self):
        self.item.scene().removeItem(self.item)    
        self.item=None
        self.item2=None
        self.field.balls[self.field.balls.index(self)]=None
        
    def graphicsItem(self):
        self.item=QtGui.QGraphicsItemGroup()
        self.item.setZValue(3)
        self.item1=QtSvg.QGraphicsSvgItem('ball.svg')
        self.item1.setZValue(1)
        self.item1.scale(0.009,0.009)
        self.item1.setPos(10*self.x+.5,10*self.y+.5)

        self.item2=QtGui.QGraphicsSimpleTextItem()
        self.item2.setText(str(self.value))
        br=self.item2.boundingRect()
        self.item2.setPos(10*self.x+2.5,10*self.y+.5)
        sf=10/br.height()
        self.item2.scale(sf,sf)
        self.item2.setZValue(2)
        
        self.item.addToGroup(self.item1)
        self.item.addToGroup(self.item2)
        
        return self.item
        
    def setSpeed(self,sx=0,sy=0):
        self.sx=sx
        self.sy=sy
        
    def animate(self):
        if self.animated:
            return
        self.animated=True
        self.moveTo(self.x+self.sx,self.y+self.sy)

    def moveTo(self,x,y):
        if x>=self.field.width or y>=self.field.height or x<0 or y < 0:
            self.kill()
            return            
        self.x=x
        self.y=y


        
class VertWall(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('vwall.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item

    def handle(self,ball):
        ball.sx=-ball.sx

class HorizWall(FlipObject,Modifier):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('hwall.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item

    def handle(self,ball):
        ball.sy=-ball.sy
    def mvalue(self,v):
        if v>0:
            return 1
        return 0
        
class SlashWall(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('swall.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    def handle(self,ball):
        sy=-ball.sx
        sx=-ball.sy
        ball.sx=sx
        ball.sy=sy
        mods=[]
        if self.y>0 and self.x<self.field.width-1:
            m=self.field.objects[self.x-1][self.y-1]
            if m and isinstance(m,Modifier):
                mods.append(m)
        if self.y<self.field.height-1 and self.x>0:
            m=self.field.objects[self.x+1][self.y+1]
            if m:
                mods.append(m)
        if not mods:
            return
        mval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in mods ]))
        if mval:
            # Flip to BSlashWall
            for i in range(0,90):
                self.item.rotate(1)
                self.item.moveBy(9./90.,0)
                QtGui.qApp.processEvents()
            BSlashWall(self.field,self.x,self.y)
            self.item.scene().removeItem(self.item)    

class BSlashWall(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('bswall.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    def handle(self,ball):
        sy=ball.sx
        sx=ball.sy
        ball.sx=sx
        ball.sy=sy
        
        mods=[]
        if self.y>0 and self.x>0:
            m=self.field.objects[self.x-1][self.y-1]
            if m:
                mods.append(m)
        if self.y<self.field.height-1 and self.x<self.field.width-1:
            m=self.field.objects[self.x+1][self.y+1]
            if m and isinstance(m,Modifier):
                mods.append(m)
        if not mods:
            return
        mval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in mods ]))
        if mval:
            # Flip to SlashWall
            for i in range(0,90):
                self.item.rotate(1)
                self.item.moveBy(9./90.,0)
                QtGui.qApp.processEvents()
            SlashWall(self.field,self.x,self.y)
            self.item.scene().removeItem(self.item)    

class RightSluice(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('rsluice.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    
    def handle(self,ball):
        if ball.sx>0: #Pass ball
            return
        elif ball.sx<0: #Bounce ball
        
            # Evaluate top modifiers
            tval=0
            tmods=[]
            if self.y>0:
                if self.x>0:
                    m=self.field.objects[self.x-1][self.y-1]
                    if m and isinstance(m,Modifier): tmods.append(m)
                if self.x<self.field.width-1:
                    m=self.field.objects[self.x+1][self.y-1]
                    if m and isinstance(m,Modifier): tmods.append(m)
            if tmods:
                tval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in tmods ]))
                
            # Evaluate bottom modifiers
            bval=0
            bmods=[]
            if self.y<self.field.height-1:
                if self.x>0:
                    m=self.field.objects[self.x-1][self.y+1]
                    if m and isinstance(m,Modifier): bmods.append(m)
                if self.x<self.field.width-1:
                    m=self.field.objects[self.x+1][self.y+1]
                    if m and isinstance(m,Modifier): bmods.append(m)
            if bmods:
                bval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in bmods ]))
            
            if bval == tval: # Equal: bounce ball
                ball.sx=-ball.sx
            elif bval: # Go down
                ball.setSpeed(0,1)
            else: # Go up
                ball.setSpeed(0,-1)
                
        else: # Turn ball
            ball.sy=0
            ball.sx=1

class LeftSluice(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('lsluice.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    
    def handle(self,ball):
        if ball.sx<0: # Pass ball
            return
        elif ball.sx>0:
        
            # Evaluate top modifiers
            tval=0
            tmods=[]
            if self.y>0:
                if self.x>0:
                    m=self.field.objects[self.x-1][self.y-1]
                    if m and isinstance(m,Modifier): tmods.append(m)
                if self.x<self.field.width-1:
                    m=self.field.objects[self.x+1][self.y-1]
                    if m and isinstance(m,Modifier): tmods.append(m)
            if tmods:
                tval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in tmods ]))
                
            # Evaluate bottom modifiers
            bval=0
            bmods=[]
            if self.y<self.field.height-1:
                if self.x>0:
                    m=self.field.objects[self.x-1][self.y+1]
                    if m and isinstance(m,Modifier): bmods.append(m)
                if self.x<self.field.width-1:
                    m=self.field.objects[self.x+1][self.y+1]
                    if m and isinstance(m,Modifier): bmods.append(m)
            if bmods:
                bval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in bmods ]))
            
            print tval,bval,tmods,bmods,self.x,self.field.width
                
            if bval == tval: # Equal: bounce ball
                ball.sx=-ball.sx
            elif bval: # Go down
                ball.setSpeed(0,1)
            else: # Go up
                ball.setSpeed(0,-1)
                
        else: # Turn ball
            ball.sy=0
            ball.sx=-1


class DownSluice(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('dsluice.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    
    def handle(self,ball):
        if ball.sy>0:
            return
        elif ball.sy<0:

            # Evaluate left modifiers
            lval=0
            lmods=[]
            if self.x>0:
                if self.y>0:
                    m=self.field.objects[self.x-1][self.y-1]
                    if m and isinstance(m,Modifier): lmods.append(m)
                if self.y<self.field.height-1:
                    m=self.field.objects[self.x-1][self.y+1]
                    if m and isinstance(m,Modifier): lmods.append(m)
            if lmods:
                lval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in lmods ]))
                
            # Evaluate right modifiers
            rval=0
            rmods=[]
            if self.x<self.field.width-1:
                if self.y>0:
                    m=self.field.objects[self.x+1][self.y-1]
                    if m and isinstance(m,Modifier): rmods.append(m)
                if self.y<self.field.height-1:
                    m=self.field.objects[self.x+1][self.y+1]
                    if m and isinstance(m,Modifier): rmods.append(m)
            if rmods:
                rval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in rmods ]))
            
            if lval == rval: # Equal: bounce ball
                ball.sy=-ball.sy
            elif lval: # Go left
                ball.setSpeed(-1,0)
            else: # Go right
                ball.setSpeed(1,0)
        else:
            ball.sy=1
            ball.sx=0


class UpSluice(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('usluice.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    
    def handle(self,ball):
        if ball.sy<0:
            return
        elif ball.sy>0:

            # Evaluate left modifiers
            lval=0
            lmods=[]
            if self.x>0:
                if self.y>0:
                    m=self.field.objects[self.x-1][self.y-1]
                    if m and isinstance(m,Modifier): lmods.append(m)
                if self.y<self.field.height-1:
                    m=self.field.objects[self.x-1][self.y+1]
                    if m and isinstance(m,Modifier): lmods.append(m)
            if lmods:
                lval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in lmods ]))
                
            # Evaluate right modifiers
            rval=0
            rmods=[]
            if self.x<self.field.width-1:
                if self.y>0:
                    m=self.field.objects[self.x+1][self.y-1]
                    if m and isinstance(m,Modifier): rmods.append(m)
                if self.y<self.field.height-1:
                    m=self.field.objects[self.x+1][self.y+1]
                    if m and isinstance(m,Modifier): rmods.append(m)
            if rmods:
                rval=eval('^'.join([ str(mod.mvalue(ball.value)) for mod in rmods ]))
            
            if lval == rval: # Equal: bounce ball
                ball.sy=-ball.sy
            elif lval: # Go left
                ball.setSpeed(-1,0)
            else: # Go right
                ball.setSpeed(1,0)
        else:
            ball.sy=-1
            ball.sx=0

class TextObject(FlipObject):
    def __init__(self,field,x,y,c):
        self.c=c
        FlipObject.__init__(self,field,x,y)

    def graphicsItem(self):
        self.item=QtGui.QGraphicsSimpleTextItem(self.c)
        br=self.item.boundingRect()
        sf=9/br.height()
        self.item.scale(sf,sf)
        self.item.setZValue(1)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item

            
class Generator(TextObject):
    def __init__(self,field,x,y,n):
        TextObject.__init__(self,field,x,y,n)
        self.n=int(n)
        
    def handle(self,ball):
        sx=ball.sx
        sy=ball.sy
        b=Ball(self.field,self.x,self.y,value=self.n)
        b.setSpeed(sx,sy)
        ball.setSpeed(-sx,-sy)
        
class ZeroGen(Generator,Modifier):            
    def __init__(self,field,x,y):
        Generator.__init__(self,field,x,y,'0')
        self.n=0
        
    def mvalue(self,v):
        if v==0:
            return 1
        return 0
            
class PlusTarpit(TextObject,Modifier):
    def __init__(self,field,x,y):
        self.value=None
        TextObject.__init__(self,field,x,y,'+')
    
    def handle(self,ball):
        if self.value==None:
            self.value=ball.value
            ball.kill()
            self.item.setText("+%d"%self.value)
        else:
            ball.setValue(ball.value+self.value)
            self.item.setText("+")
            self.value=None
    def mvalue(self,v):
        if v>0:
            return 1
        return 0

class MulTarpit(TextObject):
    def __init__(self,field,x,y):
        self.value=None
        TextObject.__init__(self,field,x,y,'*')
    
    def handle(self,ball):
        if self.value==None:
            self.value=ball.value
            ball.kill()
            self.item.setText("*%d"%self.value)
        else:
            ball.setValue(ball.value*self.value)
            self.item.setText("*")
            self.value=None
    
class Negate(TextObject,Modifier):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'~')
    def handle(self,ball):
            ball.setValue(-ball.value)
    def mvalue(self,v): return v%2

class Increment(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'++')
    def handle(self,ball):
            ball.setValue(ball.value+1)

class Decrement(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'--')
    def handle(self,ball):
            ball.setValue(ball.value-1)
    
class Reset(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'.')
    def handle(self,ball):
            ball.setValue(0)

class NumOut(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'p')
    def handle(self,ball):
            self.field.output(str(ball.value))
            ball.kill()

class CharOut(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'P')
    def handle(self,ball):
            self.field.output(chr(ball.value))
            ball.kill()

class Terminate(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('terminate.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    def handle(self,ball):
        ball.kill()
        self.field.terminate=True

class Grille(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'#')
    def handle(self,ball):
        if ball.value<=0:
            ball.kill()
class Processor(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('processor.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    def handle(self,ball):
        v=ball.value
        sx1=ball.sy
        sx2=-ball.sy
        sy1=ball.sx
        sy2=-ball.sx
        ball.kill()
        b1=Ball(self.field,self.x,self.y,v)
        b1.setSpeed(sx1,sy1)
        b2=Ball(self.field,self.x,self.y,v)
        b2.setSpeed(sx2,sy2)
        
class Always(TextObject,Modifier):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'@')
    def mvalue(self,v):
        return 1
        
class Random(TextObject,Modifier):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'%')
    def mvalue(self,v):
        v=random.randint(0,1)
        print v
        return v
            
def main():
    app=QtGui.QApplication(sys.argv)
    window=FieldWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

