import json

# JSON: dict of dict's
#   {Convert: { key: [caption, value, <tooltip, validate-code> ] } }

#! dictionary is ordered:
#!   items having a defined order, which will not change

#! hard-coded JSON keys:
#   Convert, Tooltips

class MyJson: 
    def __init__(self, json_fn):
        with open(json_fn, 'r') as jFile:
            # Load JSON data into Python dictionary
            cbDict = json.load(jFile)
            
        self.convert = cbDict['Convert']
        self.finiteDiff = cbDict['FiniteDiff']
        self.pxIV = cbDict['PxIV']
        self.cbTips = cbDict['Tooltips']