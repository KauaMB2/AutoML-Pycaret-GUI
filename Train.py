import os
from datetime import datetime
from pycaret.regression import *
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

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

class Train:
    def __init__(self, trainingPorcentage, inputsList, targetsList):
        self.__inputsList = inputsList
        self.__targetsList = targetsList
        self.__trainingPercentage = percentageHashTable[trainingPorcentage]

    def trainModel(self, data):
        # Create models directory if it doesn't exist
        if not os.path.exists("models"):
            os.makedirs("models")

        # Create a subdirectory with the current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        model_dir = os.path.join("models", timestamp)

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        for target in self.__targetsList:
            # Split the data into training and testing sets
            train_data, test_data = train_test_split(data[self.__targetsList + self.__inputsList], 
                                                      test_size=(1.0 - self.__trainingPercentage), 
                                                      random_state=123)

            # Initialize PyCaret setup for regression with training data
            exp1 = setup(train_data, target=target, session_id=123)

            # Compare machine learning models
            best_model = compare_models()

            # Create and tune the best model
            tuned_model = tune_model(best_model)

            # Save the model locally in the specified directory
            model_path = os.path.join(model_dir, f'{target}_model')
            save_model(tuned_model, model_path)

            # Make predictions on the test set
            predictions = predict_model(tuned_model, data=test_data)

            # Calculate Mean Squared Error
            mse = mean_squared_error(test_data[target], predictions['prediction_label'])

            print(f'Mean Squared Error for {target}: {mse:.2f}')
