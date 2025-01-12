import re
from datetime import datetime

def yyyymmdd(us_date):
    dateO = datetime.strptime(us_date, "%m/%d/%Y")  # date-obj
    return dateO.strftime("%Y%m%d")

#! hard-coded JSON keys/values & positions:
#   _date, maturity
#   positions of schedule

class GuiToFile: 
    def __init__(self, file_name):
        self.of = open(file_name, 'w', encoding='utf-8')  #output-file
        
    def __del__(self):
        self.of.flush()
        self.of.close()
        
    def outComment(self,info): self.of.write(f"#!---{info}---:\n")

    def outSchdImpl(self, key, date, val):    
        schd = "|".join([yyyymmdd(date), val])
        self.of.write("\t".join([key,schd]) + "\n")

    def outSchedule(self, tab, k):     # k:(key), date; k+1: value
        self.outSchdImpl(tab.key(k), tab.valByIdx(k), tab.valByIdx(k+1))
    
    def writeLine(self, key, val):
        match = re.search(r'(_date|maturity)\b', key)  # \b: begin or end of word
        if match: val = yyyymmdd(val)
        self.of.write("\t".join([key,val]) + "\n")
        
    def writeLines(self,tab, i_start, minus_i):  # index: i_start to N - minus_i
        for k in range(i_start, tab.size()-minus_i):
            self.writeLine(tab.key(k),tab.valByIdx(k))     
        return k+1   # index of Next item

    def convert(self,tab):
        self.outComment("CONVERT")
        nextI = self.writeLines(tab, 0, 2)
        self.outSchedule(tab, nextI)
           
    def finiteDiff(self,tab):
        self.outComment("FINITE DIFFERENCE")
        self.writeLines(tab, 0,0)
    
    def pxIV(self,tab, mat_date):
        self.outComment("CONV-BOND PRICING INFO")
        GKEY_N = 7     
        SCHD_N = 2      # volatility-series & rate-series
         
        nextI = self.writeLines(tab, 0, GKEY_N + SCHD_N)       
        self.outSchdImpl(tab.key(nextI), tab.valByIdx(0), tab.valByIdx(nextI))
        nextI += 1
        self.outSchdImpl(tab.key(nextI), mat_date, tab.valByIdx(nextI))
        
    