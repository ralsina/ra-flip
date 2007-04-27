#!/usr/bin/env python

import sys
from PyQt4 import QtCore,QtGui,QtSvg

from Ui_field import Ui_Form

delay=100

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

processor2='''\
  3 \\ 
  /  '''

  
class FieldWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        data=processor
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
        print lines
        self.width=len(lines[0])
        self.height=len(lines)
        print self.width,self.height
        self.objects=[ [ None for y in range (0,self.height) ] for x in range(0,self.width)]
        print self.objects
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
                elif char in "0123456789":
                    Generator(self,x,y,char)
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
                    
                x+=1 
            y+=1
            
        print self.objects
        
        
    def setupBoard(self):
        for i in range(0,self.width):
            for j in range(0,self.height):
                FlipObject(self,i,j)
                pass
        self.objects=[ [ None for y in range (0,self.height) ] for x in range(0,self.width)]
                
        
    def addItem(self,item):
        print "Field::addItem"
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
        print x,y,self.field.objects[x][y]
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

class HorizWall(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('hwall.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item

    def handle(self,ball):
        ball.sy=-ball.sy
        
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

class RightSluice(FlipObject):
    def graphicsItem(self):
        self.item=QtSvg.QGraphicsSvgItem('rsluice.svg')
        self.item.setZValue(1)
        self.item.scale(0.009,0.009)
        self.item.setPos(10*self.x+.5,10*self.y+.5)
        return self.item
    
    def handle(self,ball):
        if ball.sx>0:
            return
        elif ball.sx<0:
            ball.sx=-ball.sx
        else:
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
        if ball.sx<0:
            return
        elif ball.sx>0:
            ball.sx=-ball.sx
        else:
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
            ball.sy=-ball.sy
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
            ball.sy=-ball.sy
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
        print "Generator.handle"
        sx=ball.sx
        sy=ball.sy
        b=Ball(self.field,self.x,self.y,value=self.n)
        b.setSpeed(sx,sy)
        ball.setSpeed(-sx,-sy)
        
class PlusTarpit(TextObject):
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
    
class Negate(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'~')
    def handle(self,ball):
            ball.setValue(-ball.value)

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

class Terminate(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'Q')
    def handle(self,ball):
        ball.kill()
        self.field.terminate=True

class Grille(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'#')
    def handle(self,ball):
        if ball.value<=0:
            ball.kill()
class Processor(TextObject):
    def __init__(self,field,x,y):
        TextObject.__init__(self,field,x,y,'X')
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
        
                
            
def main():
    app=QtGui.QApplication(sys.argv)
    window=FieldWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

