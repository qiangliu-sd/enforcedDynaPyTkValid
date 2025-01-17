
from datetime import datetime
import tkinter as tk
from tkinter import messagebox as msgb

def yyyymmdd(us_date: str):
    """Input: US-date
       Output: yyyymmdd
    """
    dateO = datetime.strptime(us_date, "%m/%d/%Y")  # date-obj
    return dateO.strftime("%Y%m%d")
    
    
def fleetingPopup(out_millisec=20):
    """Show for 20 milliseconds and disappear"""
    myWin = tk.Tk()
    myWin.withdraw()
    try:
        myWin.after(out_millisec, myWin.destroy)
        msgb.showinfo('DONT-click-me', 'I take focus!', master=myWin)
    except: pass
    