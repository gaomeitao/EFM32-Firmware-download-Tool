import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import END
from tkinter import Spinbox
from tkinter import messagebox as mBox


class fm:
    def __init__(self,fatherui):
        self.verion = "1.1"
        self.fui = fatherui
        self.offset = 0
        self.mergedfile = 0
        self.savepath = ""
        self.create_ui()
    def clickfm(self):
        if self.fm1name.get() !="" and self.fm2name.get() !="":
            print "merge"
            self.savepath = filedialog.asksaveasfilename()
            if self.fm3name.get() !="":
                self.offset = int(self.fm3name.get(), 16)
            print self.offset
            if self.savepath != "":
                if True == self.mergefile(self.file1name,self.file2name,self.offset,self.savepath):
                    mBox.showinfo(self.fui.lgage.get_filemerge_box_title(), self.fui.lgage.get_filemerge_box_merge_msg())
                else:
                    mBox.showinfo(self.fui.lgage.get_filemerge_box_title(), self.fui.lgage.get_filemerge_box_offset_msg())
            else:
                mBox.showinfo(self.fui.lgage.get_filemerge_box_title(), self.fui.lgage.get_filemerge_svfile_msg())
        else:
            mBox.showinfo(self.fui.lgage.get_filemerge_box_title(), self.fui.lgage.get_filemerge_file_msg())

        self.fm1nameEntered.focus()
    def clickChoosefl1(self):
        self.file1name = filedialog.askopenfilename()
        self.fm1name.set(self.file1name)
        self.fm1nameEntered.focus()
    def clickChoosefl2(self):
        self.file2name = filedialog.askopenfilename()
        self.fm2name.set(self.file2name)
        self.fm2nameEntered.focus()
    def create_ui(self):
        self.fmtop = tk.Toplevel()
        self.fmtop.title(self.fui.lgage.get_filemerge_frame_title())
        scnWidth, scnHeight = self.fmtop.maxsize()
        tmpcnf = '%dx%d+%d+%d' % (333, 81, (scnWidth - 333) / 2, (scnHeight - 81) / 2)
        self.fmtop.geometry(tmpcnf)
        self.filelabel = ttk.Label(self.fmtop, text=self.fui.lgage.get_lb_file1_title()).grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        self.fm1name = tk.StringVar()
        self.fm1nameEntered = ttk.Entry(self.fmtop, width=30, textvariable=self.fm1name)
        self.fm1nameEntered.grid(column=1, row=0, sticky='W', columnspan=3)  # rowspan=1, ipadx=18)

        self.filelabel2 = ttk.Label(self.fmtop, text=self.fui.lgage.get_lb_file2_title()).grid(column=0, row=1,sticky='W')
        # Adding a Textbox Entry widget
        self.fm2name = tk.StringVar()
        self.fm2nameEntered = ttk.Entry(self.fmtop, width=30, textvariable=self.fm2name)
        self.fm2nameEntered.grid(column=1, row=1, sticky='W', columnspan=3)  # rowspan=1, ipadx=18)

        self.filelabel3 = ttk.Label(self.fmtop, text=self.fui.lgage.get_lb_offset_title()).grid(column=0, row=2, sticky='W')
        # Adding a Textbox Entry widget
        self.fm3name = tk.StringVar()
        self.fm3nameEntered = ttk.Entry(self.fmtop, width=30, textvariable=self.fm3name)
        self.fm3nameEntered.grid(column=1, row=2, sticky='W', columnspan=3)  # rowspan=1, ipadx=18)

        self.action_appchoose = ttk.Button(self.fmtop, text=self.fui.lgage.get_bn_choose_title(), width=10, command=self.clickChoosefl1)
        self.action_appchoose.grid(column=4, row=0)

        self.action_bootchoose = ttk.Button(self.fmtop, text=self.fui.lgage.get_bn_choose_title(), width=10, command=self.clickChoosefl2)
        self.action_bootchoose.grid(column=4, row=1)

        self.action_feedback = ttk.Button(self.fmtop, text=self.fui.lgage.get_bn_merge_title(), width=10,
                                          command=self.clickfm)
        self.action_feedback.grid(column=4, row=2)
        self.fmtop.mainloop()

    def mergefiletosrc(self,srcpath, dstfp):
        srcfb = open(srcpath, 'rb')
        while 1:
            filebytes = srcfb.readline()
            if not filebytes: break
            dstfp.write(filebytes)
        srcfb.close()

    def mergefile(self,file1,file2,offset,mfsave):
        print file1
        print file2
        print offset
        print mfsave

        self.mergedfile = open(mfsave, 'wb')

        self.mergefiletosrc(file1, self.mergedfile)
        currentPos = self.mergedfile.tell()
        print self.mergedfile.tell()
        if offset - currentPos < 0:
            print "failed"
            self.mergedfile.close()
            os.remove(mfsave)
            return False
        else:
            self.mergedfile.seek(offset - currentPos, 1)
        self.mergefiletosrc(file2, self.mergedfile)
        self.mergedfile.close()
        return True