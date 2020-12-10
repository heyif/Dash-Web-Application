# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 09:27:31 2020

@author: heyif
"""

class HeartConditions(object):
    # get all conditions along with its category 
    def get_all_with_categories(self):
        total = {}
        total.update(self.CardiacB()[1])
        total.update(self.CardiacA()[1])
        total.update(self.CardiacArterial()[1])
        total.update(self.CardiacHeartRhythm()[1])
        total.update(self.CardiacOther()[1])
        return total
    
    # get all categories 
    def get_categories(self):
        return [self.CardiacB()[0], self.CardiacA()[0], self.CardiacArterial()[0], self.CardiacHeartRhythm()[0], self.CardiacOther()[0]]
    
    # get all conditions 
    def get_all(self):
        total = self.get_all_with_categories()
        total = list(total.keys())
        return total
    
    # the first category of heart conditions
    def CardiacB(self):
        conditions = ["Congenital heart disorder", "Angina", "Heart failure", "Myocarditis", "Heart valve disorder"]
        conditions_with_category = {condition:"CVASC_Cardiac_B" for condition in conditions}
        return "CVASC_Cardiac_B", conditions_with_category 
    
    # the second category of heart conditions
    def CardiacA(self):
        conditions = ["Rheumatic heart disease", "Coronary artery disease", "Cardiomyopathy"]
        conditions_with_category = {condition:"CVASC_Cardiac_A" for condition in conditions}
        return "CVASC_Cardiac_A", conditions_with_category 
    
    # the third category of heart conditions
    def CardiacArterial(self):
        conditions = ["Polyarteritis", "Aortic aneurysm and dissection"]
        conditions_with_category = {condition :"CVASC_Arterial_A" for condition in conditions}
        return "CVASC_Arterial_A", conditions_with_category 
    
    # the fourth category of heart conditions
    def CardiacHeartRhythm(self):
        conditions = ["Arrhythmias", "Atrial fibrillation"]
        conditions_with_category = {condition:"CVASC_Heart_Rhythm_A" for condition in conditions}
        return "CVASC_Heart_Rhythm_A", conditions_with_category 
    
    # the fifth category of heart conditions
    def CardiacOther(self):
        conditions = ["Pulmonary hypertension"]
        conditions_with_category = {condition:"CVASC_Other_Nos_A" for condition in conditions}
        return "CVASC_Other_Nos_A", conditions_with_category 
        