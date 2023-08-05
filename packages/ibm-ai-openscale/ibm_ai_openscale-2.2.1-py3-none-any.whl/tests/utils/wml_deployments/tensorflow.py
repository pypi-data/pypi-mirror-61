from . import WMLDeployment
import os


class Binary(WMLDeployment):
    def __init__(self):
        super(Binary, self).__init__(
            name="AIOS TF Structured Model",
            asset_name="AIOS TF Structured Deployment"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'tf-saved_model.tar.gz')

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "tensorflow_1.13",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "tensorflow_1.13-py3.6",
            }
        else:
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "John Smith",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.13",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.6"
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(
            model=model_path,
            meta_props=model_props)

        print("Published model details:\n{}".format(published_model_details))
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)
