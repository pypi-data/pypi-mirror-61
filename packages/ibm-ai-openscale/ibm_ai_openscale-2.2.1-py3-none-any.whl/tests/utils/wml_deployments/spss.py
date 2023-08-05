from . import WMLDeployment
import os


class CustomerSatisfaction(WMLDeployment):
    def __init__(self):
        super(CustomerSatisfaction, self).__init__(
            name="AIOS SPSS Customer Deployment",
            asset_name="AIOS SPSS Customer Model"
        )

    def publish_model(self):
        model_path = os.path.join(os.getcwd(), 'artifacts', 'SPSSCustomerSatisfaction',
                                  'customer-satisfaction-prediction.str')
        input_data_schema = {
            'id': '1',
            "fields": [
                {'name': "customerID", 'type': 'string'},
                {'name': "gender", 'type': 'string'},
                {'name': "SeniorCitizen", 'type': 'integer'},
                {'name': "Partner", 'type': 'string'},
                {'name': "Dependents", 'type': 'string'},
                {'name': "tenure", 'type': 'integer'},
                {'name': "PhoneService", 'type': 'string'},
                {'name': "MultipleLines", 'type': 'string'},
                {'name': "InternetService", 'type': 'string'},
                {'name': "OnlineSecurity", 'type': 'string'},
                {'name': "OnlineBackup", 'type': 'string'},
                {'name': "DeviceProtection", 'type': 'string'},
                {'name': "TechSupport", 'type': 'string'},
                {'name': "StreamingTV", 'type': 'string'},
                {'name': "StreamingMovies", 'type': 'string'},
                {'name': "Contract", 'type': 'string'},
                {'name': "PaperlessBilling", 'type': 'string'},
                {'name': "PaymentMethod", 'type': 'string'},
                {'name': "MonthlyCharges", 'type': 'double'},
                {'name': "TotalCharges", 'type': 'double'},
                {'name': "Churn", 'type': 'string', 'nullable': True},
                {'name': "SampleWeight", 'type': 'double'},
            ]
        }
        output_data_schema = {'id': '1', 'fields': [{'name': 'Predicted Churn', 'type': 'string'},
                                                    {'name': 'Probability of Churn', 'type': 'double'}]}

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "spss-modeler_18.1",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "spss-modeler_18.1",
                self.wml_client.repository.ModelMetaNames.INPUT_DATA_SCHEMA: input_data_schema,
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema,
            }
        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "John Smith",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "spss-modeler",
                self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "18.0",
                self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "spss-modeler",
                self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "18.0"
            }

        print("Publishing a new model...")
        published_model_details = self.wml_client.repository.store_model(model=model_path,
                                                                         meta_props=model_props)
        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Published model details:\n{}".format(published_model_details))
