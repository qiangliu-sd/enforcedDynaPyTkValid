import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import sys
sys.path.append(r'.\src')  # add search path
import os
 
from LableEntryGrid import *
from MyJson import *
from Gui2File import *
from CppInPy import *
from MyUtils import fleetingPopup

#! hard-coded dir/file names:
#   qllog, __py.cb_params.txt
#   MySample.json

# GUI (interface) class 
class TkinterGUI(tk.Tk):
    """Coding-STYLE
       ------------
        MyClass, _classVar, self.dataMemb, self.membFunc
        arg_in, localVar
        MYCONSTANT 
    """
    
    DCpp = "qlcpp"      # dir-cpp  
    DLOG = "qllog"      # used by C++ (do NOT modify)
    DINPUT = "qlinput"
        
    def __init__(self, json_fn):   
        tk.Tk.__init__(self)
        self.prmFn = os.path.join(self.DINPUT, "__py.cb_params.txt")
        self.pxivFn = os.path.join(self.DLOG,"__py.cb_px_iv.txt")
        self.check3SubDirs()
        # setup GUI
        self.add3Tabs(json_fn)    
        self.add2Buttons1Label()        
    
    def add3Tabs(self, json_fn):
        noteBk = ttk.Notebook()  # hold tabs; NOT used directly later
        cb = MyJson(json_fn)

        self.tabCvt = CvtLEGrid(noteBk, cb.convert, cb.cbTips)
        self.tabFD = LableEntryGrid(noteBk, cb.finiteDiff, cb.cbTips)
        self.tabPxIV = PxIVLEGrid(noteBk, cb.pxIV, cb.cbTips)
        noteBk.add(self.tabCvt, text="Convert")
        noteBk.add(self.tabFD, text="Finite Difference")
        noteBk.add(self.tabPxIV, text="Pricing/Implied-vol")
        self.tabPxIV.setWDir(os.getcwd())
        noteBk.pack()
        #noteBk.select(self.tabPxIV)    # set-focus
        #self.tabPxIV.setFocus()
    
    def add2Buttons1Label(self):
        bPx = Button(self, text="Compute", command=lambda: self.bPxClicked())
        bSave = Button(self, text="Save Parameters", command=lambda: self.bSaveClicked())
        bPx.pack(side=tk.RIGHT)
        bSave.pack(side=tk.RIGHT)
        initNote = f"C++ exe in [{self.DCpp}]\nCB parameters in [{self.DINPUT}]\nLOG-files in [{self.DLOG}]"
        self.lMsg = Label(self, text=initNote, fg="red", bd=2, relief=GROOVE)
        self.lMsg.pack(side=tk.BOTTOM)   
    
    def bSaveClicked(self):
        """Button clicked with invalid user-input:
            focus-out is NOT trigger.
            
            Force [focusout] by [fleetingPopup] with at least 20 millisec
        """       
        fleetingPopup(20)
        if not LableEntryGrid._inputValid:
            self.lMsg.config(text="BAD inputs!!!")
            return
       
        self.lMsg.config(text="Saving Parameters ...")
        t2f = GuiToFile(self.prmFn)
        matDate = self.tabCvt.matDate()
        
        t2f.pxIV(self.tabPxIV, matDate)
        t2f.convert(self.tabCvt)
        t2f.finiteDiff(self.tabFD)
        del t2f
        self.lMsg.config(text="Parameters SAVED")

    def bPxClicked(self):
        self.bSaveClicked()   # save params first

        cppFn = os.path.join(self.DCpp,self.tabPxIV.cppExe())
        px = CppInPy(self.lMsg, self.DCpp)
        px.run(cppFn, self.tabPxIV.runId(),self.prmFn,self.pxivFn )
        if px.success(): self.showPx_IV()
                   
    def check3SubDirs(self):
        if not (os.path.isdir(self.DCpp)):  os.mkdir(self.DCpp)
        if not (os.path.isdir(self.DLOG)):  os.mkdir(self.DLOG)
        if not (os.path.isdir(self.DINPUT)):os.mkdir(self.DINPUT)
            
        
    def showPx_IV(self):
        try:
            with open(self.pxivFn, "r") as fp:
                firstLine = fp.readline()
            px_iv = firstLine.split("\t")  
            if len( px_iv) == 3: self.tabPxIV.setPx(px_iv)
            else: self.tabPxIV.setIV(px_iv[0])
        except IOError as e:
            self.lMsg.config(text=f"Pricing results file XCP: {e}")
            
 
def tkGuiMain():
    """Runs in dir of this file (current-work-dir)"""
    myGui = TkinterGUI(r'.\src\MySample.json')
    myGui.geometry("600x500")
    myGui.title("QLiu:: Enforced Dynamic-Range Tk-Validating with JSON")
    myGui.mainloop()
    
if __name__ == "__main__":
    tkGuiMain()