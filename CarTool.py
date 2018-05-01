import serial
import csv
import time
from datetime import datetime
import string

'''
Code Written by: Ziwei Peng
CS483: Digital Forensics
'''

def connectSerial(port, baud, car, monitorAll, outfile):
    res = []
    con = serial.Serial(port)
    con.baudrate = 115200
    initflag = False
    setupListCAN = ['ATZ','ATL1','ATH1','ATAL','ATS1','ATSP0']
    setupListISO = ['ATZ','ATL1','ATH1','ATAL','ATS1','ATSI','ATSP3']
    PIDS = ['0902','010C','0904','0906'] # for report
    try:

        # Initialize OBD
        if not initflag:
            setupList = []
            if car != "Toyota":
                setupList = setupListCAN
            else:
                setupList = setupListISO
            for entry in setupList:
                con.write( bytes((entry + '\r\n').encode()) )
                con.timeout = 1
                log = con.read(1024).decode()
                print(log)
            if monitorAll:
                con.write( bytes(('ATMA\r\n').encode()) )
                con.timeout = 1
                res = con.read(4096).decode()
        for entry in PIDS:
            con.write( bytes((s + '\r\n').encode()) )
            con.timeout = 1
            res.append(con.read(4096).decode())

    except:
        con.close()
        print('<<<<< Connection Ended >>>>>')

    with open(outfile, 'w') as outf:
        for entry in res:
            outf.write(res + '\n')


if __name__ == "__main__":
    port = '/dev/ttyUSB0'
    # Common Baud Rates:
    # 14400, 9600, 38400, 115200
    baud = 115200
    # Honda, Subaru, or Toyota
    car = "Honda"
    monitorAll = False
    #outfile = "Report_" + car + str(datetime.now()) + '.txt'
    outfile = car + '.txt'
    connectSerial(port, baud, car, monitorAll, outfile)
