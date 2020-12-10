# COVID-19 Web Application 
This web applicaiton contains two tools: 
* the COVID-19 risk score calculator 
* the COVID-19 behaviour quiz
![Image](https://github.com/heyif/Dash-Web-Application/blob/main/asset/Screenshot1.png)

## About the App

### COVID-19 Risk Calculator 
#### Introduction
The first on is the COVID-19 risk score calculator, which trains a XGBoost model on a synthetic dataset based on the real patient sample from APCD `Covid19_SourceFile.xlsx` to estimate mortality probability in Covid-19 patients with certain characteristics and pre-existing medical conditions.

Here users are required to select both basic information as well as their medical conditions. 
![Image](https://github.com/heyif/Dash-Web-Application/blob/main/asset/Screenshot2.png)
![Image](https://github.com/heyif/Dash-Web-Application/blob/main/asset/Screenshot3.png)

After that, the model will analyze and calculate the risk score. According to the health condition the user provides, the app will also demonstrate some suggestions.  
![Image](https://github.com/heyif/Dash-Web-Application/blob/main/asset/Screenshot4.png)

#### Model Training 
The XGBoost model training part is included in the `ModelTuning.py`

### COVID-19 Behaviour Quiz 
#### Introduction
The app also provides information people should know about Covid-19 in the form of a 5-question quiz. 
![Image](https://github.com/heyif/Dash-Web-Application/blob/main/asset/Screenshot5.png)

## How to Run the App Locally
Clone this repo
```
git clone https://github.com/heyif/Dash-Web-Application.git
cd Dash-Web-Application
```

Create a conda env
```
conda create -n Dash-Web-Application python=3.6.7
conda activate Dash-Web-Application
# Or
source activate Dash-Web-Application
```
Install required packages
```
pip install xgboost
# if you have problem with installing xgboost on Mac OS
conda install -c conda-forge xgboost
pip install pandas 
pip install dash
pip install dash-bootstrap-components
pip install dash-core-components
pip install dash-html-components
```

Run the app
```
python app.py
```
Finally visit http://127.0.0.1:8050/

