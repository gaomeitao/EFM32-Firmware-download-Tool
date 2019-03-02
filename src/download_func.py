#coding:=utf-8

import time
import sys
import serial
import serial.tools.list_ports
import os
from xmodem import XMODEM
#for test
import binascii
#import gui

###0 ->COM1  3->COM4

class dl_service:
    def __init__(self,ui,logsave):
        self.usb_port="Silicon"
        self.uart_port = "USB-to-Serial"
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.timeout = 1
        self.remain = 0
        self.sendcount = 0
        self.filesize = 0
        self.ui = ui
        self.modem = XMODEM(self.getc, self.putc)
        self.logsave = logsave
        if self.logsave == True:
            self.create_log_file()
    def create_log_file(self):
        path = os.getcwd()
        new = os.path.join(path, "saveFlashToolLog.txt")
        self.filesavepath = new
        fp = open(new, 'a+')
        filehead = "Save Begin :" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        filehead = filehead + "\n\r"
        fp.write(filehead)
        fp.close()
    def save_log_to_file(self,text):
        if self.logsave == True:
            fp = open(self.filesavepath,'ab+')
            str_file = text + "\n"
            fp.write(str_file)
            fp.close()
        else:
            print text

    def find_uart_port(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            self.save_log_to_file("The Serial port can't find!")
            return "false"
        for i in range (len(port_list)):
            print port_list[i]
            if port_list[i][1].find(self.uart_port) != -1:
                return port_list[i][0]
        return "false"
    def find_usb_port(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            self.save_log_to_file("The USB port can't find!")
            return "false"
        for i in range (len(port_list)):
            print port_list[i]
            if port_list[i][1].find(self.usb_port) != -1:
                return port_list[i][0]
        return "false"
    def second_delay(self,timeout):
        while timeout > 0:
            timeout=timeout-1
            time.sleep(1)
    def set_comm_port(self,number):
        self.ser.port = number
    def waiting_usb_comport_enmu(self,timeout):
        while timeout > 0:
            timeout=timeout-1
            usb_port = self.find_uart_usb()
            if usb_port != "false":
                print usb_port
                self.ser.port = int(usb_port[3:]) - 1
                return True
            else:
                self.save_log_to_file('waiting_usb_comport_enmu='+timeout)
                time.sleep(1)
        if timeout == 0:
            self.save_log_to_file("Can't find any download usb comport!")
        return False
    def open_comport(self):
        if self.ser.isOpen() != True:
            try:
                ret = self.ser.open()
            except Exception,e:
                print "Excettion "
                return False
            if None == ret:
                 self.save_log_to_file('ComPort Open success!')
                 return True
            else:
                self.save_log_to_file('ComPort Open failed!')
                return False
    def close_comport(self):
        self.save_log_to_file('ComPort Close!')
        self.ser.close()

    def getc(self,size,timeout =1):
        return self.ser.read(size) or None

    def putc(self,data,timeout =1):
        self.sendcount = self.sendcount + 1
        self.remain = self.sendcount * 128 * 100/ self.filesize
        if self.remain >= 100:
            self.remain = 100
        self.ui.download_info_delete()
        self.ui.download_info_show('Download Progress ..........'+ str(self.remain) + '%')
        #print "%s"%(data)
       # print binascii.hexlify(data)
        return self.ser.write(data) # note that this ignores the timeout

    def handshake_with_target(self,timeout):
        self.save_log_to_file('handshake_with_target')
        while timeout > 0:
            timeout=timeout-1
            ret = self.sendcomand('U')
            if ret == False:
                return False
            time.sleep(2)
            len = self.ser.inWaiting()
            strR = self.ser.read(len)
            print strR
            if strR.find('BOOTLOADER') != -1:
                self.save_log_to_file("Terminal go into Bootloader Mode Now!")
                return True
            else:
                self.ui.download_info_delete()
                display = "Handshake With Target By UART................" + str(timeout)
                self.ui.download_info_show(display)
                time.sleep(1)
        if timeout == 0:
            self.save_log_to_file("handshake_with_target failed!")
        return False
    def download_command_send(self):
        self.save_log_to_file('download_command_send')
        ret = self.sendcomand('u')
        if ret == False:
            return False
        time.sleep(2)
        ln = self.ser.inWaiting()
        rd = self.ser.read(ln)
        print rd
        if rd.find("Ready") != -1:
            self.save_log_to_file('Read to download bin file Now!')
            return True
        else:
            self.save_log_to_file('u command  Doesn\'t responce!')
            return False
    def app_download_command_send(self,timeout):
        while timeout > 0:
            timeout=timeout-1
            ret = self.sendcomand('u')
            if ret == False:
                return False
            time.sleep(2)
            len = self.ser.inWaiting()
            rd = self.ser.read(len)
            print rd
            if rd.find("Ready") != -1:
                self.save_log_to_file( 'Read to download bin file Now!')
                return True
            else:
                self.save_log_to_file('u command  Doesn\'t responce! timeout=' + str(timeout))
                time.sleep(1)
        if timeout == 0:
            self.save_log_to_file( 'usb u command send failed!')
        return False

    def bootloader_downloadcommand_send(self,timeout):
        while timeout > 0:
            timeout=timeout-1
            ret = self.sendcomand('d')
            if ret == False:
                return False
            time.sleep(2)
            len = self.ser.inWaiting()
            rd = self.ser.read(len)
            print rd
            if rd.find("Ready") != -1:
                self.save_log_to_file( 'Read to download bootloader file Now!')
                return True
            else:
                self.save_log_to_file('d command  Doesn\'t responce! timeout=' + str(timeout))
                time.sleep(1)
            if timeout == 0:
                self.save_log_to_file('bootloader_downloadcommand_send failed!')
                return False
    def download_bin_send(self,filepath):
        self.save_log_to_file('Downloading  ' + filepath)
        self.sendcount = 0
        self.stream =open(filepath,'rb')
        self.filesize = os.path.getsize(filepath)
        try:
            ret = self.modem.send(self.stream)
        except Exception, e:
            self.save_log_to_file("writeTimeoutError Fail!")
            return False
        if True == ret:
            self.save_log_to_file("Download Success!")
            return True
        else:
            self.save_log_to_file("Download Fail!")
            return False
    def get_bootloader_info(self):
        n = self.ser.write('i')
        time.sleep(1)
        n = self.ser.inWaiting()
        str = self.ser.read(n)
        print str
    def boot_to_application(self):
        self.save_log_to_file( 'Boot up to Application!')
        ret = self.sendcomand('b')
        if ret == False:
            return False
        time.sleep(1)
    def reboot_device(self):
        self.save_log_to_file( 'reboot_device')
        ret = self.sendcomand('r')
        if ret == False:
            return False
        time.sleep(2)
        n = self.ser.inWaiting()
        str = self.ser.read(n)
        print str
    def sendcomand(self,cmd):
        try:
            ret = self.ser.write(cmd)
            self.save_log_to_file(cmd)
        except Exception, e:
            print "Exception sendcomand failed cmd=",
            print cmd
            return False
        return True
    def waitingForReplyOK(self,timeout = 1):
        while timeout > 0:
            timeout = timeout -1
            time.sleep(1)
            n = self.ser.inWaiting()
            str = self.ser.read(n)
            self.save_log_to_file(str)
            if str == "OK":
                return True
            else:
                return False
    def reboot_device_in_standymodem(self):
        if True == self.open_comport():
            command = "AT+BOOTMODE=2"
            self.sendcomand(command)
            time.sleep(3)
            ret = self.waitingForReplyOK(2)
            if ret == True:
                command = "AT+REBOOTMCU"
                ret = self.sendcomand(command)
                if ret == True:
                    time.sleep(3)
                    if True == self.waitingForReplyOK(2):
                        self.close_comport()
                        return True
                    else:
                        self.close_comport()
                        return False
                else:
                    self.close_comport()
                    return False
            else:
                self.close_comport()
                return False
        else:
            return False
    def device_into_specialmode(self,mode):
         command = "AT+BOOTMODE=" + str(mode)
         ret = self.sendcomand(command)
         if ret == False:
             self.ui.util_info_show("Failed into Specialmode")
             return False
         self.ui.util_info_show(command)
         time.sleep(1)
         ret = self.waitingForReplyOK(2)
         if ret == False:
             self.ui.util_info_show("Failed into Specialmode")
             return False
         self.ui.util_info_show("OK")
         return True
    def device_escape_specialmode(self):
         command = "AT+REBOOTMCU"
         ret = self.sendcomand(command)
         self.ui.util_info_show(command)
         time.sleep(3)
         n = self.ser.inWaiting()
         text = self.ser.read(n)
         self.ui.util_info_show(text)
    def read_sn(self):
        command = "AT+GETRUNPARA:MCUSN:"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        n = self.ser.inWaiting()
        sn = self.ser.read(n)
        self.ui.util_info_show(sn)
        if sn != "" and sn != "FAIL":
            data = sn.split(":")
            tmp =data[1]
            return tmp[:-1]
        else:
            return False

    def read_avtcode(self):
        command = "AT+GETRUNPARA:ACTCODE:"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        n = self.ser.inWaiting()
        sn = self.ser.read(n)
        self.ui.util_info_show(sn)
        if sn != "" and sn != "FAIL":
            data = sn.split(":")
            tmp =data[1]
            return tmp[:-1]
        else:
            return False
    def read_delaytime(self):
        command = "AT+GETRUNPARA:DELAYT:"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        n = self.ser.inWaiting()
        sn = self.ser.read(n)
        self.ui.util_info_show(sn)
        if sn != "" and sn != "FAIL":
            data = sn.split(":")
            tmp =data[1]
            return str(int(tmp[:-1])*5)
        else:
            return False
    def read_sendtime(self):
        command = "AT+GETRUNPARA:SendL:"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        n = self.ser.inWaiting()
        sn = self.ser.read(n)
        self.ui.util_info_show(sn)
        if sn != "" and sn != "FAIL":
            data = sn.split(":")
            tmp =data[1]
            return str(int(tmp[:-1])/10)
        else:
            return False
    def read_savetime(self):
        command = "AT+GETRUNPARA:TLSave:"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        n = self.ser.inWaiting()
        sn = self.ser.read(n)
        self.ui.util_info_show(sn)
        if sn != "" and sn != "FAIL":
            data = sn.split(":")
            tmp =data[1]
            return str(int(tmp[:-1])/10)
        else:
            return False
    def write_sn(self,sn):
        command = "AT+SETRUNPARA:MCUSN:" + sn
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def write_actcode(self,avtcode):
        command = "AT+SETRUNPARA:ACTCODE:" + avtcode
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def write_delaytime(self,delaytime):
        val = str(int(delaytime)/5)
        command = "AT+SETRUNPARA:DELAYT:" + val
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def write_savetime(self,savetime):
        val = str(int(savetime) * 10)
        command = "AT+SETRUNPARA:TLSave:" + val
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def write_sendtime(self,sendtime):
        val = str(int(sendtime) * 10)
        command = "AT+SETRUNPARA:SendL:" + val
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def systemreset(self):
        command = "AT+SETRUNPARA:SYSRST:"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(1)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def write_sn_by_usb(self,sn):
        if True == self.open_comport():
            self.device_into_specialmode(5)
            command = "AT+SETRUNPARA:MCUSN:" + sn
            self.ser.write(command)
            self.ui.util_info_show(command)
            self.save_log_to_file(command)
            time.sleep(5)
            n = self.ser.inWaiting()
            str = self.ser.read(n)
            self.ui.util_info_show(str)
            self.device_escape_specialmode()
            self.close_comport()
    def read_sn_by_usb(self):
        if True == self.open_comport():
            self.device_into_specialmode(5)
            command = "AT+GETRUNPARA:MCUSN:"
            self.ser.write(command)
            self.ui.util_info_show(command)
            self.save_log_to_file(command)
            time.sleep(2)
            n = self.ser.inWaiting()
            sn = self.ser.read(n)
            self.ui.util_info_show(sn)
            data = sn.split(":")
            self.device_escape_specialmode()
            self.close_comport()
            return data[1]
    def read_IMEI(self):
        command = "AT+READIMEI"
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(10)
        n = self.ser.inWaiting()
        readimei = self.ser.read(n)
        data = readimei.split(":")
        self.ui.util_info_show(readimei)
        if len(data) >= 2:
            return data[1]
        else:
            return False
    def write_IMEI(self,imei):
        command = "AT+WRITEIMEI:" + imei
        ret = self.sendcomand(command)
        if ret == False:
            return False
        self.ui.util_info_show(command)
        time.sleep(5)
        if True == self.waitingForReplyOK(2):
            self.ui.util_info_show("OK")
            return True
        else:
            return False
    def write_IMEI_by_usb(self,imei):
        if True == self.open_comport():
            self.device_into_specialmode(2)
            command = "AT+WRITEIMEI:" + imei
            self.ser.write(command)
            self.ui.util_info_show(command)
            self.save_log_to_file(command)
            time.sleep(5)
            n = self.ser.inWaiting()
            str = self.ser.read(n)
            self.ui.util_info_show(str)
            self.device_escape_specialmode()
            self.close_comport()
    def read_IMEI_by_usb(self):
        if True == self.open_comport():
            self.device_into_specialmode(2)
            command = "AT+READIMEI"
            self.ser.write(command)
            self.ui.util_info_show(command)
            self.save_log_to_file(command)
            time.sleep(10)
            n = self.ser.inWaiting()
            readimei = self.ser.read(n)
            data = readimei.split(":")
            self.ui.util_info_show(readimei)
            self.device_escape_specialmode()
            self.close_comport()
            return data[1]
        return 0
    def check_file_exist(self,name):
        path = os.getcwd()
        new = os.path.join(path,name)
        return os.path.exists(new) ## return True or False
    def check_boot_bin_size(self,filepath):
        fsize = os.path.getsize(filepath)
        fsize = fsize / float(1024)
        print "The size of "+ filepath,
        print fsize ,
        print "KB"
        if fsize > 50:
            return False
        else:
            return  True


