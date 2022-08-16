from struct import unpack
from binascii import hexlify

class dot11BeaconFrame(object):

    def radioTabHeader(self,Rawdata):
        # 18 Byte RadioTab Header
        radioHeader = Rawdata[:18]
        
        #Byte 12-13th Field = Channel Frequency
        rawDataFreq = radioHeader[10:12]

        #Little-Endian => "<"
        channelFreq = unpack("<h",rawDataFreq)

        #Byte 15 = dbM
        rawDataDbm = radioHeader[14:15]
        #network (= big-endian) => "!"
        dbM = unpack("!b",rawDataDbm)

        return dbM[0],channelFreq[0]
    
    def dot11Header_Beacon(self,data):
    
        dbM,channelFreq = self.radioTabHeader(data)
    
        #24 Byte = dot11 Header Size
        dot11BeaconFrame = data[18:42]
        
        #b'\x80'(1 Byte)== 802.11 Sub_Frame Type : Beacon
        if dot11BeaconFrame[0:1] == b'\x80':

            #BSSID Field : 6 Byte & 10-16th Field
            rawBSSID = dot11BeaconFrame[10:16]
            _bssid = unpack("!6s",rawBSSID)
            
            #Convert The Binary To Hexadecimal
            bssid = hexlify(_bssid[0],":")

            #Management Frame
                #Fixed Parameters  == 12 Byte
                #Tagged Parameters == Not Constant Value
            dot11ManegementFrame = data[42:]

            #SSID Field Size Max : 32 Byte & 13-14th Field
            tag_size = dot11ManegementFrame[13:14]
            ssidLenght = unpack("!b",tag_size)

            #SSID & SSID Parse
            rawSSID = dot11ManegementFrame[14:14+ssidLenght[0]]
            _ssid = unpack(f"!{ssidLenght[0]}s",rawSSID)
            ssid = _ssid[0]

            return str(bssid.decode()).upper(),str(ssid.decode()),self.channelFrequencyRange(channelFreq),str(dbM)
        else:
            return None
    
    def channelFrequencyRange(self,frequency):
        channel = None
        if frequency == 2412:
            channel = 1
        elif frequency == 2417:
            channel = 2
        elif frequency == 2422:
            channel = 3
        elif frequency == 2427:
            channel = 4
        elif frequency == 2432:
            channel = 5
        elif frequency == 2437:
            channel = 6
        elif frequency == 2442:
            channel = 7
        elif frequency == 2447:
            channel = 8
        elif frequency == 2452:
            channel = 9
        elif frequency == 2457:
            channel = 10
        elif frequency == 2462:
            channel = 11
        elif frequency == 2467:
            channel = 12
        elif frequency == 2472:
            channel = 13
        elif frequency == 2484:
            channel = 14
        return channel
