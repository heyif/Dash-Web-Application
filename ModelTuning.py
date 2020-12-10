# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:20:35 2020

@author: heyif
"""
# libraries to process data 
import pandas as pd

# libraries for modeling 
from sklearn.model_selection import GridSearchCV, ShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from xgboost.sklearn import XGBClassifier
# In[]
# define a function to tune the hyper parameters of the model 
def tuning(model_name ,model, variables, target, param, param_value, default_param, standardize = None):    

    model_ = model(**default_param)
    
    if standardize != None:
        # remember to only transform numerical variables but not categorical ones
        
        num_indices = standardize
        num_transformer = Pipeline(steps = [('scaler', StandardScaler())])
        
        cat_indices = [i for i in variables.columns.tolist() if i not in num_indices]
        cat_transformer = Pipeline(steps = [("scaler", FunctionTransformer(lambda data: data))])
        
        preprocessor = ColumnTransformer(transformers = [('num', num_transformer, num_indices), ('cat', cat_transformer, cat_indices)])
        
        fullmodel = Pipeline(steps = [('processor', preprocessor), (model_name.lower(), model_)])
        
                
    else:
        fullmodel = make_pipeline(model_)
    
    model_name = model_name.lower() + "__"
    param_grid = {model_name + i : j for i, j in zip(param, param_value)}
    
    shuffle_split = ShuffleSplit(test_size=0.25, n_splits=100)
    grid_search=GridSearchCV(fullmodel, param_grid,cv=shuffle_split,scoring = 'roc_auc', return_train_score=True)
    grid_search.fit(variables, target)
    results = pd.DataFrame(grid_search.cv_results_).sort_values("rank_test_score", ascending = True)[['rank_test_score','mean_test_score'] + ["param_"+ model_name + i for i in param]]
    best_param = {i : results["param_"+ model_name + i].tolist()[0] for i in param}
    return results ,best_param
# In[]
# import the data
data = pd.read_csv("Data/Whole Data.csv")
target = data.iloc[:, 0]
predictors = data.iloc[:, range(2, len(data.columns))]
train_X, test_X, train_Y, test_Y = train_test_split(predictors, target, stratify = target, random_state = 123, test_size = 0.25)
test_X, val_X, test_Y, val_Y = train_test_split(test_X, test_Y, stratify = test_Y, random_state = 123, test_size = 0.01)

# In[]
# tuning n estimators
default = dict(learning_rate = 0.1, objective = "binary:logistic", min_child_weight = 1, max_depth = 4, scale_pos_weight = 17)
n_estimators = [125, 150, 175, 200]
result, best_params = tuning("xgbclassifier", XGBClassifier, val_X, val_Y, ["n_estimators"], [n_estimators], default, standardize = None)
print(result)
default.update(best_params)
# the best n estimators is 200
# In[]
# tuning max_depth
max_depth = [4,6,8,10]
result, best_params = tuning("xgbclassifier", XGBClassifier, val_X, val_Y, ["max_depth"], [max_depth], default, standardize = None)
print(result)
default.update(best_params)
# the best max depth is 4
# In[]
# tuning gamma
gamma = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
result, best_params = tuning("xgbclassifier", XGBClassifier, val_X, val_Y, ["gamma"], [gamma], default, standardize = None)
print(result)
default.update(best_params)
# the best gamma is 0.3
# In[]
# the final model is 
finalModel = XGBClassifier(default)
finalModel = XGBClassifier(learning_rate = 0.1 , n_estimators = 150, gamma = 0.3, objective = "binary:logistic", min_child_weight = 1, max_depth = 4, scale_pos_weight = 17)
finalModel.fit(predictors, target)
finalModel.fit(val_X, val_Y)
# In[]
# save the model and sample dataset 
import pickle 

with open('finalModel.pkl', 'wb') as f:
    pickle.dump(finalModel, f)

val_X.to_csv("Data/predictors.csv", index = False)
val_Y.to_csv("Data/target.csv", index = False)
