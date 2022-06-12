import pandas, numpy
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def get_data_for_statistics(dataset):
    data = list_to_dataframe(dataset)
    return data.groupby(["status"])["status"].count()


def predict_time_for_task_by_ml(performer, severity, tasks):
    tasks_data = list_to_dataframe(tasks)

    if tasks_data is not None:
        # Clean data
        X = tasks_data.drop(columns=[  # data (input)
            "id",
            "_state",
            "text",
            "start_time",
            "end_time",
            "status",
            "project_id", ]
        )

        y = tasks_data["end_time"] - tasks_data["start_time"]  # answers (output)

        # Split data into Training/Test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Train model
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Make prediction
        prediction = model.predict([[severity, performer.id]])[0]

        return numpy.timedelta64(prediction, "D")


def list_to_dataframe(list_of_models):
    if len(list_of_models) > 0:
        row = list_of_models[0].__dict__
        columns = row.keys()

        return pandas.DataFrame(
            [[getattr(row, col) for col in columns] for row in list_of_models], columns=columns
        )
