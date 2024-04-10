# 這是用來控制plc的各種裝置, 包括輸送帶(conveyor), 馬達(motor)等
# 這個部份是copy自ROS系統, 出自milo之手

import socket
import time

HOST_NAME = '192.168.33.100'
TCP_PORT = 500

START_BYTE = '\x02'
SLAVE_NO = '01'
CMD_SINGLE_DISCRETE_CONTROL = '42'
CMD_READ_ENABLE_STATUS = '43'
CMD_WRITE_STATUS = '45'
CMD_READ_STATUS = '44'
CMD_READ_DATA_REGISTERS = '46'
CMD_WRITE_DATA_REGISTERS = '47'
CMD_RUN = '41'
PLC_RUN = '1'
PLC_STOP = '0'
END_BYTE = '\x03'

ErrorCode_Free = '0'


class CmdFatek:
    CONVEYOR_ON = 3
    CONVEYOR_OFF = 4

class FatekControl(object):
    def __init__( self, slaveNo = SLAVE_NO, host=HOST_NAME,port=TCP_PORT):
        self.client = None
        self.slaveNo = slaveNo
        self.server_addr = (HOST_NAME, TCP_PORT)
        self.socketisConnected = self.connect2SocketServer()
        
        return 


    #======================================================================================================================================================
    # write start run command to PLC
    def StartRunPLC(self):
        writeDataBuffer = START_BYTE + self.slaveNo + CMD_RUN + PLC_RUN
        checksum = self.calculateCheckSum(writeDataBuffer)
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        recv = self.writeData(writeDataBuffer)
    
        # check PLC response
        temp = START_BYTE + self.slaveNo + CMD_RUN +ErrorCode_Free
        checksum = self.calculateCheckSum(temp)
        temp += checksum
        temp += END_BYTE
        if len(recv) == 0:
            return False
        if recv == temp:
            return True
        else:
            return False


    #======================================================================================================================================================
    # write stop run command to PLC    
    def StopPLC(self):
        writeDataBuffer = START_BYTE + self.slaveNo + CMD_RUN + PLC_STOP
        checksum = self.calculateCheckSum(writeDataBuffer)
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        recv = self.writeData(writeDataBuffer)

        # check PLC response
        temp = START_BYTE + self.slaveNo + CMD_RUN +ErrorCode_Free
        checksum = self.calculateCheckSum(temp)
        temp += checksum
        temp += END_BYTE
        if len(recv) == 0:
            return False
        if recv == temp:
            return True
        else:
            return False
    

    #======================================================================================================================================================
    # Command code is '42'
    def controlSingleDiscrete(self, discreteNo, control):
        if discreteNo[0] != 'Y' and discreteNo[0] != 'X' and discreteNo[0] != 'M':
            print(discreteNo[0])
            return False

        writeDataBuffer = START_BYTE + self.slaveNo + CMD_SINGLE_DISCRETE_CONTROL + str(control) + discreteNo
        checksum = self.calculateCheckSum(writeDataBuffer)
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        recv = self.writeData(writeDataBuffer)

        checkBuffer = START_BYTE + self.slaveNo + CMD_SINGLE_DISCRETE_CONTROL + ErrorCode_Free
        checksum = self.calculateCheckSum(checkBuffer)
        checkBuffer += checksum
        checkBuffer += END_BYTE
        
        if(checkBuffer == recv):
            return True
        else:
            return False


    #======================================================================================================================================================
    # Command code is '45'
    def writeStatus(self,startNo = 'Y0000',list = [0]):
        # check the data length is in range 255
        if len(list) > 255:
            return False

        statusNumber = str(len(list)).zfill(2)
        writeDataBuffer = START_BYTE + self.slaveNo + CMD_WRITE_STATUS  + statusNumber + startNo
        for value in list:
            writeDataBuffer += str(value)
        checksum = self.calculateCheckSum(writeDataBuffer)
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        recv = self.writeData(writeDataBuffer)

        return recv


    #======================================================================================================================================================
    # Command code is '44'
    def readStatus(self,startNo = 'Y0000',length=1):
        datalength = ('%X'%length).zfill(2)
        writeDataBuffer = START_BYTE + self.slaveNo + CMD_READ_STATUS  + datalength + startNo
        checksum = self.calculateCheckSum(writeDataBuffer)
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        recv = self.writeData(writeDataBuffer)

        return recv


    #======================================================================================================================================================
    # Command code is '46'
    def readDataRegistor(self,startNo = 'D00000',length=1):
        datalength = str(length).zfill(2)
        writeDataBuffer = START_BYTE + self.slaveNo + CMD_READ_DATA_REGISTERS + datalength + startNo
        checksum = self.calculateCheckSum(writeDataBuffer)
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        print(writeDataBuffer)
        recv = self.writeData(writeDataBuffer)

        return recv


    #======================================================================================================================================================
    # Command code is '47'
    def writeDataRegistor(self,startNo = 'D00000',list = [0]):
        registerNumber = str(len(list) * 4).zfill(2)
        writeDataBuffer = START_BYTE + self.slaveNo + CMD_WRITE_DATA_REGISTERS + registerNumber + startNo
        
        for value in list:
            writeDataBuffer += '%04X' % value
        checksum = self.calculateCheckSum(writeDataBuffer)
        
        writeDataBuffer += checksum
        writeDataBuffer += END_BYTE
        recv = self.writeData(writeDataBuffer)

        return recv


    #======================================================================================================================================================
    def calculateCheckSum(self,input):
        temp = 0
        for chr in input:
            temp += ord(chr)
        checksum = hex(temp)
        checksum = checksum[len(checksum)-2:len(checksum)]
        checksum = checksum.upper()

        return checksum


    #=======================================================================================================================================================
    def writeData(self,writeBuffer):
        # print(str)
        self.client.sendall(writeBuffer.encode())
        time.sleep(0.01)
        try :
            readData = self.readData()
            return readData
        except Exception as e:
            print("recv data from socket server is : %s" %e)


    #================================================read the socket buffer and decode it
    def readData(self):
        readData = self.client.recv(1024)
        return readData.decode('utf-8')


    ########################################################################################
    def connect2SocketServer(self):
        try: 
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(0.25)
            self.client.connect(self.server_addr)
            print("Fatek is connected")
            return True

        except Exception as e:
            print("{}".format(e))
            return False
        


if __name__ =="__main__":
    fc = FatekControl()
    # fc.controlSingleDiscrete('M0102', CmdFatek.CONVEYOR_ON)  # on conveyor
    # time.sleep(3)
    fc.controlSingleDiscrete('M0113', CmdFatek.CONVEYOR_ON)  # off conveyor
    time.sleep(1)  # seems remoter must reply the cmd echo? or conveyor would not stop
    