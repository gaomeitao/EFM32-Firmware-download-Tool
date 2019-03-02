# -*- coding: UTF-8 -*-
# ======================
# imports
# ======================


from download_func import dl_service
from feedback import feedback
from filemerge import fm
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import END
from tkinter import Spinbox
from tkinter import messagebox as mBox
import threading as thread
import time
from language import language

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

        # ===================================================================


def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class download_gui:
    def __init__(self,language):
        # Create instance
        self.lgage = language
        self.win = tk.Tk()
        self.win.title(self.lgage.get_title_name())
        self.win.resizable(0, 0)
        self.createWidgets()
        self.info_length = 0
        self.onlyapp = "Only APP"
        self.bootapp = "Boot+APP"
        self.allinone = "AllInOne"
        self.dl_standby_mode = False
        self.log_switch = False
        self.cust = 2;
        self.WSN = 0
        self.WACT = 0
        self.WDT = 0
        self.WSVT = 0
        self.WSDT = 0
        self.WSRT = 0
        self.oncnt = 0
        self.soft_verison = 'SoftWare Version:A80_V1.2_20180619'
    # Modified Button Click Function
    def createDownloadThread(self):
        arrgv = ['usb', 'usb']
        runT = thread.Thread(target=startThreadForDownloadService,args=arrgv)
        runT.start()

    def createUtilThread(self,action):
        runT = thread.Thread(target=startThreadForUtilService, args=(action,))
        runT.start()
    def clickChooseapp(self):
        #delete all info in the scrolltext
        self.appfilename = filedialog.askopenfilename()
        self.scr.insert(tk.INSERT, self.appfilename + '\n')
        self.appname.set(self.appfilename)
    def clickChooseboot(self):
        #delete all info in the scrolltext
        self.bootfilename = filedialog.askopenfilename()
        self.scr.insert(tk.INSERT, self.bootfilename + '\n')
        self.bootname.set(self.bootfilename)
    def clickDownload(self):
        self.download_info_delete()

        if self.dl_chosen.get() == self.onlyapp:
            if self.appname.get() != "" :
                self.disable_download_button_text(True)
                self.action_download.configure(state='disabled')  # Disable the Button Widget
                self.scr.insert(tk.INSERT, 'Download......' + '\n')
                self.createDownloadThread()
            else:
                mBox.showinfo(self.lgage.get_download_box_title(), self.lgage.get_download_box_message())
            # download function called .
      #  startThreadToDownload()
        else:
            if self.dl_chosen.get() == self.bootapp:
                if self.appname.get() != "" and self.bootname.get() !="":
                    self.disable_download_button_text(True)
                    self.action_download.configure(state='disabled')  # Disable the Button Widget
                    self.scr.insert(tk.INSERT, 'Download......' + '\n')
                    self.createDownloadThread()
                else:
                    mBox.showinfo(self.lgage.get_download_box_title(), self.lgage.get_download_box_message())
            else:
                if self.dl_chosen.get() == self.allinone:
                    if self.bootname.get() != "":
                        self.disable_download_button_text(True)
                        self.action_download.configure(state='disabled')  # Disable the Button Widget
                        self.scr.insert(tk.INSERT, 'Download......' + '\n')
                        self.createDownloadThread()
                    else:
                        mBox.showinfo(self.lgage.get_download_box_title(), self.lgage.get_download_box_message())


    def clickreadSN(self):
        self.util_info_delete()
        self.writeSN.set(" ")
        self.wrAVT.set(" ")
        self.delayt.set(" ")
        self.sendt.set(" ")
        self.savet.set(" ")
        self.util_action = "readSN"
        self.createUtilThread(self.util_action)
        self.disable_utils_button_text(True)
    def clickwriteSN(self):
        self.util_info_delete()
        if self.WSN == 1 or self.WACT ==1 or self.WDT == 1 or self.WSVT ==1 or self.WSDT == 1:
            if self.WSN ==1:
                if self.writeSN.get() != "":
                    if len(self.writeSN.get()) != 8 :
                        mBox.showinfo(self.lgage.get_utils_box_title(),self.lgage.get_utils_box_sn_length())
                        return None
                else:
                    mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_sn_exam())
                    return None
            if self.WACT == 1:
                if self.wrAVT.get() != "":
                    if  len(self.wrAVT.get()) != 8:
                        mBox.showinfo(self.lgage.get_utils_box_title(),self.lgage.get_utils_box_act_length())
                        return None
                else:
                    mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_act_exam())
                    return None
            if self.WDT == 1:
                if self.delayt.get() != "" :
                     if int(self.delayt.get()) < 60:
                         mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_delayT_min_msg())
                         return None
                else:
                    mBox.showinfo(self.lgage.get_utils_box_title(),self.lgage.get_utils_box_delayT_msg())
                    return None
            if self.WSVT == 1:
                if self.savet.get() != "":
                    if int(self.savet.get()) < 60:
                        mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_save_min_msg())
                        return None
                else:
                    mBox.showinfo(self.lgage.get_utils_box_title(),self.lgage.get_utils_box_save_msg())
                    return None
            if self.WSDT == 1:
                if self.sendt.get() != "" :
                    if int(self.sendt.get()) < 180:
                        mBox.showinfo(self.lgage.get_utils_box_title(),self.lgage.get_utils_box_send_min_msg())
                        return None
                else:
                    mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_send_msg())
                    return None
            self.util_action = "writeSN"
            self.createUtilThread(self.util_action)
            self.disable_utils_button_text(True)
        else:
            if self.WSRT == 1:
                self.util_action = "writeSN"
                self.createUtilThread(self.util_action)
                self.disable_utils_button_text(True)
            else:
                mBox.showinfo(self.lgage.get_utils_box_title(),  self.lgage.get_utils_box_no_choose_msg())
    def clickreadIMEI(self):
        self.util_info_delete()
        self.readIMEI.set(" ")
        self.util_action = "readIMEI"
        self.createUtilThread(self.util_action)
        self.disable_utils_button_text(True)
    def clickwriteIMEI(self):
        self.util_info_delete()
        if self.writeIMEI.get() != "":
            if len(self.writeIMEI.get()) != 15:
                mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_imei_length_msg())
            else:
                self.util_action = "writeIMEI"
                self.createUtilThread(self.util_action)
                self.disable_utils_button_text(True)
        else:
            mBox.showinfo(self.lgage.get_utils_box_title(), self.lgage.get_utils_box_imei_exam_msg())

    def disable_download_button_text(self,switch):
        if True == switch:
            self.dl_chosen.config(state='disabled')
            self.comm_chosen.config(state='disabled')
            if self.dl_chosen.get() == self.onlyapp:
                self.action_appchoose.configure(state='disabled')
                self.appnameEntered.configure(state='readonly')
            else:
                if self.dl_chosen.get() == self.allinone:
                    self.action_bootchoose.configure(state='disabled')
                    self.bootnameEntered.configure(state='readonly')
                else:
                    self.action_bootchoose.configure(state='disabled')
                    self.action_appchoose.configure(state='disabled')
                    self.bootnameEntered.configure(state='readonly')
                    self.appnameEntered.configure(state='readonly')
        else:
            self.dl_chosen.config(state='readonly')
            self.comm_chosen.config(state='readonly')
            if self.dl_chosen.get() == self.onlyapp:
                self.action_appchoose.configure(state='enabled')
                self.appnameEntered.configure(state='normal')
            else:
                if self.dl_chosen.get() == self.allinone:
                    self.action_bootchoose.configure(state='enabled')
                    self.bootnameEntered.configure(state='normal')
                else:
                    self.action_bootchoose.configure(state='enabled')
                    self.action_appchoose.configure(state='enabled')
                    self.bootnameEntered.configure(state='normal')
                    self.appnameEntered.configure(state='normal')
    def disable_utils_button_text(self,switch):
        if True == switch:
            self.action_readSN.configure(state='disabled')
            self.action_writeSN.configure(state='disabled')
            self.action_readIMEI.configure(state='disabled')
            self.action_writeIMEI.configure(state='disabled')
            self.writeSNEntered.configure(state='readonly')
            self.wrAVTEntered.configure(state='readonly')
            self.writeIMEIEntered.configure(state='readonly')
            self.sendtEntered.configure(state='readonly')
            self.savetEntered.configure(state='readonly')
            self.delaytEntered.configure(state='readonly')
            self.readIMEIEntered.configure(state='readonly')
            self.cksn.configure(state='disabled')
            self.ckact.configure(state='disabled')
            self.ckdyt.configure(state='disabled')
            self.cksdt.configure(state='disabled')
            self.cksvt.configure(state='disabled')
        else:
            self.dl_chosen.config(state='readonly')
            self.comm_chosen.config(state='readonly')
            self.action_readSN.configure(state='enabled')
            self.action_writeSN.configure(state='enabled')
            self.action_readIMEI.configure(state='enabled')
            self.action_writeIMEI.configure(state='enabled')
            self.action_appchoose.configure(state='enabled')
            self.writeSNEntered.configure(state='normal')
            self.wrAVTEntered.configure(state='normal')
            self.writeIMEIEntered.configure(state='normal')
            self.readIMEIEntered.configure(state='normal')
            self.sendtEntered.configure(state='normal')
            self.savetEntered.configure(state='normal')
            self.delaytEntered.configure(state='normal')
            self.cksn.configure(state='normal')
            self.ckact.configure(state='normal')
            self.ckdyt.configure(state='normal')
            self.cksdt.configure(state='normal')
            self.cksvt.configure(state='normal')
    def download_info_show(self,info):
        self.scr.insert(tk.INSERT, info + '\n')
        #show latest row in the scrollbar
        self.scr.see(END)
    def util_info_show(self,info):
        self.scr1.insert(tk.INSERT, info + '\n')
        #show latest row in the scrollbar
        self.scr1.see(END)
    def info_get_text_len(self):
        self.info_length = len(self.scr.get('1.0', END + '-1c'))
    def info_delete_certain_length(self):
        self.scr.delete(str(float(self.info_length)), END)
    def download_info_delete(self):
        self.scr.delete(1.0,END)
    def util_info_delete(self):
        self.scr1.delete(1.0,END)
    def combobox_select_func(self,args):
        if self.dl_chosen.get() == self.onlyapp:
            self.action_appchoose.configure(state='enabled')
            self.appnameEntered.configure(state='normal')
            self.action_bootchoose.configure(state='disabled')
            self.bootnameEntered.configure(state='readonly')
        else:
            if self.dl_chosen.get() == self.bootapp:
                self.action_bootchoose.configure(state='enabled')
                self.bootnameEntered.configure(state='normal')
                self.action_appchoose.configure(state='enabled')
                self.appnameEntered.configure(state='normal')
            else:
                if  self.dl_chosen.get() ==self.allinone:
                    self.action_bootchoose.configure(state='enabled')
                    self.bootnameEntered.configure(state='normal')
                    self.action_appchoose.configure(state='disabled')
                    self.appnameEntered.configure(state='readonly')
    # Exit GUI cleanly
    def Entry_WriteIMEI(self,input_text):
        print input_text
        if input_text.isdigit() or (input_text == ""):
            if len(input_text) > 15: #imei len is 15
                return False
            else:
                return True
        else:
            return False
    def Entry_WriteSN(self,input_text):
        print input_text
        if self.cust == 1:
            if input_text.isdigit() or (input_text == ""):
                if len(input_text) > 12: #imei len is 15
                    return False
                else:
                    return True
            else:
                return False
        elif self.cust == 2 :
                if len(input_text) > 8: #imei len is 15
                    return False
                else:
                    return True
    def Entry_digit(self,input_text):
        print input_text
        if input_text.isdigit() or (input_text == ""):
          #  if len(input_text) > 12: #imei len is 15
          #      return False
          #  else:
                return True
        else:
                return False
    def systemreset_switch(self,onoff):
        if onoff == 1:
            self.oncnt = self.oncnt + 1
        else:
            if self.oncnt > 0:
                self.oncnt = self.oncnt - 1
       # print onoff
       # print self.oncnt
        if self.oncnt > 0:
            self.cksysrst.configure(state='disabled')
            self.ckbnsysrst.set(1)
            self.WSRT = 1
        else:
            self.cksysrst.configure(state='normal')
            self.ckbnsysrst.set(0)
            self.WSRT = 0
    ## delete radio box for duoxie tool .by major 20180302
    # def radCall(self):
    #     radSel = self.radVar.get()
    #     print radSel
    #     if radSel == 1:
    #         self.cust = 1 # tg
    #     elif radSel == 2:
    #         self.cust = 2  #duoxie
    def callCheckbuttonSN(self):
        if self.ckbnsn.get() == 1:
            self.WSN = 1
        else:
            self.WSN = 0

    def callCheckbuttonACT(self):
        if self.ckbnact.get() == 1:
            self.WACT = 1
        else:
            self.WACT = 0
    def callCheckbuttonDELAYT(self):
        if self.ckbndelay.get() == 1:
            self.WDT = 1
            self.systemreset_switch(1)
        else:
            self.WDT = 0
            self.systemreset_switch(0)
    def callCheckbuttonSAVET(self):
        if self.ckbnsave.get() == 1:
            self.WSVT = 1
            self.systemreset_switch(1)
        else:
            self.WSVT = 0
            self.systemreset_switch(0)
    def callCheckbuttonSENDT(self):
        if self.ckbnsend.get() == 1:
            self.WSDT = 1
            self.systemreset_switch(1)
        else:
            self.WSDT = 0
            self.systemreset_switch(0)

    def callCheckbuttonSRST(self):
        if self.ckbnsysrst.get() == 1:
            self.WSRT = 1
        else:
            self.WSRT = 0
    def show_port_and_baud(self,port,band):
        self.lsport.set(port)
        if band != "":
            self.lsbaud.set(band)
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()
    def donothing(self):
        ## need to go
        mBox.showinfo(self.lgage.get_about_box_title(),self.soft_verison)

    def clickfeedback(self):
        content = self.fdname.get()
        if content != "":
            if fd.feedback_mail(content):
                mBox.showinfo(self.lgage.get_feedback_box_title(),self.lgage.get_feedback_box_success_msg())
            else:
                mBox.showinfo(self.lgage.get_feedback_box_title(), self.lgage.get_feedback_box_fail_msg())
            self.fdtop.quit()
            self.fdtop.destroy()
        else:
            print "ddd"
    def send_problem(self):
        self.fdtop = tk.Toplevel()
        self.fdtop.title(self.lgage.get_feedback_frame_title())
        scnWidth, scnHeight = self.fdtop.maxsize()
        tmpcnf = '%dx%d+%d+%d' % (308, 81, (scnWidth - 308) / 2, (scnHeight - 81) / 2)
        self.fdtop.geometry(tmpcnf)
        self.fdname = tk.StringVar()
        self.fdnameEntered = ttk.Entry(self.fdtop, width=30, textvariable=self.fdname)
        self.fdnameEntered.grid(column=1, row=0, sticky='W', rowspan=1, ipadx=18,ipady = 30)
        self.action_feedback = ttk.Button(self.fdtop, text=self.lgage.get_bn_send_title(), width=10, command=self.clickfeedback)
        self.action_feedback.grid(column=2, row=0)
        self.fdtop.mainloop()
      #  fd.feedback_mail("test")
    def dl_in_stanby_mode(self):
        if self.dl_standby_mode == False:
            self.dl_standby_mode = True
        else:
            self.dl_standby_mode = False
    def dl_save_tool_log(self):
        if self.log_switch == False:
            self.log_switch = True
        else:
            self.log_switch = False
    def fm_file_merge(self):
        fm(self)
    def createWidgets(self):

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="green")
        self.tabControl = ttk.Notebook(self.win)  # Create Tab Control

        self.tab1 = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.tab1, text=self.lgage.get_tabcontrol_tool_title())  # Add the tab

        self.tab2 = ttk.Frame(self.tabControl)  # Add a second tab
        self.tabControl.add(self.tab2, text=self.lgage.get_tabcontrol_util_title())#,state = "hidden")  # Make second tab visible
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

        self.monty = ttk.LabelFrame(self.tab1,text=self.lgage.get_lbfrm_upgrade_title())
        self.monty.grid(column=0, row=0, padx=60, pady=20)
        self.filelabel = ttk.Label(self.monty, text=self.lgage.get_lb_appfile_title()).grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        self.appname = tk.StringVar()
        self.appnameEntered = ttk.Entry(self.monty, width=30, textvariable=self.appname)
        self.appnameEntered.grid(column=1, row=0, sticky='W', columnspan=3)#rowspan=1, ipadx=18)

        self.filelabel2 = ttk.Label(self.monty, text=self.lgage.get_lb_bootfile_title()).grid(column=0, row=1, sticky='W')
        # Adding a Textbox Entry widget
        self.bootname = tk.StringVar()
        self.bootnameEntered = ttk.Entry(self.monty, width=30, textvariable=self.bootname)
        self.bootnameEntered.grid(column=1, row=1, sticky='W', columnspan=3)#rowspan=1, ipadx=18)
        self.bootnameEntered.configure(state='readonly')
        
        # Adding a Choose Button
        self.action_appchoose = ttk.Button(self.monty, text=self.lgage.get_bn_choose_title(), width=10, command=self.clickChooseapp)
        self.action_appchoose.grid(column=4, row=0)

        self.action_bootchoose = ttk.Button(self.monty, text=self.lgage.get_bn_choose_title(), width=10, command=self.clickChooseboot)
        self.action_bootchoose.grid(column=4, row=1)
        self.action_bootchoose.configure(state='disabled')
        # Adding a Download Button
        self.action_download = ttk.Button(self.monty, text=self.lgage.get_bn_dl_title(), width=10, command=self.clickDownload)
        self.action_download.grid(column=4, row=2)

  

        self.commlabel = ttk.Label(self.monty, text=self.lgage.get_lb_comm_title()).grid(column=0, row=2, sticky='W')

        self.comm_option = tk.StringVar()
        self.comm_chosen = ttk.Combobox(self.monty, width=4, textvariable=self.comm_option)
        self.comm_chosen['values'] = ('USB', 'UART',)
        self.comm_chosen.grid(column=1, row=2)
        self.comm_chosen.current(0)  # set init value turple is index
        self.comm_chosen.config(state='readonly')  # set as readonly

        self.typelabel = ttk.Label(self.monty, text=self.lgage.get_lb_type_title()).grid(column=2, row=2, sticky='W')
        # Adding a Combobox
        self.dl_option = tk.StringVar()
        self.dl_chosen = ttk.Combobox(self.monty, width=10, textvariable=self.dl_option)
        self.dl_chosen['values'] = ("Only APP","Boot+APP","AllInOne")
        self.dl_chosen.grid(column=3, row=2)
        self.dl_chosen.current(0)  # set init value turple is index
        self.dl_chosen.config(state='readonly')  # set as readonly

        self.lsport = tk.StringVar()
        self.lport = ttk.Label(self.monty, text="",textvariable =self.lsport ).grid(column=0, row=3, sticky='W')
        self.lsbaud = tk.StringVar()
        self.lbaud = ttk.Label(self.monty, text="",textvariable =self.lsbaud).grid(column=3, row=3, sticky='W')

      # Using a scrolled Text control
        self.scrolW = 30
        self.scrolH = 8
        self.scr = scrolledtext.ScrolledText(self.monty, width=self.scrolW, height=self.scrolH, wrap=tk.WORD)
        self.scr.grid(column=0, row=4, sticky='WE', columnspan=6)

       # self.dlpg = ttk.Progressbar(self.monty,length=350, mode="indeterminate", orient="horizontal")
       # self.dlpg.grid(row=4, column=0,columnspan=9)
       # self.dlpg["maximum"] = 100
       # self.dlpg["value"] = 0
        #add by major for test
       # for i in range(100):
        #    self.dlpg.step(i)


        self.dl_chosen.bind("<<ComboboxSelected>>", self.combobox_select_func)
        # Add Tooltip
        # createToolTip(self.action, 'This is Button.')
        # createToolTip(self.nameEntered, 'the file path where is download bin.')
        # createToolTip(self.scr, 'infor display.')
        for child in self.monty.winfo_children():
            child.grid_configure(padx=6, pady=2)

        self.monty1 = ttk.LabelFrame(self.tab2,text="MCU")
        self.monty1.grid(column=2, row=0, padx=60, pady=10)

       # self.labelsFrame = ttk.LabelFrame(self.tab2, text='Modem')
       # self.labelsFrame.grid(column=0, row=0,)# padx=60, pady=20)#columnspan=4)

        #self.labelsFrame1 = ttk.LabelFrame(self.tab2, text='Modem')
        #self.labelsFrame1.grid(column=1, row=0, padx=30, pady=10)  # columnspan=4)

        #self.label_SN = ttk.Label(self.monty1, text="SN:").grid(column=0, row=1, sticky='W')
        #self.label_ACTCODE = ttk.Label(self.monty1, text="AVTCODE:").grid(column=2, row=1, sticky='W')
        #self.label_delay = ttk.Label(self.monty1, text="DelayT:").grid(column=0, row=2, sticky='W')
        #self.label_send = ttk.Label(self.monty1, text="SaveT:").grid(column=2, row=2, sticky='W')
        #self.label_save = ttk.Label(self.monty1, text="SendT:").grid(column=0, row=3, sticky='W')

        #style = ttk.Style()
        #style.configure("BW.TButton", font=("Times", "10", 'bold'))
        #style = "BW.TButton"
        self.action_readSN = ttk.Button(self.monty1, text=self.lgage.get_bn_get_title(),command=self.clickreadSN)
        self.action_readSN.grid(column=4, row=1, rowspan=2,ipadx= 8,ipady=10,sticky='W')

        self.action_writeSN = ttk.Button(self.monty1, text=self.lgage.get_bn_set_title(),command=self.clickwriteSN)
        self.action_writeSN.grid(column=4, row=3,rowspan=2,ipadx= 8,ipady=10, sticky='W')

        self.writeSN = tk.StringVar()
        self.writeSNCMD = self.win.register(self.Entry_WriteSN)  ## neccesary
        self.writeSNEntered = ttk.Entry(self.monty1, textvariable=self.writeSN,width=30,validate='key',
                                        validatecommand = (self.writeSNCMD, '%P'))
        self.writeSNEntered.grid(column=1, row=0, sticky='W')


        self.wrAVT = tk.StringVar()
        self.wrAVTCMD = self.win.register(self.Entry_WriteSN)  ## neccesary
        self.wrAVTEntered = ttk.Entry(self.monty1, textvariable=self.wrAVT,width=30, validate='key',
                                        validatecommand=(self.wrAVTCMD, '%P'))
        self.wrAVTEntered.grid(column=1, row=1, sticky='W')


        self.delayt = tk.StringVar()
        self.delaytCMD = self.win.register(self.Entry_digit)  ## neccesary
        self.delaytEntered = ttk.Entry(self.monty1,width=30, textvariable=self.delayt, validate='key',
                                        validatecommand=(self.delaytCMD, '%P'))
        self.delaytEntered.grid(column=1, row=2, sticky='W',)

        self.savet = tk.StringVar()
        self.savetCMD = self.win.register(self.Entry_digit)  ## neccesary
        self.savetEntered = ttk.Entry(self.monty1,width=30, textvariable=self.savet,validate='key',
                                        validatecommand=(self.savetCMD, '%P'))
        self.savetEntered.grid(column=1, row=3, sticky='W')

        self.sendt = tk.StringVar()
        self.sendtCMD = self.win.register(self.Entry_digit)  ## neccesary
        self.sendtEntered = ttk.Entry(self.monty1,width=30, textvariable=self.sendt,validate='key',
                                        validatecommand=(self.sendtCMD, '%P'))
        self.sendtEntered.grid(column=1, row=4, sticky='W')

        # Creating three checkbuttons
        self.ckbnsn = tk.IntVar()
        self.cksn = tk.Checkbutton(self.monty1, text=self.lgage.get_lb_sn_title(), variable=self.ckbnsn,command = self.callCheckbuttonSN)#, state='disabled')
        self.cksn.deselect()
        self.cksn.grid(column=0, row=0, sticky=tk.W)
       # self.cksn.configure(state='disabled')
        self.ckbnact = tk.IntVar()
        self.ckact = tk.Checkbutton(self.monty1, text=self.lgage.get_lb_act_title(), variable=self.ckbnact,command = self.callCheckbuttonACT)
        self.ckact.deselect()  # Clears (turns off) the checkbutton.
        self.ckact.grid(column=0, row=1, sticky=tk.W)
        #self.ckbnact.set(0)
        self.ckbndelay = tk.IntVar()
        self.ckdyt = tk.Checkbutton(self.monty1, text=self.lgage.get_lb_dlt_title(), variable=self.ckbndelay,command = self.callCheckbuttonDELAYT)
        self.ckdyt.deselect()
        self.ckdyt.grid(column=0, row=2, sticky=tk.W)

        self.ckbnsave = tk.IntVar()
        self.cksvt = tk.Checkbutton(self.monty1, text=self.lgage.get_lb_svt_title(), variable=self.ckbnsave,command = self.callCheckbuttonSAVET)
        self.cksvt.deselect()
        self.cksvt.grid(column=0, row=3, sticky=tk.W)

        self.ckbnsend = tk.IntVar()
        self.cksdt = tk.Checkbutton(self.monty1, text=self.lgage.get_lb_sdt_title(), variable=self.ckbnsend,command = self.callCheckbuttonSENDT)
        self.cksdt.deselect()
        self.cksdt.grid(column=0, row=4, sticky=tk.W)

        self.ckbnsysrst= tk.IntVar()
        self.cksysrst = tk.Checkbutton(self.monty1, text=self.lgage.get_lb_srst_title(), variable=self.ckbnsysrst,command = self.callCheckbuttonSRST)
        self.cksysrst.deselect()
        self.cksysrst.grid(column=4, row=0, sticky=tk.W)

        self.label_RDIMEI = ttk.Label(self.monty1, text=self.lgage.get_lb_rdimei_title()).grid(column=0, row=7, sticky='W')
        self.label_WRIMEI = ttk.Label(self.monty1, text=self.lgage.get_lb_wrimei_title()).grid(column=0, row=6, sticky='W')
        self.action_readIMEI = ttk.Button(self.monty1, text=self.lgage.get_bn_rdimei_title(),command=self.clickreadIMEI)
        self.action_readIMEI.grid(column=4, row=7,ipadx= 8, sticky='W')
        self.action_writeIMEI = ttk.Button(self.monty1, text=self.lgage.get_bn_wrimei_title(),command=self.clickwriteIMEI)
        self.action_writeIMEI.grid(column=4, row=6,ipadx= 8, sticky='W')
        self.readIMEI = tk.StringVar()
        self.readIMEIEntered = ttk.Entry(self.monty1,width=30, textvariable=self.readIMEI)
        self.readIMEIEntered.grid(column=1, row=7, sticky='W', )
        self.writeIMEI = tk.StringVar()
        self.writeIMEICMD = self.win.register(self.Entry_WriteIMEI) ## neccesary
        self.writeIMEIEntered = ttk.Entry(self.monty1,width=30, textvariable=self.writeIMEI,validate='key',
                                          validatecommand=(self.writeIMEICMD,'%P'))
        self.writeIMEIEntered.grid(column=1, row=6, sticky='W',)

        self.scr1 = scrolledtext.ScrolledText(self.monty1, width=30, height=5, wrap=tk.WORD)
        self.scr1.grid(column=0, row=5, sticky='WE', columnspan=6)

        style1 = ttk.Style()
        style1.configure("XX.TLabel", foreground="red")

        self.label_SN = ttk.Label(self.monty1, text=self.lgage.get_lb_tip_title(),style ="XX.TLabel" ).grid(column=0, row=8, sticky='W')
        ## delete radio box for duoxie tool .by major 20180302
        # self.radVar = tk.IntVar()
        # self.rad_tg = tk.Radiobutton(self.monty1, text="TG+", variable=self.radVar, value=1,  command=self.radCall)
        # self.rad_tg.grid(column=0, row=5, sticky=tk.W)
        #
        # self.rad_dx = tk.Radiobutton(self.monty1, text="DUOXIE", variable=self.radVar, value=2, command=self.radCall)
        # self.rad_dx.grid(column=1, row=5, sticky=tk.W)
        # self.radVar.set(2)  # set default value
        ## modify end
       # self.action.grid(column=2, row=1, rowspan=2, padx=6)
    # Creating a Menu Bar
        self.menuBar = Menu(self.win)
        self.win.config(menu=self.menuBar)

#    Add menu items
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label=self.lgage.get_mn_quit_title(), command=self._quit)

        self.optmenu = Menu(self.menuBar, tearoff=0)
        self.optmenu.add_checkbutton(label=self.lgage.get_mn_dl_in_standy_title(),command=self.dl_in_stanby_mode)
        self.optmenu.add_separator()
        self.optmenu.add_checkbutton(label=self.lgage.get_mn_save_log_title(), command=self.dl_save_tool_log)
        self.optmenu.add_separator()
        self.optmenu.add_command(label=self.lgage.get_mn_file_merge_title(), command=self.fm_file_merge)

        self.helpmenu = Menu(self.menuBar, tearoff=0)
        self.helpmenu.add_command(label=self.lgage.get_mnlb_help_title(), command=self.donothing)
        self.helpmenu.add_command(label=self.lgage.get_mnlb_fdbk_title(), command=self.send_problem)
        self.helpmenu.add_command(label=self.lgage.get_mnlb_abt_title(), command=self.donothing)


        self.menuBar.add_cascade(label=self.lgage.get_mnlb_file_title(), menu=self.filemenu)
        self.menuBar.add_cascade(label=self.lgage.get_mnlb_option_title(), menu=self.optmenu)
        self.menuBar.add_cascade(label=self.lgage.get_mnlb_help_title(), menu=self.helpmenu)

        # Change the main windows icon
        # Place cursor into name Entry
        path = os.getcwd()
        self.appnameEntered.focus()

def waiting_for_usb_comport_enmu(dl,type,timeout=20):
    while timeout > 0:
        timeout = timeout - 1
        usb_port = dl.find_usb_port()
        if usb_port != "false":
            print usb_port
            port_num = int(usb_port[3:]) - 1
            dl.set_comm_port(port_num)
            ui.show_port_and_baud("Port:"+usb_port,"")
            return True
        else:
            display = "Waiting for USB Comm ................" + str(timeout)
            if type == "dl":
                ui.download_info_delete()
                ui.download_info_show(display)
            else:
                ui.util_info_delete()
                ui.util_info_show(display)
            time.sleep(1)
    if timeout == 0:
        return False

def waiting_for_uart_comport_enmu(dl,timeout=20):
    while timeout > 0:
        timeout = timeout - 1
        uart_port = dl.find_uart_port()
        if uart_port != "false":
            print uart_port
            port_num = int(uart_port[3:]) - 1
            dl.set_comm_port(port_num)
            ui.show_port_and_baud("Port:"+uart_port, "Baud:115200")
            return True
        else:
            ui.download_info_delete()
            display = "Waiting for Uart Comm ................" + str(timeout)
            ui.download_info_show(display)
            time.sleep(1)
    if timeout == 0:
        return False
def download_agent(dl,filename):
    start = time.clock()
    ret = dl.download_bin_send(filename)
    stop = time.clock()
    ui.download_info_show("Time Expense: " + str(round((stop - start),2)) +' S')
    return ret
def download_bootloader_by_usb(dl):
    if True == waiting_for_usb_comport_enmu(dl,'dl'):
        if True == dl.open_comport():
            ui.download_info_show("USB CommPortOpenSuccess")
            if True == dl.bootloader_downloadcommand_send(6):
                ui.download_info_show("USB bootloader download command Send success")
                if True == download_agent(dl,ui.bootfilename):
                    dl.reboot_device()
                    ui.download_info_show("USB bootloader download  SUCCESS")
                    dl.close_comport()
                    time.sleep(10)
                    return True
                else:
                    dl.close_comport()
                    ui.download_info_show("USB bootloader download  Failed")
                    return False
            else:
                ui.download_info_show("USB bootloader download command Send Failed")
                dl.close_comport()
                return False
        else:
            ui.download_info_show("USB CommPortOpenFailed")
            return False
    else:
        ui.download_info_show("Can't find any availiable comm port!")
        return False
def download_allinone_by_usb(dl):
    if True == waiting_for_usb_comport_enmu(dl,'dl'):
        if True == dl.open_comport():
            ui.download_info_show("USB CommPortOpenSuccess")
            if True == dl.bootloader_downloadcommand_send(6):
                ui.download_info_show("USB  AllInOne command Send success")
                if True == download_agent(dl,ui.bootfilename):
                    dl.boot_to_application()
                    ui.download_info_show("USB AllInOne download  SUCCESS")
                    dl.close_comport()
                    return True
                else:
                    dl.close_comport()
                    ui.download_info_show("USB AllInOne download  Failed")
                    return False
            else:
                ui.download_info_show("USB AllInOne download command Send Failed")
                dl.close_comport()
                return False
        else:
            ui.download_info_show("USB CommPortOpenFailed")
            return False
    else:
        ui.download_info_show("Can't find any availiable comm port!")
        return False
def download_file_by_usb(dl):
    if True == waiting_for_usb_comport_enmu(dl,'dl'):
        if True == dl.open_comport():
            ui.download_info_show("USB CommPortOpenSuccess")
            time.sleep(2)
            if True == dl.app_download_command_send(6):
                ui.download_info_show("USB App download command Send success")
                if True == download_agent(dl,ui.appfilename):
                #dl.boot_to_application() #new bootloader no need to send bootup comand
                    ui.download_info_show("USB App download SUCCESS")
                else:
                    ui.download_info_show("USB App download Failed")
                dl.close_comport()
            else:
                ui.download_info_show("USB App download command Send Failed")
                dl.close_comport()
        else:
            ui.download_info_show("USB CommPortOpenFailed")
    else:
        ui.download_info_show("Can't find any availiable comm port!")
def download_bootloader_by_uart(dl):
    if True == waiting_for_uart_comport_enmu(dl):
        if True == dl.open_comport():
            ui.download_info_show("UART CommPortOpenSuccess")
            if True == dl.handshake_with_target(20):
                if True == dl.bootloader_downloadcommand_send(6):
                    ui.download_info_show("UART bootloader download command Send success")
                    download_agent(dl,ui.bootfilename)
                    dl.reboot_device()
                    ui.download_info_show("UART bootloader download SUCCESS")
                    dl.close_comport()
                    return True
                else:
                    ui.download_info_show("UART bootloader download command Send Failed")
                    dl.close_comport()
                    return False
            else:
                ui.download_info_show("UART HandShake with target Failed !1")
                dl.close_comport()
                return False
        else:
            ui.download_info_show("CommPortOpenFailed")
            return False
    else:
        ui.download_info_show("Can't find any availiable comm port!")
        return False
def download_allinone_by_uart(dl):
    if True == waiting_for_uart_comport_enmu(dl):
        if True == dl.open_comport():
            ui.download_info_show("UART CommPortOpenSuccess")
            if True == dl.handshake_with_target(20):
                if True == dl.bootloader_downloadcommand_send(6):
                    ui.download_info_show("UART AllInOne download command Send success")
                    download_agent(dl,ui.bootfilename)
                    dl.boot_to_application()
                    ui.download_info_show("UART AllInOne download SUCCESS")
                    dl.close_comport()
                    return True
                else:
                    ui.download_info_show("UART AllInOne download command Send Failed")
                    dl.close_comport()
                    return False
            else:
                ui.download_info_show("UART HandShake with target Failed !1")
                dl.close_comport()
                return False
        else:
            ui.download_info_show("CommPortOpenFailed")
            return False
    else:
        ui.download_info_show("Can't find any availiable comm port!")
        return False
def download_file_by_uart(dl):
    if True == waiting_for_uart_comport_enmu(dl):
        if True == dl.open_comport():
            ui.download_info_show("UART CommPortOpenSuccess")
            if True == dl.handshake_with_target(20):
                if True == dl.app_download_command_send(6):
                    ui.download_info_show("UART App download command Send success")
                    if True == download_agent(dl,ui.appfilename):
                        #dl.boot_to_application() # new bootloader no need to send boot up comand
                        ui.download_info_show("UART App download SUCCESS")
                        dl.close_comport()
                        return True
                    else:
                        ui.download_info_show("UART App download Failed")
                        dl.close_comport()
                        return False
                else:
                    ui.download_info_show("UART App download command Send Failed")
                    dl.close_comport()
                    return False
            else:
                ui.download_info_show("UART HandShake with target Failed !1")
                dl.close_comport()
                return False
        else:
            ui.download_info_show("CommPortOpenFailed")
            return False
    else:
        ui.download_info_show("Can't find any availiable comm port!")
        return False

def reboot_device_to_bootloader(dl):
    if True == waiting_for_usb_comport_enmu(dl,'dl'):
        ui.download_info_show("Reboot device into BootLoader!")
        if True == dl.reboot_device_in_standymodem():
            time.sleep(6)
            ui.download_info_show("device reboot success!")
            return True
        else:
            ui.download_info_show("device reboot failed!,Pls retry agained!")
            return False
    else:
        ui.download_info_show("Can't find any availiable comm port!")
        return False

def startThreadForDownloadService(comm_type,file_type):
    dl = dl_service(ui, ui.log_switch)
    if True == ui.dl_standby_mode and ui.comm_chosen.get() == "USB":
        if False == reboot_device_to_bootloader(dl):
            ui.action_download.configure(state='enabled')
            ui.disable_download_button_text(False)
            return None
    if ui.comm_chosen.get() == "USB":
        if ui.dl_chosen.get() == ui.bootapp:
            if True == dl.check_file_exist(ui.bootfilename) and True == dl.check_boot_bin_size(
                    ui.bootfilename) and True == dl.check_file_exist(ui.appfilename):
                if True == download_bootloader_by_usb(dl):
                    download_file_by_usb(dl)
                else:
                    ui.action_download.configure(state='enabled')
                    ui.disable_download_button_text(False)
                    return None
            else:
                ui.download_info_show("Bootloader File is wrong!")
                ui.action_download.configure(state='enabled')
                ui.disable_download_button_text(False)
                return None
        else:
            if ui.dl_chosen.get() == ui.allinone:
                if True == dl.check_file_exist(ui.bootfilename):
                    download_allinone_by_usb(dl)
                else:
                    ui.download_info_show("Download File is not exist!")
                    ui.action_download.configure(state='enabled')
                    ui.disable_download_button_text(False)
                    return None
            else:
                if True == dl.check_file_exist(ui.appfilename):
                    download_file_by_usb(dl)
                else:
                    ui.download_info_show("Download File is not exist!")
                    ui.action_download.configure(state='enabled')
                    ui.disable_download_button_text(False)
                    return None
    else:
        if ui.comm_chosen.get() == "UART":
            if ui.dl_chosen.get() == ui.bootapp:
                if True == dl.check_file_exist(ui.bootfilename) and True == dl.check_boot_bin_size(
                        ui.bootfilename)and True == dl.check_file_exist(ui.appfilename):
                    if True == download_bootloader_by_uart(dl):
                        download_file_by_uart(dl)
                    else:
                        print "bootloader download fail"
                    ui.action_download.configure(state='enabled')
                    ui.disable_download_button_text(False)
                    return None
                else:
                    ui.download_info_show("Bootloader File is wrong!")
                    ui.action_download.configure(state='enabled')
                    ui.disable_download_button_text(False)
                    return None
            else:
                if ui.dl_chosen.get() == ui.allinone:
                    if True == dl.check_file_exist(ui.bootfilename):
                        download_allinone_by_uart(dl)
                    else:
                        ui.download_info_show("Download File is not exist!")
                        ui.action_download.configure(state='enabled')
                        ui.disable_download_button_text(False)
                        return None
                else:
                    if True == dl.check_file_exist(ui.appfilename):
                        download_file_by_uart(dl)
                    else:
                        ui.download_info_show("Download File is not exist!")
                        ui.action_download.configure(state='enabled')
                        ui.disable_download_button_text(False)
                        return None
        else:
            ui.download_info_show(ui.comm_chosen.get())
    ui.action_download.configure(state='enabled')
    ui.disable_download_button_text(False)
def device_bootup_with_usb(dl):
    if True == waiting_for_usb_comport_enmu(dl, 'ul'):
        if True == dl.open_comport():
            dl.boot_to_application()
            dl.close_comport()

def startThreadForUtilService(action):
     dl = dl_service(ui,ui.log_switch)
     if True == waiting_for_usb_comport_enmu(dl,'ul'):
            if action == "readSN":
                if True == dl.open_comport():
                    ret = dl.device_into_specialmode(5)
                    if ret == False:
                        ui.disable_utils_button_text(False)
                        dl.close_comport()
                        return False
                    sn = dl.read_sn()
                    if sn != False:
                        ui.util_info_show(sn)
                        ui.writeSN.set(sn)
                    avtcode = dl.read_avtcode()
                    if avtcode != False:
                        ui.wrAVT.set(avtcode)
                        ui.util_info_show(avtcode)
                    delaytime = dl.read_delaytime()
                    if delaytime != False:
                        ui.delayt.set(delaytime)
                    savetime = dl.read_savetime()
                    if savetime != False:
                        ui.savet.set(savetime)
                    sendtime = dl.read_sendtime()
                    if sendtime != False:
                        ui.sendt.set(sendtime)
                    dl.device_escape_specialmode()
                    dl.close_comport()
                    device_bootup_with_usb(dl)
                else:
                    print " read error"

            if action == "writeSN":
                if True == dl.open_comport():
                    ret = dl.device_into_specialmode(5)
                    if ret == False:
                        ui.disable_utils_button_text(False)
                        dl.close_comport()
                        return False
                    if ui.WSN == 1:
                        sn = ui.writeSN.get()
                        dl.write_sn(sn)
                    if ui.WACT == 1:
                        avtcode = ui.wrAVT.get()
                        dl.write_actcode(avtcode)
                    if ui.WDT == 1:
                        delaytime = ui.delayt.get()
                        dl.write_delaytime(delaytime)
                    if ui.WSVT == 1:
                        savetime = ui.savet.get()
                        dl.write_savetime(savetime)
                    if ui.WSDT == 1:
                        sendtime = ui.sendt.get()
                        dl.write_sendtime(sendtime)
                    if ui.WSRT == 1:
                        dl.systemreset()
                    dl.device_escape_specialmode()
                    dl.close_comport()
                    device_bootup_with_usb(dl)
                else:
                    print "write error"
            if action == "readIMEI":
                if True == dl.open_comport():
                    ret = dl.device_into_specialmode(2)
                    if ret == False:
                        ui.disable_utils_button_text(False)
                        dl.close_comport()
                        return False
                    imei = dl.read_IMEI()
                    ui.readIMEI.set(imei)
                    ui.util_info_show(imei)
                    dl.device_escape_specialmode()
                    dl.close_comport()
                    device_bootup_with_usb(dl)
                else:
                    print "read IMEI error"
            if action == "writeIMEI":
                if True == dl.open_comport():
                    ret = dl.device_into_specialmode(2)
                    if ret == False:
                        ui.disable_utils_button_text(False)
                        dl.close_comport()
                        return False
                    imei = ui.writeIMEI.get()
                    dl.write_IMEI(imei)
                    dl.device_escape_specialmode()
                    dl.close_comport()
                    device_bootup_with_usb(dl)
                else:
                    print "write IMEI error"
     else:
         ui.util_info_show("Can't find any availiable USB comm port!")
     ui.disable_utils_button_text(False)

# ======================
# Start GUI
# ======================
lg = language()
ui= download_gui(lg)
fd = feedback()
width = 488
height = 341
scnWidth, scnHeight = ui.win.maxsize()
tmpcnf = '%dx%d+%d+%d' % (width, height, (scnWidth - width) / 2, (scnHeight - height) / 2)
ui.win.geometry(tmpcnf)
ui.win.mainloop()