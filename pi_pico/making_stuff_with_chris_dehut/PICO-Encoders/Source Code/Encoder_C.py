#This library contains a class that can be used with rotary encoders or other quadrature signals
#It is entireley in MicroPython and therefore not very efficient.  It is very suitable for using
#with rotary encoder switches and other encoders.  The limitiation is about 1000 counts per second.
#To determine max RPM of an an encoder this can handle:
# ECPR = Encoder counds per revolution - many rotary encoder swtiches have 20 detents and thus, 80 counts per rev
# IrqT = Time in microseconds to process a count
# TPR  = Time Per Revolution of processing time
# ECPR = 80
# IrqT = .0001
# TPR  = ECPR * IrqT = .008 seconds per revolution
# Max RPM = 1 / TPR  = 125

import machine

class R_Encoder:
   
    def __init__(self, A_Pin, B_Pin):
        self.A_Pin = A_Pin
        self.B_Pin = B_Pin
        self.Enc_Counter = 0
        self.Enc_A_State = 0
        self.Enc_A_State_old = 0
        self.Enc_B_State = 0
        self.Enc_B_State_old = 0
        self.error = 0

        self.Setup_Irqs()    
           
    def DisplayPins(self):
        print("A_Pin = ",self.A_Pin,"  B_Pin = ",self.B_Pin)

    def Reset_Counter(self):
        self.Enc_Counter = 0
        
    def Enc_Handler(self, Source):
        self.Enc_A_State = self.Enc_Pin_A.value()  #Capture the current state of both A and B
        self.Enc_B_State = self.Enc_Pin_B.value()
        
        if self.Enc_A_State == self.Enc_A_State_old and self.Enc_B_State == self.Enc_B_State_old:  #Probably 'bounce" as there was a trigger but no change
            self.error += 1  #add the error event to a variable - may by useful in debugging
        elif (self.Enc_A_State == 1 and self.Enc_B_State_old == 0) or (self.Enc_A_State == 0 and self.Enc_B_State_old == 1):
            # this will be clockwise rotation
            # A   B-old
            # 1 & 0 = CW rotation
            # 0 & 1 = CW rotation
            self.Enc_Counter += 1  #Increment counter by 1 - counts ALL transitions
        elif (self.Enc_A_State == 1 and self.Enc_B_State_old == 1) or (self.Enc_A_State == 0 and self.Enc_B_State_old == 0):
            # this will be counter-clockwise rotation
            # A   B-old
            # 1 & 1 = CCW rotation
            # 0 & 0 = CCW rotation
            self.Enc_Counter -= 1 # Decrement counter by 1 - counts ALL transitions
        else:  #if here, there is a combination we don't care about, ignore it, but track it for debugging
            self.error += 1
        self.Enc_A_State_old = self.Enc_A_State     # store the current encoder values as old values to be used as comparison in the next loop
        self.Enc_B_State_old = self.Enc_B_State       

        
    def Setup_Irqs(self):
        #Configure the A channel and B channel pins and their associated interrupt handing
        self.Enc_Pin_A = machine.Pin(self.A_Pin,machine.Pin.IN,machine.Pin.PULL_DOWN)
        self.Enc_Pin_A.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.Enc_Handler)
        self.Enc_Pin_B = machine.Pin(self.B_Pin,machine.Pin.IN,machine.Pin.PULL_DOWN)
        self.Enc_Pin_B.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.Enc_Handler)

        #Preset some variables to useful and known values
        self.Enc_A_State_old = self.Enc_Pin_A.value()
        self.Enc_B_State_old = self.Enc_Pin_B.value()
# #--------------------------------------------------------------------------------------------------------------------
