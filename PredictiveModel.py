# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 17:07:47 2020

@author: heyif
"""
import pandas as pd
from xgboost import XGBClassifier
from MedicalInfo import HeartConditions
# In[]
class Prediction(object):
    def __init__(self, predictors, target):
        self.predictors = predictors
        self.target = target
        self.model = None
        self.features = pd.DataFrame({column_name:[] for column_name in self.predictors.columns.values})
        self.feature_value = {column_name:0 for column_name in self.predictors.columns.values}
    
    def train_model(self):
        self.model = XGBClassifier(learning_rate = 0.1 , n_estimators = 150, gamma = 0.3, objective = "binary:logistic", min_child_weight = 1, max_depth = 4, scale_pos_weight = 17)
        self.model.fit(self.predictors, self.target)
    
    def update_q1(self, q1_result):
        self.feature_value.update({"1":q1_result})
    
    def update_q2(self, q2_result):
        if q2_result < 18:
            self.feature_value.update({"RefUnder18":1})
        elif q2_result <= 49 and q2_result >= 40:
            self.feature_value.update({"Age_40_49":1})
        elif q2_result <= 59 and q2_result >= 50:
            self.feature_value.update({"Age_50_59":1})
        elif q2_result <= 69 and q2_result >= 60:
            self.feature_value.update({"Age_60_69":1})
        elif q2_result <= 74 and q2_result >= 70:
            self.feature_value.update({"Age_70_74":1})
        elif q2_result >= 75:
            self.feature_value.update({"Age_75_99":1})
    
    def update_q3(self, q3_result, q3_detail):
        if q3_result == "Yes":
            if "Other" in q3_detail:
                q3_detail.remove("Other")
                
            total = HeartConditions().get_all_with_categories()
            selected = set([total[i] for i in q3_detail])
            self.feature_value.update({i:1 for i in selected})
            
    def update_q4(self, q4_result):
        if q4_result == "Yes":
            self.feature_value.update({"ENDOC_MET_Metabolic_A":1})
    
    def update_q5(self, q5_result):
        if q5_result == "Yes":
            self.feature_value.update({"ENDOC_MET_Diabetes":1})
    
    def update_q6(self, q6_result):
        if q6_result == "Yes":
            self.feature_value.update({"GENRL_UNSP_Other_Nos_A":1})
    
    def update_q7(self, q7_result):
        if q7_result == "Yes":
            self.feature_value.update({"CHEST_Airway_Lungs_A":1})

    def update_q8(self, q8_result):
        if q8_result == "Yes":
            self.feature_value.update({"CHEST_Airway_Lungs_A":1})
    
    def update_q9(self, q9_result):
        if q9_result == "Yes":
            self.feature_value.update({"UROLG_GEN_Other_Nos_B":1})
    
    def predict_result(self):
        self.features = self.features.append(self.feature_value, ignore_index = True)
        self.train_model()
        return self.model.predict_proba(self.features)[0][1]
        
    
            
            
    
        
