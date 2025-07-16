'''
Dealing with shared data so that both cores do not try to access the same data at the same
time.  

'''
import machine, _thread, time

Shared_Var = 0           #This is a variable both cores will access

def core_1():             #This function will be run in the second core
    global Shared_Var     #because it is started with the _thread.start command
    Counter = 0
    while True:	                            #Endless loop
        Counter += 1                        #increment a counter 
        time.sleep(.5)                      #take a break
        Shared_Var = 0                      #reset Shared_Var to zero
        while Shared_Var < 500000:          #loop 500,000 times
            Shared_Var += 1                 #incrementing Shared_Var to 500,000
        Shared_Var = Shared_Var + Counter   #add in the level 1 loop counter
        

#main code
_thread.start_new_thread(core_1,()) #Starts the thread running in core 1

while True:
    time.sleep(.25)
    print(Shared_Var)







