from . import WMLDeployment
import os


class MulticlassDigits(WMLDeployment):
    def __init__(self):
        super(MulticlassDigits, self).__init__(
            name="AIOS Scikit Digits",
            asset_name="AIOS Scikit Digits"
        )

    def publish_model(self):
        from sklearn import datasets
        from sklearn import preprocessing
        from sklearn import svm
        from sklearn.pipeline import Pipeline

        model_data = datasets.load_digits()
        scaler = preprocessing.StandardScaler()
        clf = svm.SVC(kernel='rbf', probability=True)
        pipeline = Pipeline([('scaler', scaler), ('svc', clf)])
        model = pipeline.fit(model_data.data, model_data.target)
        predicted = model.predict(model_data.data[1: 10])
        predicted_probs = model.predict_proba(model_data.data[1: 10])

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "scikit-learn_0.20",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "scikit-learn_0.20-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: {},
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.19",
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "accuracy",
                        "value": 0.64,
                        "threshold": 0.8
                    }
                ]
            }
        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model,
                                                                         meta_props=model_props,
                                                                         training_data=model_data.data,
                                                                         training_target=model_data.target)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class MulticlassGolf(WMLDeployment):
    filename = 'datasets/golf/golf_train_data.csv'

    def __init__(self):
        super(MulticlassGolf, self).__init__(
            name="AIOS Scikit Golf",
            asset_name="AIOS Scikit Golf"
        )

    def publish_model(self):
        import pandas as pd

        label_column = ['total_label']
        feature_list_columns = ['crowd_score', 'gesture_score', 'face_score',
                                'speaker_sound_score', 'age', 'country', 'years_professional',
                                'tourn_entered', 'play_status', 'hole',
                                'ground', 'stroke', 'par_number', 'hole_yardage', 'hit_bunker',
                                'hit_fairway', 'green_in_regulation', 'putts', 'sand_save',
                                'player_rank',
                                'player_in_top10', 'player_tied', 'in_water', 'ball_position',
                                'shot_length', 'penalty', 'last_shot', 'is_eagle_or_better',
                                'is_birdie', 'is_par',
                                'is_bogey', 'is_double_bogey_or_worse', 'close_approach',
                                'long_putt', 'feels_like', 'temperature', 'heat_index',
                                'barometric_pressure',
                                'relative_humidity']
        data = pd.read_csv(self.filename)

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "scikit-learn_0.20",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "scikit-learn_0.20-py3.6",
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "Aaron Baughman",
                self.wml_client.repository.ModelMetaNames.NAME: "SVCHighlights",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "scikit-learn",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.19",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
            }

        path_to_model = "./artifacts/golf/downloaded_artifact.tar.gz"
        import tarfile
        tar = tarfile.open(path_to_model, "r:gz")
        tar.extractall("./artifacts/golf/")
        tar.close()
        from sklearn.externals import joblib
        path_to_model_pkl = "./artifacts/golf/scikit_model.pkl"
        model = joblib.load(path_to_model_pkl)

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model,
                                                                         meta_props=model_props,
                                                                         training_data=data[feature_list_columns],
                                                                         training_target=data[label_column])

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class RegressionDiabetes(WMLDeployment):
    def __init__(self):
        super(RegressionDiabetes, self).__init__(
            name="AIOS Scikit Regression Diabetes",
            asset_name="AIOS Scikit Regression Diabetes"
        )

    def publish_model(self):
        from sklearn import datasets, linear_model
        from sklearn.metrics import mean_squared_error, r2_score
        diabetes_data = datasets.load_diabetes()

        diabetes_X = diabetes_data.data
        print('sample data records', diabetes_data.data[1, :].tolist())

        # Split the data into training/testing sets
        diabetes_X_train = diabetes_X[:-20]
        diabetes_X_test = diabetes_X[-20:]

        # Split the targets into training/testing sets
        diabetes_y_train = diabetes_data.target[:-20]
        diabetes_y_test = diabetes_data.target[-20:]

        # Create linear regression object
        model = linear_model.LinearRegression()

        # Train the model using the training sets
        model.fit(diabetes_X_train, diabetes_y_train)

        # Make predictions using the testing set
        diabetes_y_pred = model.predict(diabetes_X_test)

        print('predictions', diabetes_y_pred)

        # The coefficients
        print('Coefficients: \n', model.coef_)
        # The mean squared error
        print("Mean squared error: %.2f"
              % mean_squared_error(diabetes_y_test, diabetes_y_pred))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "scikit-learn_0.20",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "scikit-learn_0.20-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: {},
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model,
                                                                         meta_props=model_props,
                                                                         training_data=diabetes_data.data,
                                                                         training_target=diabetes_data.target)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class RegressionDiabetesWithXGBoost(WMLDeployment):
    def __init__(self):
        super(RegressionDiabetesWithXGBoost, self).__init__(
            name="AIOS Scikit-XGBoost Regression Diabetes",
            asset_name="AIOS Scikit-XGBoost Regression Diabetes"
        )

    def publish_model(self):
        from sklearn import datasets
        from sklearn.metrics import mean_squared_error, r2_score
        from xgboost import XGBRegressor
        from sklearn.pipeline import Pipeline

        diabetes_data = datasets.load_diabetes()

        diabetes_X = diabetes_data.data
        print('sample data records', diabetes_data.data[1, :].tolist())

        # Split the data into training/testing sets
        diabetes_X_train = diabetes_X[:-20]
        diabetes_X_test = diabetes_X[-20:]

        # Split the targets into training/testing sets
        diabetes_y_train = diabetes_data.target[:-20]
        diabetes_y_test = diabetes_data.target[-20:]

        # Create linear regression object
        xgb_regressor = XGBRegressor(booster='gblinear')

        # Create pipeline
        pipeline = Pipeline([('linear', xgb_regressor)])

        # Train the model using the training sets
        model = pipeline.fit(diabetes_X_train, diabetes_y_train)

        # Make predictions using the testing set
        predicted = model.predict(diabetes_X_test)

        print('predictions', predicted)

        # The mean squared error
        print("Mean squared error: %.2f"
              % mean_squared_error(diabetes_y_test, predicted))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(diabetes_y_test, predicted))

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "scikit-learn_0.20",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "scikit-learn_0.20-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: {},
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model,
                                                                         meta_props=model_props,
                                                                         training_data=diabetes_data.data,
                                                                         training_target=diabetes_data.target)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))
