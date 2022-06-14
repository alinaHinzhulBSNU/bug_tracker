import pandas, numpy
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


# Groups items by status
def get_data_for_statistics(dataset):
    data = list_to_dataframe(dataset)
    if data is not None:
        return data.groupby(["status"])["status"].count()


# Makes predictions about item`s progress based on severity and performer
def predict_time_for_item_by_ml(performer, severity, items):
    data_frame = list_to_dataframe(items)

    if data_frame is not None and len(data_frame) > 4:
        # Clean data
        X = data_frame[["severity", "performer_id"]]  # data (input)
        y = data_frame["end_time"] - data_frame["start_time"]  # answers

        # Split data into Training/Test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2)

        # Train model
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Make prediction
        prediction = model.predict([[severity, performer.id]])[0]

        return numpy.timedelta64(prediction, "D")
    else:
        return "Not enough data for machine learning. Sorry :("


# Converts list to DataFrame
def list_to_dataframe(list_of_models):
    if len(list_of_models) > 0:
        row = list_of_models[0].__dict__
        columns = row.keys()

        return pandas.DataFrame(
            [
                [getattr(row, col) for col in columns]
                for row in list_of_models
            ],
            columns=columns
        )
