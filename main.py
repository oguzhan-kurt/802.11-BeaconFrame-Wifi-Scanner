from threading import Thread
from BeaconFrame import dot11BeaconFrame
import controllerFunctions
from rich.live import Live
from rich.table import Table
from signal import SIGINT, signal
from collections import defaultdict
from os import system
import socket



BSSID = set()

SSID_INF    = defaultdict(list)
CHANNEL_INF = defaultdict(list)
DBM_INF     = defaultdict(list)


def unique_BSSID(data):
    BSSID.add(data[0])
    return BSSID

def data_grouping(data):
    _BSSID = unique_BSSID(data)
    _BSSID_List = list(_BSSID)

    if data[0] in _BSSID_List:
        SSID_INF[data[0]].append(data[1])
        CHANNEL_INF[data[0]].append(data[2])
        DBM_INF[data[0]].append(data[3])

    return SSID_INF,CHANNEL_INF,DBM_INF

#Data Print
def generate_table(data) -> Table:
    """Make a New Table"""

    table = Table()

    table.add_column("BSSID")
    table.add_column("SSID")
    table.add_column("Channel")
    table.add_column("dBM")

    _SSID,_CHANNEL,_DBM = data_grouping(data)

    for MAC_ADDR in list(BSSID):
        for NAME in _SSID.items():
            if NAME[0] == MAC_ADDR:
                for CHANNEL in _CHANNEL.items():
                    if CHANNEL[0] == MAC_ADDR:
                        for DBM in _DBM.items():
                            if DBM[0] == MAC_ADDR:
                                table.add_row(f"{MAC_ADDR}",f"{NAME[1][0]}",f"{CHANNEL[1][-1]}",f"{DBM[1][-1]}")
                                if len(NAME[1]) > 3:
                                    NAME[1].pop(0)
                                    CHANNEL[1].pop(0)
                                    DBM[1].pop(0)
    return table


#Get Data and Update
def start_program(interface):
    BEACON_FRAME = dot11BeaconFrame()
    with socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x0003)) as sock:
        sock.bind((str(interface),0x0003))
        with Live(refresh_per_second=4,screen=False) as live:
            while True:
                RAW_DATA = sock.recvfrom(2048)[0]
                BEACON_DATA = BEACON_FRAME.dot11Header_Beacon(RAW_DATA)
                if BEACON_DATA != None:
                    live.update(generate_table(BEACON_DATA))



if __name__ == "__main__":
    
    signal(SIGINT,controllerFunctions.signal_handler)
    
    #Check Root
    controllerFunctions.check_root()

    #Clear Screen
    system("clear")

    #Get Interface from user
    get_user_parameter = controllerFunctions.user_parameters()
    _interface = get_user_parameter._interface
    
    monitor_mode = controllerFunctions.set_monitor_mode(_interface)
    t1 = Thread(target=start_program,args=(monitor_mode,))

    #Different Channel Listening
    t2 = Thread(target=controllerFunctions.listen_channel,args=(monitor_mode,),daemon=True)
    
    t1.start()
    t2.start()
