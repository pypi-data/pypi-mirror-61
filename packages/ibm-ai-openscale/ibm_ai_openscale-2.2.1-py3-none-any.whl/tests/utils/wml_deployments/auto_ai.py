from . import WMLDeployment
import os
import json


class AutoAIDeployment(WMLDeployment):
    model_path = None
    input_schema = None

    def __init__(self, name, asset_name):
        super(AutoAIDeployment, self).__init__(
            name=name,
            asset_name=asset_name
        )

    def publish_model(self):
        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "wml-hybrid_0.1",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "hybrid_0.1",
                self.wml_client.repository.ModelMetaNames.INPUT_DATA_SCHEMA: self.input_schema
            }
            print("Publishing a new model...")
            published_model_details = self.wml_client.repository.store_model(model=self.model_path,
                                                                             meta_props=model_props)
            self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

            print("Published model details:\n{}".format(published_model_details))
        else:
            raise NotImplemented()


class CarPrice(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_Car_Price_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_Car_Price_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(CarPrice, self).__init__(
            name="AutoAI Car Price deployment WMLv4",
            asset_name="AutoAI Car Price model WMLv4"
        )


class Iris(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_Iris_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_Iris_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(Iris, self).__init__(
            name="AutoAI Iris deployment WMLv4",
            asset_name="AutoAI Iris model WMLv4"
        )


class CustomerChurn(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_Customer_Churn_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_Customer_Churn_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(CustomerChurn, self).__init__(
            name="AutoAI Customer Churn deployment WMLv4",
            asset_name="AutoAI Customer Churn model WMLv4"
        )


class BankMarketing(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_bank_marketing_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_bank_marketing_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(BankMarketing, self).__init__(
            name="AutoAI bank marketing deployment WMLv4",
            asset_name="AutoAI bank marketing model WMLv4"
        )


class WinePrediction(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_wine_prediction_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_wine_prediction_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(WinePrediction, self).__init__(
            name="AutoAI wine prediction deployment WMLv4",
            asset_name="AutoAI wine prediction model WMLv4"
        )


class VideoGame(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_video_game_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_video_game_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(VideoGame, self).__init__(
            name="AutoAI video game deployment WMLv4",
            asset_name="AutoAI video game model WMLv4"
        )


class CreditRisk(AutoAIDeployment):
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_credit_risk_model_WMLv4.tar.gz')
        schema_path = os.path.join(os.getcwd(), 'artifacts', 'AutoAI', 'AutoAI_credit_risk_model_WMLv4.json')
        with open(schema_path) as json_schema:
            self.input_schema = json.load(json_schema)
        super(CreditRisk, self).__init__(
            name="AutoAI credit risk deployment WMLv4",
            asset_name="AutoAI credit risk model WMLv4"
        )

