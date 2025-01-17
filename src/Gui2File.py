import re
from MyUtils import yyyymmdd

#! hard-coded JSON keys/values & positions:
#   _date, maturity
#   positions of schedule

class GuiToFile: 
    """Write inputs on GUI to parameters-file for C++"""
    
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

    def index_number(self, tab, part_key):  
        """index of first-match and number of matches of partial-key"""
        idx, num = -1, 0
        for k in range(0, tab.size()):
            if re.search(f'{part_key}', tab.key(k)):
                if idx == -1: idx = k
                num += 1
        return idx, num

    def convert(self,tab):
        self.outComment("CONVERT")
        idx, num = self.index_number(tab, "convert_schedule")
        self.writeLines(tab, 0, num)
        self.outSchedule(tab, idx)
           
    def finiteDiff(self,tab):
        self.outComment("FINITE DIFFERENCE")
        self.writeLines(tab, 0,0)
    
    def pxIV(self,tab, mat_date):
        self.outComment("CONV-BOND PRICING INFO")
        iGkey, nGkey = self.index_number(tab, "gkey_")
        iVol, nVol = self.index_number(tab, "volatility_series") 
        iRate, nRate = self.index_number(tab, "disc_rate_series") 
         
        self.writeLines(tab, 0, nGkey+nVol+nRate)     
        self.outSchdImpl(tab.key(iVol), tab.valByIdx(0), tab.valByIdx(iVol))
        self.outSchdImpl(tab.key(iRate), mat_date, tab.valByIdx(iRate))
        
    