import pandas
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib


def get_data_for_statistics(dataset):
    data = list_to_dataframe(dataset)
    return data.groupby(["status"])["status"].count()


'''def predict_by_ml(performer, severity, tasks):
    try:
        model = joblib.load('time_recomender.joblib')  # try to load model
    except:
        # Load data
        tasks_data = list_to_dataframe(tasks)

        if tasks_data is not None:
            # Clean data
            X = tasks_data.drop(columns=['genre', 'date', 'name', '_state', 'id'])  # data (input)
            y = tasks_data['genre']  # answers (output)

            # Split data into Training/Test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            # Train model
            model = DecisionTreeClassifier()
            model.fit(X_train, y_train)

            # Save model
            joblib.dump(model, 'music-recommender.joblib')
    else:
        # Make prediction
        predictions = model.predict([[age, gender]])
        return predictions[0]'''


def list_to_dataframe(list_of_models):
    if len(list_of_models) > 0:
        row = list_of_models[0].__dict__
        columns = row.keys()

        return pandas.DataFrame(
            [[getattr(row, col) for col in columns] for row in list_of_models], columns=columns
        )