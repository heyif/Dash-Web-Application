# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 09:53:47 2020

@author: heyif
"""

import pytest
from PredictiveModel import Prediction
#from MedicalInfo import HeartConditions 
# In[]
@pytest.mark.parametrize("q1, q2, q3, q3_detail, q4, q5, q6, q7, q8, q9", 
                         [(1, 87, 1, ["Congenital heart disorder", "Aortic aneurysm and dissection", "Other"], 0, 1, 0, 1, 0, 1),
                          (0, 44, 0, [], 1, 0, 1, 1, 1, 1, 0), 
                          (1, 59, 1, ["Atrial fibrillation", "Cardiomyopathy", "Myocarditis"], 1, 0, 0, 0, 1, 0)
                          ])

def test_update_answer(q1, q2, q3 , q3_detail, q4, q5, q6, q7, q8, q9):
    predict = Prediction()
    predict.update_q1(q1)
    predict.update_q2(q2)
    predict.update_q3(q3, q3_detail)
    predict.update_q4(q4)
    predict.update_q5(q5)
    predict.update_q6(q6)
    predict.update_q7(q7)
    predict.update_q8(q8)
    predict.update_q9(q9)
    predictors = predict.feature_value 
    
    assert predictors["1"] == q1
    if q2 < 18:
        assert predictors["RefUnder18"] == 1
    elif q2 <= 49 and q2 >= 40:
        assert predictors["Age_40_49"] == 1
    elif q2 <= 59 and q2 >= 50:
        assert predictors["Age_50_59"] == 1
    elif q2 <= 69 and q2 >= 60:
        assert predictors["Age_60_69"] == 1
    elif q2 <= 74 and q2 >= 70:
        assert predictors["Age_70_74"] == 1
    elif q2 >= 75:
        assert predictors["Age_75_99"] == 1
    
    for i in q3_detail:
        if i != "Other":
            assert predictors[i] == 1
    
    assert predictors["ENDOC_MET_Metabolic_A"] == (q4 == "Yes")
    assert predictors["ENDOC_MET_Diabetes"] == (q5 == "Yes")
    assert predictors["GENRL_UNSP_Other_Nos_A"] == (q6 == "Yes")
    assert predictors["CHEST_Airway_Lungs_A"] == (q7 == "Yes" or q8 == "Yes")
    assert predictors["UROLG_GEN_Other_Nos_B"] == (q9 == "Yes")
# In[]
@pytest.mark.parametrize("q1, q2, q3, q3_detail, q4, q5, q6, q7, q8, q9", 
                         [(0, 18, 1, ["Congenital heart disorder", "Aortic aneurysm and dissection", "Other"], 0, 1, 0, 1, 0, 1),
                          (1, 68, 0, [], 1, 0, 1, 1, 1, 1, 0), 
                          (0, 34, 1, ["Rheumatic heart disease", "Cardiomyopathy", "Polyarteritis"], 1, 0, 0, 0, 1, 0)
                          ])

def test_predict(q1, q2, q3 , q3_detail, q4, q5, q6, q7, q8, q9):
    predict = Prediction()
    predict.update_q1(q1)
    predict.update_q2(q2)
    predict.update_q3(q3, q3_detail)
    predict.update_q4(q4)
    predict.update_q5(q5)
    predict.update_q6(q6)
    predict.update_q7(q7)
    predict.update_q8(q8)
    predict.update_q9(q9)
    
    predict.predict_result()
    
    assert True 