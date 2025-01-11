import tkinter as tk
from tkinter import *

# pip install tkinter-tooltip
from tktooltip import ToolTip
from tkinter import messagebox as mb
import re
from datetime import datetime

# stored in the class: list of widgets with
#   { key: [caption, value, <tooltip, validate-code>] }
                
class LableEntryGrid(Frame):   
    def __init__(self, master, cb_part, cb_tips):
        Frame.__init__(self, master)       
        self.columnconfigure(0, weight=2) # configure grid
        self.columnconfigure(1, weight=1)
        
        self.gInputL = []    #  list: key-value(user-input)
        self.create2Columns(cb_part, cb_tips)
        self.rowNum = len(self.gInputL)

    def size(self): return self.rowNum
    def key(self, row_i): return self.gInputL[row_i].key   
    def valByIdx(self, row_i): return self.gInputL[row_i].get()    
    
    def valByKey(self, gkey):      # return gui-input for gui-key 
        for j in range(self.rowNum):
            if self.key(j) == gkey: return self.valByIdx(j)
        return ""
                
    def setVal(self, gkey, gval):
        for j in range(self.rowNum):
            if self.key(j) == gkey:
                self.gInputL[j].delete(0, tk.END) 
                self.gInputL[j].insert(0, gval)
                return
            
    def create2Columns(self, cb_part, cb_tips):       
        gRow = -1   # grid-row
        for keyL, valL in cb_part.items():
            if valL[0]:                         # caption is NOT "" (EMPTY)
                gRow +=1
                if isinstance(valL[1], list):   # value is input-list
                    ctrl = self.addOptMenuRow(gRow, valL, cb_tips)
                else:                           # caption-input pair                    
                    ctrl = self.addEntryRow(gRow, valL, cb_tips)
            else: 
                ctrl = self.addHiddenKV(valL[1]) 

            ctrl.key = keyL   # Add a new attribute to tk-widget
            self.gInputL += [ctrl]                
            
    def addLabel(self, row_i, caption):
        gLabel = Label(self, text=caption)
        gLabel.grid(column=0, row=row_i, sticky=W, padx=2, pady=2)

    # ToolTip and validatecommand
    def addEntryRow(self, row_i, val_list, cb_tips):
        self.addLabel( row_i, val_list[0])      # caption
        
        uEntry = Entry(self, justify="right")   # user-Entry
        uEntry.insert(0, val_list[1])           # value
        if len(val_list) >= 3: ToolTip(uEntry, msg=cb_tips[val_list[2]])
        if len(val_list) == 4:
            vCmd = self.addValidator(val_list[3])
            uEntry.config(validate='focusout', validatecommand=vCmd)

        uEntry.grid(column=1, row=row_i, sticky=E, padx=2, pady=2)
        return uEntry          # Entry for retrieve value later
        
    def addOptMenuRow(self, row_i, val_list, cb_tips):  
        self.addLabel( row_i, val_list[0])
        
        optVals = val_list[1]       # optVals: LIST
        valShow = StringVar(self)          
        valShow.set(optVals[0])     # Set default value
        oMenu = OptionMenu(self, valShow, *optVals) 
        oMenu.config(bg="lightblue", relief="groove")
        if len(val_list) >= 3: ToolTip(oMenu, msg=cb_tips[val_list[2]])
        
        oMenu.grid(column=1, row=row_i, sticky=E, padx=2, pady=2)
        return valShow          # StringVar for retrive value later
    
    def addHiddenKV(self, value):       # EMPTY ("") caption
        valNoShow = StringVar(self) 
        valNoShow.set(value) 
        return valNoShow 
        
    def validateNotNegative(self,g_input, widget_name):    
        if re.match(r"^[0-9]*\.?[0-9]+$", g_input): return True
        mb.showerror("BAD Input", f"{g_input}: NOT zero or positive")
        self.nametowidget(widget_name).focus_set()
        return False
        
    def validatePositive(self,g_input, widget_name):    
        if re.match(r"^[0-9]*\.?[0-9]+$", g_input) and float(g_input)>0.0: return True
        mb.showerror("BAD Input", f"{g_input}: NOT positive")
        self.nametowidget(widget_name).focus_set()
        return False
    
    def validateUSDate(self, g_input, widget_name):    
        try:
            datetime.strptime(g_input, "%m/%d/%Y")
            return True
        except ValueError:
            mb.showerror("BAD Input", f"{g_input}: NOT a US-date (month/day/year)")
            self.nametowidget(widget_name).focus_set()
            return False    
        
    def validateInBtw(self, g_input, widget_name, valid_code):    
        x,lowB,highB = valid_code.split("_")   # lowB: low-bound
        if re.match(r"^[0-9]*\.?[0-9]+$", g_input):
            if float(lowB) <= float(g_input) and float(g_input) <= float(highB): return True
        mb.showerror("BAD Input", f"{g_input}: NOT between {lowB} and {highB}")
        self.nametowidget(widget_name).focus_set()
        return False
    
    def addValidator(self, valid_code):
        if valid_code == "date_us":
            vCmd = (self.register(self.validateUSDate), '%P', '%W')
        elif valid_code == "non_minus":
            vCmd = (self.register(self.validateNotNegative), '%P', '%W')
        elif valid_code == "plus":
            vCmd = (self.register(self.validatePositive), '%P', '%W')
        else:
            vCmd = (self.register(self.validateInBtw), '%P', '%W', valid_code)
        return vCmd
        
        
class CvtLEGrid(LableEntryGrid):   
    def __init__(self, master, cb_part, cb_tips):
        LableEntryGrid.__init__(self, master, cb_part, cb_tips)
        
    def matDate(self): return self.valByKey("maturity")
        
class PxIVLEGrid(LableEntryGrid):   
    def __init__(self, master, cb_part, cb_tips):
        LableEntryGrid.__init__(self, master, cb_part, cb_tips)
       
    def cppExe(self): return self.valByKey("gkey_cpp")
    def wDir(self): return self.valByKey("gkey_dir")
    def runId(self): 
        px_iv = self.valByKey("gkey_PxIv")
        return "Iv" if px_iv.find("implied")>-1 else "Px"
        
    def setPx(self, px):
        self.setVal('gkey_cbPx', px[0])
        self.setVal('gkey_delta', px[1])
        self.setVal('gkey_gamma', px[2])
    
    def setIV(self, iv): self.setVal('gkey_iv', iv[0])    
    def setWDir(self, w_dir): self.setVal('gkey_dir', w_dir)
    
    def setFocus(self): self.gInputL[0].focus_set()