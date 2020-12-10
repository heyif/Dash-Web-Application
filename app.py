# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:49:21 2020

@author: heyif
"""
#import sklearn
#from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from MedicalInfo import HeartConditions
from PredictiveModel import Prediction

# In[]
#with open('finalModel.pkl', "rb") as f:
#    Model = pickle.load(f)
predictors = pd.read_csv("Data/predictors.csv")
target = pd.read_csv("Data/target.csv")
# In[]
app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True)

# sidebar style 
SIDEBAR_STYLE = {
        "position": "relative",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f2f0eb",
        }

# content style
#CONTENT_STYLE = {
#        "position": "relative",
#        "top": 0,
#        "margin-left": "18rem",
#        "margin-right": "2rem",
#       # "padding": "2rem 1rem",
#        }
CONTENT_STYLE = {
        "width": "70rem",
        "height": "180rem",
        "padding": "2rem 1rem",
        "background-color": "#f2f0eb"
        }

# prognostic tool style
PROGNOSTIC_STYLE = {
        #"padding": "2rem 1rem",
        "background-color": "#f8f9fa"
        }


# In[]
nav_bar = dbc.Navbar(
        dbc.NavbarBrand([html.H1("COVID-19 RISK CALCULATOR", style = {"color":"white" , "fontSize":30})]),
        color = "primary", 
        dark = True
        )
# In[]
# Nav
nav = dbc.Nav([
        dbc.NavItem(dbc.NavLink("COVID PROGNOSTIC TOOL", href = "covid-prognostic-tool", id = "covid-prognostic-tool-link")),
        dbc.NavItem(dbc.NavLink("COVID QUIZ", href = "covid-quiz", id = "covid-quiz-link"))
        ], vertical = True, pills = True)


# Side Bar 
sidebar = html.Div([
        html.H5("NAVIGATION"),
        html.Hr(),
        nav
        ],
style = SIDEBAR_STYLE
)

# --- activation of navigation link--- #
@app.callback([Output(link_name, "active") for link_name in ("covid-prognostic-tool-link", "covid-quiz-link")], [Input("url", "pathname")])
def toggle_active_link(path_name):
    if path_name == "/":
        return True, False
    return [path_name == link_name for link_name in ("/covid-prognostic-tool", "/covid-quiz")]

# In[]
# covid-19 prognostic tool heading
prognostic_heading = html.Div([
        html.H3("COVID-19 PROGNOSTIC TOOL"), 
        html.H5("Estimate mortality rates in patients with COVID-19.", style = {"color":"#828187"}),
        html.Hr()
        ])

# progress bar
progress_bar = dbc.Alert([
        html.P(children = "0/9 QUESTIONS COMPLETE", style = {"color":"#00754a" , "fontSize":18}, id = "answer-progress"),
        dbc.Progress(value = 0, striped = True, animated = True, id = "answer-progress-bar")
        ], color = "light")

# Part 1: basic information
# question 1: gender
q1 = dbc.FormGroup([
        dbc.Label("1. WHAT SEX WERE YOU ASSIGNED AT BIRTH: ", html_for = "gender-option", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "gender-option",            
                       options = [{"label":"Male", "value":1}, {"label":"Female", "value":0}],
                       style = {"color":"#1f5869", "fontSize":17.5}
                       )       
            ])

# question 2: age 
q2 = dbc.FormGroup([
        dbc.Label("2. YOUR AGE: ", id = "age-question", html_for = "age-slider", style = {"color":"#1f5869", "fontSize":18}),
        dcc.Slider(id = "age-slider", 
                   min = 0, 
                   max = 100, 
                   step = 1, 
                   value = 0,
                   marks = {
                           15: {"label":'15', "style":{"color":"#63a8a6"}},
                           30: {"label":'30', "style":{"color":"#63a8a6"}},
                           45: {"label":'45', "style":{"color":"#63a8a6"}},                
                           60: {"label":'60', "style":{"color":"#63a8a6"}},
                           75: {"label":'75', "style":{"color":"#63a8a6"}},
                           90: {"label":'90', "style":{"color":"#63a8a6"}}
                           }, included = False
                   )
        ])
        
# aggregate part1 questions
basic_info = dbc.Alert([
        html.H5("ABOUT YOU", style = {"color":"#1f5869"}),
        html.Hr(),
        q1,
        q2
        ], color = "light")

# Part 2: pre-existing conditions
# question 3: heart disease 
q3 = dbc.FormGroup([
                dbc.Label("3. DO YOU HAVE UNDERLYING HEART CONDITIONS", html_for = "heart-question", style = {"color":"#1f5869", "fontSize":18}),
                dbc.RadioItems(id = "heart-question", 
                               options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                               style = {"color":"#1f5869", "fontSize":17.5}, 
                               inline = True 
                               )                                                                                                    
        ]) 

# question 3 follow-up question
q3_details = html.Div([
        dbc.Collapse([
                dbc.FormGroup([
                        #dbc.Label("CHOOSE ANY OF THE FOLLOWING HEART CONDITIONS"), 
                        dcc.Dropdown(
                                id = "heart-detail-question", 
                                options = [{"label":i, "value":i} for i in HeartConditions().get_all() + ["Other"]],
                                multi = True,
                                placeholder = "CHOOSE ANY OF THE FOLLOWING HEART CONDITIONS", 
                                value = []
                                )                       
                        ])               
                ], id = "heart-detail-collapse")       
        ])

#q3_details = html.Div([
#        dbc.Collapse([
#                dbc.FormGroup([
#                        dbc.Label("3.1 CHOOSE ANY OF THE FOLLOWING HEART CONDITIONS", style = {"color":"#1f5869", "fontSize":18}), 
#                        dbc.Checklist(
#                                options = [{"label":i, "value":i} for i in HeartConditions().get_all() + ["Other"]],
#                                #multi = True,
#                                id = "heart-detail-question",
#                                value = [],
#                                style = {"color":"#77919d", "fontSize":16}
#                                )                       
#                        ])               
#                ], id = "heart-detail-collapse")       
#        ])

#  question 4: overweight or obesity 
q4 = dbc.FormGroup([
        dbc.Label("4. ARE YOU OVERWEIGHT OR OBESE (BMI HIGHER THAN 30 KG/M2)", html_for = "obesity-question", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "obesity-question", 
                       options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                       style = {"color":"#1f5869", "fontSize":17.5}, 
                       inline = True 
                       )                                                                                                    
        ])

# question 5: diabetes
q5 = dbc.FormGroup([
        dbc.Label("5. DO YOU HAVE DIABETES", html_for = "diabetes-question", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "diabetes-question", 
                       options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                       style = {"color":"#1f5869", "fontSize":17.5}, 
                       inline = True 
                       )                                                                                                    
        ])

# question 6: Cystic fibrosis
q6 = dbc.FormGroup([
        dbc.Label("6. DO YOU HAVE CYSTIC FIBROSIS", html_for = "cystic-question", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "cystic-question", 
                       options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                       style = {"color":"#1f5869", "fontSize":17.5}, 
                       inline = True 
                       )                                                                                                    
        ])

# question 7: Pulmonary fibrosis
q7 = dbc.FormGroup([
        dbc.Label("7. DO YOU HAVE PULMONARY FIBROSIS", html_for = "lung-question", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "lung-question", 
                       options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                       style = {"color":"#1f5869", "fontSize":17.5}, 
                       inline = True 
                       )                                                                                                    
        ])

# question 8: Immunocompromised condition
q8 = dbc.FormGroup([
        dbc.Label("8. DO YOU HAVE IMMUNOCOMPROMISED CONDITION", html_for = "immune-question", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "immune-question", 
                       options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                       style = {"color":"#1f5869", "fontSize":17.5}, 
                       inline = True 
                       )                                                                                                    
        ])

# question 9: Chronic kidney disease
q9 = dbc.FormGroup([
        dbc.Label("9. DO YOU HAVE CHRONIC KIDNEY DISEASE", html_for = "kidney-question", style = {"color":"#1f5869", "fontSize":18}),
        dbc.RadioItems(id = "kidney-question", 
                       options = [{"label":"Yes", "value":"Yes"}, {"label":"No", "value":"No"}],
                       style = {"color":"#1f5869", "fontSize":17.5}, 
                       inline = True 
                       )                                                                                                    
        ])


# aggregate part2 questions 
medical_info = dbc.Alert([
        html.H5("PRE-EXISTING MEDICAL CONDITIONS", style = {"color":"#1f5869"}),
        html.Hr(),
        q3, 
        q3_details,
        q4,
        q5,
        q6,
        q7,
        q8,
        q9
        ], color = "light")

    

# --- the callback of age --- #
@app.callback(Output("age-question" , "children"), [Input("age-slider", "value")])
def update_age_question(age):
    if age == 0:
        return "2. YOUR AGE: "
    return f"2. YOUR AGE: {age}"

# --- the callback of heart condition details --- #
@app.callback([Output("heart-detail-collapse", "is_open"), Output("heart-detail-question", "value")], 
              [Input("heart-question", "value"), 
               State("heart-detail-collapse", "is_open")])
def show_detail_heart_conditions(has_condition, is_open):
    if has_condition == "Yes":
        return True, []
    return False, []

# --- update the progress bar --- #
@app.callback([Output("answer-progress-bar", "value"), Output("answer-progress", "children")], 
              [Input("gender-option", "value"), 
               Input("age-slider", "value"),
               Input("heart-question", "value"),
               Input("heart-detail-question", "value"), 
               Input("obesity-question", "value"),
               Input("diabetes-question", "value"), 
               Input("cystic-question", "value"), 
               Input("lung-question", "value"),
               Input("immune-question", "value"), 
               Input("kidney-question", "value"),
               #State("answer-progress-bar", "value"),
               State("gender-option", "value"), 
               State("age-slider", "value"),
               State("heart-question", "value"),
               State("heart-detail-question", "value"), 
               State("obesity-question", "value"),
               State("diabetes-question", "value"), 
               State("cystic-question", "value"), 
               State("lung-question", "value"),
               State("immune-question", "value"), 
               State("kidney-question", "value"),
               ])

def update_progress_bar(gender, age, heart, heart_detail, obesity, diabetes, cystic, lung, immune, kidney, gender_state, age_state, heart_state, heart_detail_state, obesity_state, diabetes_state, cystic_state, lung_state, immune_state, kidney_state):
    value = 0
    
    if gender != None:
        value += 10
    
    if age > 0:
        value += 10
    
    if heart == "No":
        value += 10
    elif (heart == "Yes") and (len(heart_detail) > 0):
        value += 10
    
    if obesity != None:
        value += 10
    
    if diabetes != None:
        value += 10
    
    if cystic != None:
        value += 10
    
    if lung != None:
        value += 10
    
    if immune != None:
        value += 10
    
    if kidney != None:
        value += 10
    
    return value * 10/9,  f"{int(value/10)}/9 QUESTIONS COMPLETE"   

# In[]
# the score bar 
score_bar = dbc.Progress(id = "prognostic_score")

# explaination
explain = html.Div(id = "prognostic-explain")

# the content of the result 
prognostic_result = html.Div([
        html.Hr(),
        html.H6("THE RISK SCORE FOR PATIENTS WITH COVID-19 AND SIMILAR CHARACTERISTICS AS YOU IS:"),
        score_bar, 
        explain
        ])
# In[]
# covid19 prognostic tool content 
content_prognostic_tool = html.Div([
        prognostic_heading,
        progress_bar,
        basic_info,
        medical_info,
        dbc.Button("COMPLETE THE QUESTIONS AND SUBMIT!", color = "primary", block = True, id = "prognostic-submit"),
#        dbc.Toast(prognostic_result, id = "prognostic-result", dismissable = True, is_open = True, 
#                  style = {"position":"relative", "top":66, "left":55, "width":700, "height":700, "color": "#dae9f4"})
        dbc.Fade(prognostic_result, id = "prognostic-result", is_in = True, appear = False)
        ], id="page-content", style = CONTENT_STYLE)

# --- enable the submitt button--- #
@app.callback([Output("prognostic-submit", "disabled"), Output("prognostic-submit", "children")],
              [Input("answer-progress-bar", "value")])

def enable_prognostic_submit_button(value):
    if value == 100:
        return False, "GO TO THE RESULTS!"
    return True, "COMPLETE THE QUESTIONS AND SUBMIT!"

# --- the callback of the submit button --- #
@app.callback([Output("gender-option", "value"), 
               Output("heart-question", "value"),
               Output("obesity-question", "value"),
               Output("diabetes-question", "value"), 
               Output("cystic-question", "value"), 
               Output("lung-question", "value"),
               Output("immune-question", "value"), 
               Output("kidney-question", "value"),
               Output("age-slider", "value")],
              [Input("prognostic-submit", "n_clicks")])

def submit_prognostic_button(n):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    submitting = len([1 for i in triggered if i == "prognostic-submit.n_clicks"])
    if submitting:
        return [None] * 8 + [0]
    return dash.no_update

# --- update the prognostic result content --- #
@app.callback([Output("prognostic-result", "is_in"),
               Output("prognostic_score", "value"),
               Output("prognostic_score", "color"), 
               Output("prognostic_score", "children"),
               Output("prognostic-explain", "children")
               ],
              [Input("prognostic-submit", "n_clicks"), 
               State("gender-option", "value"), 
               State("age-slider", "value"),
               State("heart-question", "value"),
               State("heart-detail-question", "value"), 
               State("obesity-question", "value"),
               State("diabetes-question", "value"), 
               State("cystic-question", "value"), 
               State("lung-question", "value"),
               State("immune-question", "value"), 
               State("kidney-question", "value"),
               ])
def update_prognostic_result(n, gender, age, heart, heart_detail, obesity, diabetes, cystic, lung, immune, kidney):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    submitting = len([1 for i in triggered if i == "prognostic-submit.n_clicks"])
    
    if submitting:
        explain = [html.Hr()]
        P = Prediction(predictors, target)
        P.update_q1(gender)
        P.update_q2(age)
        P.update_q3(heart, heart_detail)
        P.update_q4(obesity)
        P.update_q5(diabetes)
        P.update_q6(cystic)
        P.update_q7(lung)
        P.update_q8(immune)
        P.update_q9(kidney)
        score = P.predict_result()
        
        if heart == "Yes":
            explain.append(dbc.Card([
                    dbc.CardHeader("Heart Conditions and Other Cardiovascular and Cerebrovascular Diseases", 
                                   style = {"color":"#3a5134", "fontSize":20}),
                    dbc.CardBody([
                            html.Div("Having other cardiovascular or cerebrovascular disease, such as hypertension (high blood pressure) or stroke, might increase your risk of severe illness from COVID-19."),
                            html.B("Actions to take"),
                            html.Div("Take your medicines exactly as prescribed and follow your healthcare provider’s recommendations for diet and exercise while maintaining social distancing precautions.Continue angiotensin converting enzyme inhibitors (ACE-I) or angiotensin-II receptor blockers (ARB) as prescribed by your healthcare provider for indications such as heart failure or high blood pressure.Make sure that you have at least a 30-day supply of your heart disease medicines, including high cholesterol and high blood pressure medicines.")                            
                            ])
                    ]))

        if obesity == "Yes":
            explain.append(dbc.Card([
                    dbc.CardHeader("Overweight, Obesity and Severe Obesity",
                                   style = {"color":"#3a5134", "fontSize":20}),
                    dbc.CardBody([
                            html.Div("Having obesity, defined as a body mass index (BMI) between 30 kg/m2 and <40 kg/m2 or severe obesity (BMI of 40 kg/m2 or above), increases your risk of severe illness from COVID-19. Having overweight, defined as a BMI > 25 kg/m2 but less than 30 kg/m2 might increase your risk of severe illness from COVID-19."),
                            html.B("Actions to take"),
                            html.Div("Take your prescription medicines for overweight, obesity or severe obesity exactly as prescribed.Follow your healthcare provider’s recommendations for nutrition and physical activity, while maintaining social distancing precautions.Call your healthcare provider if you have concerns or feel sick.")                            
                            ])
                    ]))
    
        if diabetes == "Yes":
            explain.append(dbc.Card([
                    dbc.CardHeader("Diabetes",
                                   style = {"color":"#3a5134", "fontSize":20}),
                    dbc.CardBody([
                            html.Div("Having type 2 diabetes increases your risk of severe illness from COVID-19. Based on what we know at this time, having type 1 or gestational diabetes might increase your risk of severe illness from COVID-19."),
                            html.B("Actions to take"),
                            html.Div("Continue taking your diabetes pills and insulin as usual.Test your blood sugar and keep track of the results, as directed by your healthcare provider.Make sure that you have at least a 30-day supply of your diabetes medicines, including insulin.Follow your healthcare provider’s instructions if you are feeling ill as well as the sick day tips for people with diabetes.")                            
                            ])
                    ]))
        
        if cystic == "Yes" or lung == "Yes":
            explain.append(dbc.Card([
                    dbc.CardHeader("Cystic fibrosis, pulmonary fibrosis, and other chronic lung diseases",
                                   style = {"color":"#3a5134", "fontSize":20}),
                    dbc.CardBody([
                            html.Div("Having COPD (including emphysema and chronic bronchitis) is known to increase your risk of severe illness from COVID-19. Other chronic lung diseases, such as idiopathic pulmonary fibrosis and cystic fibrosis, might increase your risk of severe illness from COVID-19."),
                            html.B("Actions to take"),
                            html.Div("Keep taking your current medicines, including those with steroids in them (“steroids” is another word for corticosteroids).Make sure that you have at least a 30-day supply of your medicines.Avoid triggers that make your symptoms worse.Call your healthcare provider if you have concerns about your condition or feel sick.")                            
                            ])
                    ]))
                
        if immune == "Yes":
            explain.append(dbc.Card([
                    dbc.CardHeader("Immunocompromised state (weakened immune system) ",
                                   style = {"color":"#3a5134", "fontSize":20}),
                    dbc.CardBody([
                            html.Div("Many conditions and treatments can cause a person to be immunocompromised or have a weakened immune system. These include: having a solid organ transplant, blood, or bone marrow transplant; immune deficiencies; HIV with a low CD4 cell count or not on HIV treatment; prolonged use of corticosteroids; or use of other immune weakening medicines. Having a weakened immune system might increase your risk of severe illness from COVID-19."),
                            html.B("Actions to take"),
                            html.Div("Continue any recommended medicines or treatments and follow the advice of your healthcare provider.Make sure that you have at least a 30-day supply of your medicines.Do not stop taking your medicines without talking to your healthcare provider.")                            
                            ])
                    ]))
        
        if kidney == "Yes":
            explain.append(dbc.Card([
                    dbc.CardHeader("Chronic kidney disease",
                                   style = {"color":"#3a5134", "fontSize":20}),
                    dbc.CardBody([
                            html.Div("Having chronic kidney disease of any stage increases your risk for severe illness from COVID-19."),
                            html.B("Actions to take"),
                            html.Div("Continue your medicines and your diet as directed by your healthcare provider.Make sure that you have at least a 30-day supply of your medicines.Stay in contact with your healthcare team as often as possible, especially if you have any new signs or symptoms of illness. Also reach out to them if you can’t get the medicines or foods you need.If you don’t have a healthcare provider, contact your nearest community health centerexternal icon or health department.Have shelf-stable food choices to help you follow your kidney diet.")                            
                            ])
                    ]))
        
        if score*100 <= 25:
            color = "primary"
        elif score*100 <= 50:
            color = "info"
        elif score*100 <= 75:
            color = "warning"
        elif score*100 <= 100:
            color = "danger"
        
        result = round(score*100,2)
        
        return True, score * 100, color, f"{result}/100", explain
    else:
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update 

# In[]
quiz_heading =  html.Div([
        html.H3("COVID-19 BEHAVIOUR QUIZ"), 
        #html.H5("Estimate mortality rates in patients with COVID-19.", style = {"color":"#828187"}),
        html.Hr()
        ])

quiz1 = dbc.FormGroup([
        dbc.Label("1. What are some of the common symptoms of COVID-19? (Check all that apply)".upper(), html_for = "quiz1-question", style = {"color":"#1f5869", "fontSize":20}),
        html.Hr(),
        html.Div([dbc.Checklist(id = "quiz1-option",            
                       options = [{"label":"Sore throat", "value":1}, 
                                  {"label":"Congestion or runny nose", "value":2},
                                  {"label":"Fever or chills", "value":3},
                                  {"label":"New loss of taste or smell", "value":4}
                                  ],
                       style = {"color":"#1f5869", "fontSize":18},
                       labelCheckedStyle={"color": "#cff0da"}
                       )]),
        html.Br(),
        dbc.Button("CHECK THE ANSWER", id = "quiz1-submit", size = "sm", block = True)        
            ])

quiz2 = dbc.FormGroup([
        dbc.Label("2. DEIStancing is shorthand for the following six guidelines: maintain 6 feet of distance, wear a mask or face covering, wash your hands frequently, don’t share food or drinks, limit the size of your gatherings, and stay home when you’re sick.".upper(), html_for = "quiz2-question", style = {"color":"#1f5869", "fontSize":20}),
        html.Hr(),
        html.Div([dbc.RadioItems(id = "quiz2-option",            
                       options = [{"label":"True", "value":1}, 
                                  {"label":"False", "value":2}
                                  ],
                       style = {"color":"#1f5869", "fontSize":18},
                       labelCheckedStyle={"color": "#cff0da"}, inline = True
                       )]),
        html.Br(),
        dbc.Button("CHECK THE ANSWER", id = "quiz2-submit", size = "sm", block = True)        
            ])

quiz3 = dbc.FormGroup([
        dbc.Label("3. True or False: Masks are required on campus in all shared and public spaces, including outdoor spaces on campus, even if you are alone in those spaces.".upper(), html_for = "quiz3-question", style = {"color":"#1f5869", "fontSize":20}),
        html.Hr(),
        html.Div([dbc.RadioItems(id = "quiz3-option",            
                       options = [{"label":"True", "value":1}, 
                                  {"label":"False", "value":2}
                                  ],
                       style = {"color":"#1f5869", "fontSize":18},
                       labelCheckedStyle={"color": "#cff0da"}, inline = True
                       )]),
        html.Br(),
        dbc.Button("CHECK THE ANSWER", id = "quiz3-submit", size = "sm", block = True)        
            ])
    
quiz4 = dbc.FormGroup([
        dbc.Label("4. True or False: It is required to maintain 6 feet of distance from others only when you are not wearing a mask.".upper(), html_for = "quiz4-question", style = {"color":"#1f5869", "fontSize":20}),
        html.Hr(),
        html.Div([dbc.RadioItems(id = "quiz4-option",            
                       options = [{"label":"True", "value":1}, 
                                  {"label":"False", "value":2}
                                  ],
                       style = {"color":"#1f5869", "fontSize":18},
                       labelCheckedStyle={"color": "#cff0da"}, inline = True
                       )]),
        html.Br(),
        dbc.Button("CHECK THE ANSWER", id = "quiz4-submit", size = "sm", block = True)        
            ])

quiz5 = dbc.FormGroup([
        dbc.Label("5. How many days in a row should you wear your mask before washing it?".upper(), html_for = "quiz5-question", style = {"color":"#1f5869", "fontSize":20}),
        html.Hr(),
        html.Div([dbc.RadioItems(id = "quiz5-option",            
                       options = [{"label":"1", "value":1}, 
                                  {"label":"2", "value":2},
                                  {"label":"3", "value":3},
                                  {"label":"7", "value":7}
                                  ],
                       style = {"color":"#1f5869", "fontSize":18},
                       labelCheckedStyle={"color": "#cff0da"}
                       )]),
        html.Br(),
        dbc.Button("CHECK THE ANSWER", id = "quiz5-submit", size = "sm", block = True)        
            ])
   
    
# the content of covid quiz 
content_quiz = html.Div([
        quiz_heading,
        dbc.Alert([
                quiz1,               
                ], color = "light"),
        dbc.Alert([
                quiz2
                ], color = "light"),
        dbc.Alert([
                quiz3
                ], color = "light"),
        dbc.Alert([
                quiz4
                ], color = "light"),
        dbc.Alert([
                quiz5
                ], color = "light")
    

        
        ], id="page-content", style = CONTENT_STYLE)
#content_prognostic_tool = html.Div([
#        prognostic_heading,
#        progress_bar,
#        basic_info,
#        medical_info,
#        dbc.Button("COMPLETE THE QUESTIONS AND SUBMIT!", color = "primary", block = True, id = "prognostic-submit"),
##        dbc.Toast(prognostic_result, id = "prognostic-result", dismissable = True, is_open = True, 
##                  style = {"position":"relative", "top":66, "left":55, "width":700, "height":700, "color": "#dae9f4"})
#        dbc.Fade(prognostic_result, id = "prognostic-result", is_in = True, appear = False)
#        ], id="page-content", style = CONTENT_STYLE)

# --- the callback of submit button --- #
@app.callback(
               [Output("quiz1-option", "value"),
                Output("quiz2-option", "value"),
                Output("quiz3-option", "value"),
                Output("quiz4-option", "value"),
                Output("quiz5-option", "value")
                ],
               [Input("quiz1-submit", "n_clicks"),
                Input("quiz2-submit", "n_clicks"),
                Input("quiz3-submit", "n_clicks"),
                Input("quiz4-submit", "n_clicks"),
                Input("quiz5-submit", "n_clicks")
                ])
def show_answer(n1, n2, n3, n4, n5):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    n1 = len([1 for i in triggered if i == "quiz1-submit.n_clicks"])
    n2 = len([1 for i in triggered if i == "quiz2-submit.n_clicks"])
    n3 = len([1 for i in triggered if i == "quiz3-submit.n_clicks"])
    n4 = len([1 for i in triggered if i == "quiz4-submit.n_clicks"])
    n5 = len([1 for i in triggered if i == "quiz5-submit.n_clicks"])

    if n1:
        return [1,2,3,4], dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if n2:
        return dash.no_update, 1, dash.no_update, dash.no_update, dash.no_update
    if n3:
        return dash.no_update, dash.no_update, 1, dash.no_update, dash.no_update
    if n4:
        return dash.no_update, dash.no_update, dash.no_update, 2, dash.no_update
    if n5:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, 1
     
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update 


# In[]
# App layout 
#app.layout = dbc.Container([
#        dcc.Location(id="url"),
#        nav_bar,
#        html.Hr(),
#        sidebar, 
#        content 
#        ], fluid = True)

app.layout = html.Div([
        dcc.Location(id="url"),
        nav_bar,
        html.Hr(),
        dbc.Row([
                dbc.Col(sidebar, md = 2.7),
                dbc.Col(md = 0.3),
                #dbc.Col(content_prognostic_tool, md = 9.0)
                #dbc.Col(content_quiz, md = 9.0)
                dbc.Col(id = "total-content", md = 9.0)
                ])
        ])

# --- changing the page --- #
@app.callback(Output("total-content", "children"), Input("url", "pathname"))

def update_pathname(pathname):
    if pathname in ["/", "/covid-prognostic-tool"]:
        return content_prognostic_tool
    elif pathname == "/covid-quiz":
        return content_quiz
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

        
# In[]
# Main
if __name__ == "__main__":
    app.run_server(debug=True)

