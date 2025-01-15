
import subprocess as sp
import os

class CppInPy:
    def __init__(self, msg_b, d_log):
        self.msg = msg_b
        self.dLog = d_log
        self.rCode = -1
    
    def success(self):
        return self.rCode == 0
    
    # paths from os.path.join() (exe, prm_fn, px_fn) have to pass in separately
    def run(self, exe, code, prm_fn, px_fn):   
        self.msg.config(text="Computing ...")
        eMsg =lambda obj: obj.stderr if obj.stderr else obj.stdout                  
               
        try:
            spRun = sp.run([exe, code, prm_fn, px_fn], check=True,
                shell=True, capture_output= True,text=True, cwd=os.getcwd())
            self.rCode = spRun.returncode
            if self.success():
                self.msg.config(text="Computing DONE")             
            else:
                self.msg.config(text=f"C++ run ERR: see >err_*.log< in [{self.dLog}]\n{eMsg(spRun)}")
        except sp.CalledProcessError as xcp:
            self.msg.config(text=f"C++ run XCP:\n{eMsg(xcp)}")            
