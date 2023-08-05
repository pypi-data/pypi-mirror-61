from . import WMLDeployment
import os


class Iris(WMLDeployment):
    def __init__(self):
        super(Iris, self).__init__(
            name="AIOS Keras Iris deployment V4xxx",
            asset_name="AIOS Keras Iris model V4xxx"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'iris', 'iris-model.h5.tgz')

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class BinaryDogsCats(WMLDeployment):
    def __init__(self):
        super(BinaryDogsCats, self).__init__(
            name="AIOS Keras Binary Dogs vs Cats deployment V4",
            asset_name="AIOS Keras Binary Dogs vs Cats model V4"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'dogs-vs-cats', 'dogs-vs-cats-model.h5.tgz')
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class BinarySpam(WMLDeployment):
    def __init__(self):
        super(BinarySpam, self).__init__(
            name="AIOS Keras Binary Spam deployment V4",
            asset_name="AIOS Keras Binary Spam model V4"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'spam-classification', 'spam-classification.h5.tgz')
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class Lstm(WMLDeployment):
    def __init__(self):
        super(Lstm, self).__init__(
            name="AIOS Keras LSTM V4",
            asset_name="AIOS Keras LSTM V4"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'keras-lstm', '2019127_1dcnn-lstm_po750_ep15.h5.tgz')
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class MulticlassMnist(WMLDeployment):
    def __init__(self):
        super(MulticlassMnist, self).__init__(
            name="AIOS Keras Multiclass Mnist V4",
            asset_name="AIOS Keras Multiclass Mnist V4"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'core_ml', 'keras', 'mnistCNN.h5.tgz')
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class StackOverflow(WMLDeployment):
    def __init__(self):
        super(StackOverflow, self).__init__(
            name="AIOS Keras Multiclass StackOverflow V4",
            asset_name="AIOS Keras Multiclass StackOverflow V4"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'stack-overflow', 'stack-overflow.h5.tgz')
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))


class PolandHousePrices(WMLDeployment):
    def __init__(self):
        super(PolandHousePrices, self).__init__(
            name="AIOS Keras Regression Poland House Prices V4",
            asset_name="AIOS Keras Regression Poland House Prices V4"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'poland_house_prices', 'poland_house_prices.h5.tgz')
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "keras_2.2.4-tf",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6"
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.14",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.2.4'}],
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))
