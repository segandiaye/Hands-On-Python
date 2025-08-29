"""
Class lecture
"""
# 1
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

#2
from pydantic import BaseModel #  for Data validation as class models
from typing import List

#3
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import uuid # creating a unique ID
import pickle # to save models

from fastapi import FastAPI
app = FastAPI()

###################    
MODELS = {
    "lr": {
        "model": LogisticRegression,
        "name": "Logistic Regression",
        "api_model_code": "lr",
        "documentation": "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html"
    },
    "dt": {
        "model": DecisionTreeClassifier,
        "name": "Decision Tree",
        "api_model_code": "dt",
        "documentation": "https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html"
    },
    "knn": {
        "model": KNeighborsClassifier,
        "name": "K Nearest Neighbors",
        "api_model_code": "knn",
        "documentation": "https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html"
    }
}

IRIS_TYPES = {
    0: 'setosa',
    1: 'versicolor',
    2: 'virginica' 
}

############ Listing the supported types of ML models
class ModelInfo(BaseModel):
    name: str
    api_model_code: str
    documentation: str = None
        

@app.get("/model/info/", response_model=List[ModelInfo])
async def info_models():
    result = []
    for model_key in MODELS:
        model_info = MODELS[model_key]
        result.append(model_info)
    return result

########### Creating and training new ML models
class ModelTrainIn(BaseModel):
    api_model_code: str
    trained_model_name: str

class ModelTrainOut(BaseModel):
    train_id: str = None
    api_model_code: str = None
    trained_model_name: str = None
    accuracy: float = None
    
@app.post("/model/train/", response_model=ModelTrainOut) # here we're defining the data model for our response
async def train_model(model_train: ModelTrainIn): # this defines the data model for our request
    # we transform our data model object into a dictionary
    model_train_dict = model_train.dict() 
    
    # we initialize our ML model
    model = MODELS[model_train_dict['api_model_code']]['model']() # we initialize our ML model
    
    # load and split data
    data = load_iris()
    X = data.data
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, stratify=y, random_state=42)
    
    # fit model and get a prediction and a score
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # we define a unique ID
    unique_id = uuid.uuid4().hex 
    
    # saving the model locally 
    filename = f"trained_models/{unique_id}.sav"
    pickle.dump(model, open(filename, 'wb')) 
    model_train_dict.update({"train_id": unique_id, "accuracy": accuracy})
    
    # return our response that has the same data structure as ModelTrainOut
    return model_train_dict 

########## Running predictions with user data
class ModelIrisPredictIn(BaseModel):
    train_id: str
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width : float

class ModelIrisPredictOut(BaseModel):
    type_predicted: str
    proba_setosa: float
    proba_versicolor: float
    proba_virginica: float
    train_id: str
    
@app.post("/model/predict/", response_model=ModelIrisPredictOut)
async def predict_iris(iris_data: ModelIrisPredictIn):
    iris_data_dict = iris_data.dict()
    train_id = iris_data_dict['train_id']
    
    # loading the saved ML Model
    model = pickle.load(open(f"trained_models/{train_id}.sav", 'rb')) 
    data = [
                [
                    iris_data_dict['sepal_length'],
                    iris_data_dict['sepal_width'],
                    iris_data_dict['petal_length'],
                    iris_data_dict['petal_width']
                ]
            ]
    pred = model.predict(data)[0]
    proba = model.predict_proba(data)[0]
    return {
        "type_predicted": IRIS_TYPES[pred],
        "proba_setosa": proba[0],
        "proba_versicolor": proba[1],
        "proba_virginica": proba[2],
        "train_id": train_id
    }
