"""
Persist Model
"""
# TODO : this code is not OK

from pymongo import MongoClient 
from fastapi import FastAPI

client = MongoClient('localhost', 27017)
db = client["iris_api"]
models_mg = db["models"]

# Saving trained models' metadata in MongoDB
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
    
    ###############
    
    # THIS IS THE NEW LINE WE JUST INSERTED
    # saving the information into MongoDB
    models_mg.insert_one(model_train_dict) 
    
    ###############
    
    # return our response that has the same data structure as ModelTrainOut
    return model_train_dict 

# Listing available models
@app.get("/model/list/", response_model=List[ModelTrainOut])
async def trained_models():
    result = models_mg.find({}, {"_id": 0})
    return list(result)


@app.get("/model/{train_id}", response_model=ModelTrainOut)
async def trained_models(train_id: str):
    result = models_mg.find_one({"train_id": train_id}, {"_id": 0})
    return result

# Updating available models
@app.patch("/model/update/{train_id}", response_model=ModelTrainOut)
async def update_trained_model(train_id: str, model_train: ModelTrainOut):
    
    # We query the database for the metadata matching the train_id
    stored_model_train = models_mg.find_one({"train_id": train_id})
    # We convert the result to a pydantic Model
    stored_model_train = ModelTrainOut(**stored_model_train) 
    
    # User input contains the fields to be modified, we conver the user input to python dict
    # We allow keys to be missing
    update_data = model_train.dict(exclude_unset=True) 
    # We write the new object to database
    models_mg.update_one({"train_id": train_id}, {"$set": update_data})
    
    # We create our return Model object by overwriting the object we got from database 
    # using the update_data we received from the user. 
    updated_item = stored_model_train.copy(update=update_data)
    return updated_item

