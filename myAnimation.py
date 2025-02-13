from PyQt5.QtCore import QTimer

class myAnimation:
    def __init__(self,object):
        self.object=object
        self.x=object.geometry().x()
        self.y=object.geometry().y()
        self.h=object.geometry().height()
        self.w=object.geometry().width()
        self.incrimentation_y=0
        self.incrimentation_x=0
        self.percentage=0
        self.cumule=0
        self.x_juge=0
        self.y_juge=0
        self.juge_winner=0
        self.styleSheet=object.styleSheet()
        self.bordersize=0
        

    ######################################################################  
    def moveTo(self,x,y,speed):
        if x-self.x <0:
            self.incrimentation_x=-1
        else :
            self.incrimentation_x=1
        if y-self.y <0:
            self.incrimentation_y=-1
        else :
            self.incrimentation_y=1
        self.x_juge=(x-self.x)*self.incrimentation_x
        self.y_juge=(y-self.y)*self.incrimentation_y

        if self.x_juge>self.y_juge:
            self.percentage=(self.y_juge)/(self.x_juge)
            self.juge_winner=self.x_juge
        else:
            self.percentage=(self.x_juge)/(self.y_juge)
            self.juge_winner=self.y_juge
            
        self.cumule=self.percentage
        
        def move_():
            if self.juge_winner==self.x_juge:
                self.incrimentation_y=int(self.cumule)
                self.cumule=self.cumule-int(self.incrimentation_y) 

            else:
                self.incrimentation_x=int(self.cumule)
                self.cumule=self.cumule-int(self.incrimentation_x) 
            self.object.move(self.x+self.incrimentation_x,self.y+self.incrimentation_y)
            self.y=self.y+self.incrimentation_y
            self.x=self.x+self.incrimentation_x
            self.cumule=self.cumule+self.percentage

        for i in range((self.juge_winner)):
            QTimer.singleShot(i*speed,move_)
            

    ##########################################################################   
    def R_Move(self,distance,speed):
        self.moveTo(self.x+distance,self.y,speed)
     
    def L_Move(self,distance,speed):
        self.moveTo(self.x-distance,self.y,speed)
        
    def U_Move(self,distance,speed):
        self.moveTo(self.x,self.y-distance,speed)
        
    def D_Move(self,distance,speed):
        self.moveTo(self.x,self.y+distance,speed)
    ###########################################################################
    def increase_width(self,plus,speed,direction="r"):
        if plus>=0:
            step=1
        else:
            step=-1
        def increase(direction,step):
            self.w+=step
            if direction=="l":
                self.x=self.x-1*step
            self.object.setGeometry(self.x,self.y,self.w,self.h)
        for i in range (int(plus*step)):
            QTimer.singleShot(i*speed,lambda:increase(direction,step))
            
    #############################################################################
    def increase_height(self,plus,speed,direction="d"):
        if plus>=0:
            step=1
        else:
            step=-1
        
        def increase(direction,step):
            self.h+=step
            if direction=="u":
                self.y=self.y-1*step
            self.object.setGeometry(self.x,self.y,self.w,self.h)
        for i in range (int(plus*step)):
            QTimer.singleShot(i*speed,lambda:increase(direction,step))
    #############################################################################
    def increase_border(self,plus,speed,previousValue=0):
        self.bordersize=previousValue
        if plus>=0:
            step=1
        else:
            step=-1
        def increase(step):
            self.bordersize+=step
            print(self.styleSheet)
            self.object.setStyleSheet(self.styleSheet+"QLabel{ border:"+str(self.bordersize)+"px solid black;}")
        for i in range(int(plus*step)):
            QTimer.singleShot(i*speed,lambda:increase(step))
    #############################################################################""""
    def scrollDown(self,speed,distance):
        def scrollStep():
            current_scroll_value = self.object.verticalScrollBar().value()
            self.object.verticalScrollBar().setValue(current_scroll_value + 1)

        # Effectuer 100 étapes de défilement à intervalle de 100 ms
        for i in range(int(distance)):
            QTimer.singleShot(i*speed, scrollStep)
    ##############################################################################""
    def scrollUp(self,speed,distance):
        def scrollStep():
            current_scroll_value = self.object.verticalScrollBar().value()
            self.object.verticalScrollBar().setValue(current_scroll_value - 1)

        # Effectuer 100 étapes de défilement à intervalle de 100 ms
        for i in range(int(distance)):
            QTimer.singleShot(i*speed, scrollStep)
    ##########################################################################""       
    def scrollLeft(self,speed,distance):
        def scrollStep():
            current_scroll_value = self.object.horizontalScrollBar().value()
            self.object.horizontalScrollBar().setValue(current_scroll_value - 1)

        # Effectuer 100 étapes de défilement à intervalle de 100 ms
        for i in range(int(distance)):
            QTimer.singleShot(i*speed, scrollStep)
    ##############################################################################""
    def scrollRight(self,speed,distance):
        def scrollStep():
            current_scroll_value = self.object.horizontalScrollBar().value()
            self.object.horizontalScrollBar().setValue(current_scroll_value + 1)

        # Effectuer 100 étapes de défilement à intervalle de 100 ms
        for i in range(int(distance)):
            QTimer.singleShot(i*speed, scrollStep)
        
            
        
        


        
        