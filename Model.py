import os
from datetime import datetime
from pycaret.regression import *
import pandas as pd
from sklearn.model_selection import train_test_split
import json

percentageHashTable = {
    "50%": 0.50,
    "55%": 0.55,
    "60%": 0.60,
    "65%": 0.65,
    "70%": 0.70,
    "75%": 0.75,
    "80%": 0.80,
    "85%": 0.85,
    "90%": 0.90
}

class Model:
    def __init__(self, trainingPorcentage, inputsList, targetsList):
        self.__inputsList = inputsList
        self.__targetsList = targetsList
        self.__trainingPercentage = percentageHashTable[trainingPorcentage]

    def trainModel(self, data):
        if not os.path.exists("models"):# Create models directory if it doesn't exist
            os.makedirs("models")

        # Create a subdirectory with the current date and time
        timestamp = datetime.now().strftime("%d_%H_%M_%S")
        model_dir = os.path.join("models", timestamp)

        config_path = os.path.join(model_dir, 'config.json')# Define the path for the config.json file
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        config_data={
            "modelsAmount":0,
            "modelsFileName":[],
            "modelsInput":self.__inputsList
        }
        for target in self.__targetsList:
            # Split the data into training and testing sets
            train_data, test_data = train_test_split(data[[target] + self.__inputsList], 
                                                      test_size=(1.0 - self.__trainingPercentage), 
                                                      random_state=123)
            setup(train_data, target=target, session_id=123)# Initialize PyCaret setup for regression with training data
            best_model = compare_models()# Compare machine learning models
            tuned_model = tune_model(best_model)# Create and tune the best model
            model_path = os.path.join(model_dir, f'{target}_model')# Save the model locally in the specified directory
            save_model(tuned_model, model_path)
            config_data["modelsAmount"] += 1
            config_data["modelsFileName"].append(f'{target}_model')
            with open(config_path, 'w') as json_file:# Save the data to config.json
                json.dump(config_data, json_file, indent=4)
            predict_model(tuned_model, data=test_data)# Make predictions on the test set
    def Predict(self, inputData, configData, folderName, DIR):
        # Convert the input list to a DataFrame
        input_df = pd.DataFrame([inputData])  # Create a DataFrame with a single row
        input_df.columns = configData["modelsInput"]  # Set the DataFrame column names
        predictionsResult=[]
        predictionsMessage=""
        for modelName in configData["modelsFileName"]:
            model=load_model(fr"{DIR}\models\{folderName}\{modelName}")  # Load the model and generate predictions
            currentPrediction=predict_model(model, data=input_df)["prediction_label"][0]
            predictionsResult.append(currentPrediction)
            predictionsMessage+=f"{modelName}: {currentPrediction}\n"
        print(predictionsMessage)
        return predictionsMessage