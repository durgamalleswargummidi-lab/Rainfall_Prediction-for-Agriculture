import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
data = pd.read_csv("weatherAUS.csv")
data = data.dropna()
data['RainToday'] = data['RainToday'].map({'No':0,'Yes':1})
data['RainTomorrow'] = data['RainTomorrow'].map({'No':0,'Yes':1})
X = data[['MinTemp','MaxTemp','Rainfall','Humidity9am','Humidity3pm','RainToday']]
y = data['RainTomorrow']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:\n")
print(classification_report(y_test, predictions))
API_KEY = "72343e3221b9dc586da175e40ee4e559"
CITY = "visakhapatnam,IN"
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
response = requests.get(url)
if response.status_code == 200:
    weather = response.json()
    temperature = weather['main']['temp']
    humidity = weather['main']['humidity']
    if 'rain' in weather:
        rainfall = weather['rain'].get('1h',0)
    else:
        rainfall = 0
    print("\nCurrent Weather Data")
    print("City:", CITY)
    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity,"%")
    print("Rainfall:", rainfall,"mm")
    MinTemp = temperature - 2
    MaxTemp = temperature + 2
    Rainfall = rainfall
    Humidity9am = humidity
    Humidity3pm = max(humidity - 5,0)
    RainToday = 1 if rainfall > 0 else 0
    sample = pd.DataFrame([[MinTemp,MaxTemp,Rainfall,Humidity9am,Humidity3pm,RainToday]],
    columns=['MinTemp','MaxTemp','Rainfall','Humidity9am','Humidity3pm','RainToday'])
    result = model.predict(sample)
    print("\nPrediction Result:")
    if result[0] == 1:
        print("Rain Tomorrow")
    else:
        print("No Rain Tomorrow")
else:
    print("Error: Unable to fetch weather data from API")

=========================
SAMPLE OUTPUT

Model Accuracy: 0.7502658631690889

Classification Report:

              precision    recall  f1-score   support

           0       0.84      0.83      0.84      8799
           1       0.44      0.46      0.45      2485

    accuracy                           0.75     11284
   macro avg       0.64      0.65      0.64     11284
weighted avg       0.75      0.75      0.75     11284


Current Weather Data
City: visakhapatnam,IN
Temperature: 32.94 °C
Humidity: 55 %
Rainfall: 0 mm

Prediction Result:
Rain Tomorrow

==========================
