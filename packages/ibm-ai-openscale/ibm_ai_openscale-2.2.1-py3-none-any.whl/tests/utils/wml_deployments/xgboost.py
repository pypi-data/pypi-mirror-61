from . import WMLDeployment
import os
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston, load_iris
from sklearn.datasets import load_svmlight_file
import xgboost as xgb
import pandas as pd


class BostonHouse(WMLDeployment):
    def __init__(self):
        super(BostonHouse, self).__init__(
            name="AIOS Xgboost Boston House Deployment V4",
            asset_name="AIOS Xgboost Boston House Model V4"
        )

    def publish_model(self):
        boston_dataset = load_boston()

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TYPE: "xgboost_0.82",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "xgboost_0.82-py3.6",
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.8",
            }

        data = pd.DataFrame(boston_dataset.data)
        data.columns = boston_dataset.feature_names
        X, y = data.iloc[:, :-1], data.iloc[:, -1]
        data_dmatrix = xgb.DMatrix(data=X, label=y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1, max_depth=5,
                                  alpha=10, n_estimators=10)

        xg_reg.fit(X_train, y_train)

        # preds = xg_reg.predict(X_test)
        #
        # bst = xgb.XGBRegressor()
        # bst.load_model("artifacts/XGboost/boston-house-xgboost.model")

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=xg_reg,
                                                                         training_data=X_train,
                                                                         training_target=y_train,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class Solar(WMLDeployment):
    def __init__(self):
        super(Solar, self).__init__(
            name="AIOS Xgboost Solar Deployment",
            asset_name="AIOS Xgboost Solar Model"
        )

    def publish_model(self):
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TYPE: "xgboost_0.82",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "xgboost_0.82-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.8",
            }

        data = pd.read_csv('datasets/XGboost/SolarPrediction.csv')
        final_data = data.drop(['UNIXTime', 'Data', 'Time', 'TimeSunRise', 'TimeSunSet'], axis=1)
        final_y = final_data.pop('Radiation')
        final_x = final_data
        X_train, X_test, y_train, y_test = train_test_split(final_x, final_y, test_size=0.33, random_state=42)
        xgdmat = xgb.DMatrix(X_train, y_train)
        our_params = {'eta': 0.1, 'seed': 0, 'subsample': 0.8, 'colsample_bytree': 0.8, 'objective': 'reg:linear',
                      'max_depth': 3, 'min_child_weight': 1}
        final_gb = xgb.train(our_params, xgdmat)
        tesdmat = xgb.DMatrix(X_test)
        y_pred = final_gb.predict(tesdmat)

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=final_gb,
                                                                         training_data=X_train,
                                                                         training_target=y_train,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class Iris(WMLDeployment):
    def __init__(self):
        super(Iris, self).__init__(
            name="AIOS Xgboost Iris Deployment v4",
            asset_name="AIOS Xgboost Iris Model v4"
        )

    def publish_model(self):
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TYPE: "xgboost_0.82",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "xgboost_0.82-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.8",
            }

        iris = load_iris()
        X = iris.data
        y = iris.target
        X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
        D_train = xgb.DMatrix(X_train, label=Y_train)
        D_test = xgb.DMatrix(X_test, label=Y_test)
        param = {
            'eta': 0.3,
            'max_depth': 3,
            'objective': 'multi:softmax',
            'num_class': 4}

        steps = 20
        model = xgb.train(param, D_train, steps)
        preds = model.predict(D_test)

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model,
                                                                         training_data=X_train,
                                                                         training_target=Y_train,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class Agaricus(WMLDeployment):
    def __init__(self):
        super(Agaricus, self).__init__(
            name="AIOS Xgboost Agaricus vx2 Deployment",
            asset_name="AIOS Xgboost Agaricus xv2 Model"
        )

    def publish_model(self):
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TYPE: "xgboost_0.82",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "xgboost_0.82-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.8",
            }

        dtrain = xgb.DMatrix(os.path.join(os.getcwd(), 'datasets', 'XGboost', 'agaricus.txt.train'),
                             feature_names=['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f69', 'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f79', 'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88', 'f89', 'f90', 'f91', 'f92', 'f93', 'f94', 'f95', 'f96', 'f97', 'f98', 'f99', 'f100', 'f101', 'f102', 'f103', 'f104', 'f105', 'f106', 'f107', 'f108', 'f109', 'f110', 'f111', 'f112', 'f113', 'f114', 'f115', 'f116', 'f117', 'f118', 'f119', 'f120', 'f121', 'f122', 'f123', 'f124', 'f125', 'f126'],
                             feature_types=['float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float'])
        dtest = xgb.DMatrix(os.path.join(os.getcwd(), 'datasets', 'XGboost', 'agaricus.txt.test'))
        # specify parameters via map
        param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
        num_round = 2
        bst = xgb.train(param, dtrain)

        # make prediction
        preds = bst.predict(dtest)

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=bst,
                                                                         training_data=dtrain,
                                                                         feature_names=bst.feature_names,
                                                                         meta_props=model_props)

        print("Published model details:\n{}".format(published_model_details))
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))
