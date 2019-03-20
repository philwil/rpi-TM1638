#this one connects to a port / socket
# coding=utf-8
from time import sleep
from rpi_TM1638 import TMBoards
import socket
import select
import sys

#GPIO6 STP pin31
#GPI13 CLK pin33
#GPI19 DIO pin35

# my GPIO settings (two TM1638 boards connected on GPIO19 and GPIO13 for DataIO and Clock; and on GPIO06 and GPIO26 for the STB)
DIO = 19
CLK = 13
#STB = 06, 26
STB = 06

# instanciante my TMboards
TM = TMBoards(DIO, CLK, STB, 0)

TM.clearDisplay()

# some LEDs manipulation
TM.leds[0] = True       # turn on led 0 (1st led of the 1st board)
TM.leds[6] = True      # turn on led 12 (5th led of the 2nd board, since there is 8 leds per board)

TM.segments[1] = '0'        # display '0' on the display 1 (2nd 7-segment display of the 1st board)
TM.segments[4] = '98.76'     # display '9876' on the 7-segment display number 4, 5, 6 and 7 (the point is on segment 5)
TM.segments[3,1] = True     # turn on the segment #1 of the 7-segment number 3

#TM.segments[8] = '01234567'
#TM.leds = (True, False, True)   # set the three first leds

sval = 12.34

print __name__
if __name__ == "__main__":
    NODE,HOST,PORT = "LEDS1","pine64-001",5541
    if len(sys.argv) >= 4:
        print "Correct usage: script, NODEIP address, port number"
        NODE= str(sys.argv[1])
        HOST= str(sys.argv[2])
        PORT = int(sys.argv[3])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    
    msg = "set " + NODE + ":led1 off\n"
    server.send(msg)
    print msg
    msg = "set " + NODE + ":led2 off\n"
    server.send(msg)
    print msg
    msg = "set " + NODE + ":led3 off\n"
    server.send(msg)
    print msg
    msg = "set " + NODE + ":led4 off\n"
    server.send(msg)
    print msg
    


    
    while True:
        #
        l = 0
        lasta = 0
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]
    
        """ There are two possible input situations. Either the
        user wants to give manual input to send to other people,
        or the server is sending a message to be printed on the
        screen. Select returns from sockets_list, the stream that
        is reader for input. So for example, if the server wants
        to send a message, then the if condition will hold true
        below.If the user wants to send a message, the else
        condition will evaluate as true"""

        read_sockets,write_socket, error_socket =\
                          select.select(sockets_list,[],[],1)
        TM.segments[4] = str(sval)
        sval = sval+0.02
        print "select done"
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print message
                sleep(0.5)
            else:
                message = sys.stdin.readline()
                server.send(message)
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()

                
        msg = "get " + NODE + ":led4\n"
        server.send(msg)
        print msg

        TM.leds[l] = False
        l = l+1
        if l > 7:
            l = 0
        TM.leds[l] = True
        
        a=TM.getData(0)
        b=TM.getData(0)
        if l == 2:
            print b
            print a
            for x in a:
                print x
            
        # 	b=TM.getData(1)
        #TM.segments[0] = ''.join("%02d"%x for x in a)
        # 	TM.segments[8] = ''.join("%02d" % x for x in b)
        #sleep(0.1)


