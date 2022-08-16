from optparse import OptionParser
from itertools import cycle
from time import sleep
from subprocess import Popen,PIPE
import sys,os


def listen_channel(iface):
    channl = [8,9,4,6,5,7,2,1,10,11,3]
    for i in cycle(channl):
        sleep(0.5)
        os.system("iwconfig " + iface + " channel " + str(i))

def user_parameters():
    parser = OptionParser()
    parser.add_option("-i","--interface",dest="_interface",help="Enter Your Wireless Network Interface",type=str)
    _option = parser.parse_args()[0]
    if not _option._interface:
        print("\nPlease Enter Interface !!\n")
        sys.exit(1)

    return _option


###### Check root
def check_root():
	if not os.geteuid()==0:
		print("\n\033[0;30;47mYou must run this script with root privilages !!\033[0m")
		exit(1)
    
    
###### Set up Wireless interface in monitor mode.
def set_monitor_mode(iface):
    print("\n>> Checking Settings...\n")
    proc = Popen(['iwconfig'], stdout=PIPE, stderr=PIPE)
    for i in proc.communicate():
        results = i.decode("utf-8").split(" ")
    
        if 'Mode:Monitor' in results:
            return iface
        else:
            print("\n[+]Setting Monitor Mode")
            os.system("ifconfig " + iface + " down")
            try:
                os.system("iwconfig "+iface+" mode monitor")
            except:
                print("Failed to Setup your interface in monitor mode")
                sys.exit(1)
            os.system("ifconfig " + iface + " up")
            print("\n[+]Successed!\n")
            return iface


###### if the user chooses to terminate it with a CTRL + C and provide the user with an appropriate message.
def signal_handler(signal,frame):
    print("\n Execution Aborted By User \n")
    os.system("kill -9 " + str(os.getpid()))
    sys.exit(1)
