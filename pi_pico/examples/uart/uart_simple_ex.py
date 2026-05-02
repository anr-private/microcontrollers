#
#
# Uses a single UART as a loopback: sends out the TX pin and receives on the RX pin.

import sys
import time
from machine import UART, Pin

# UARTs tested:
#  UART 1  GPIO 4,5 as Tx,Rx   Connect GPIO4 <--> GPIO5


def test_1():
    print("=== TEST 1  ---  simple basic send / receive  =================")
    
    ###uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

    print(f" UART is {uart}")

    mesg = "Hello there!"
    print(f"Sending '{mesg}'  len={len(mesg)}")
    uart.write(mesg)

    # wait
    ###time.sleep(0.1)

    # Receive
    ###print(f"uart.any() is {uart.any()}")
    ctr = 0
    nchars_recvd = 0
    while 1:
        if uart.any():
            data = uart.read()
            decoded = data.decode('utf-8')
            nchars_recvd += len(decoded)
            print(f"RECVD: '{decoded}'   when {ctr=}.   {nchars_recvd=}")
            if nchars_recvd >= len(mesg):
                print(f"  RECEIVED ALL CHARS of the mesg. Stop!")
                break
        # Wait until we receive
        ctr += 1
        if ctr > 50000:
            print(f"   ctr is {ctr}.  Stopping")
            break
    print("=== end of TEST 1  ============================\n")


def test_2():
    print("=== TEST 2  ---  Send chars one at a time, with sleep in between each  =================")
    
    ###uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

    print(f" UART is {uart}")


    # wait
    ###time.sleep(0.1)

    # Receive
    print(f"uart.any() is {uart.any()}")
    ctr = 0
    tx_pos = 0
    tx_chars = "THIS IS TEST 2"
    nchars_recvd = 0
    while 1:
        if  tx_pos >= len(tx_chars):
            print(f"   --- sent all {len(tx_chars)} chars; end of test")
            if nchars_recvd >= len(tx_chars):
                print(f"        Received all chars that were sent")
            else:
                print(f"       FAILED TO RECEIVE ALL CHARS.  sent={len(tx_chars)}   received={nchars_recvd}")
            break
        ch = tx_chars[tx_pos]
        tx_pos += 1
        
        uart.write(ch)
        
        ctr = 0
        while 1:
            if uart.any():
                data = uart.read()
                decoded = data.decode("UTF-8")
                nchars_recvd += len(decoded)
                print(f"RECVD: {decoded}")
                break
            # wait for the data 
            ctr += 1
            if ctr > 100000:
                print(f"   ctr is {ctr}.  Stopping - NOTHING RECEIVED")
                break
            
    print("=== end of TEST 2  ============================\n")

def main(args):
    test_1()
    test_2()
    
    
if __name__ == "__main__":
    main(sys.argv[1:0])
    
###

