from . import WMLDeployment
import os


class MultiplyFunction(WMLDeployment):
    def __init__(self):
        super(MultiplyFunction, self).__init__(
            name="AIOS Multiply Function V4",
            asset_name="AIOS Multiply Function Deployment V4"
        )

    def get_asset_details(self, asset_id):
        return self.wml_client.repository.get_function_details(asset_id)

    def publish_model(self):
        if self.wml_v4:
            def score(payload):
                values = [[row[0] * row[1]] for input_data in payload['input_data'] for row in input_data['values']]
                return {'predictions': [{'fields': ['multiplication'], 'values': values}]}

            print("Publishing new model using V4 client.")
            function_props = {
                self.wml_client.repository.FunctionMetaNames.NAME: self.asset_name,
                self.wml_client.repository.FunctionMetaNames.TYPE: "python",
                self.wml_client.repository.FunctionMetaNames.RUNTIME_UID: "ai-function_0.1-py3.6",
            }
        else:
            def score(payload):
                values = [[row[0] * row[1]] for row in payload['values']]
                return {'fields': ['multiplication'], 'values': values}

            print("Publishing new model using V3 client.")
            function_props = self.name

        print("Publishing a new function...")
        published_function_details = self.wml_client.repository.store_function(function=score,
                                                                               meta_props=function_props)

        print("Published model details:\n{}".format(published_function_details))
        self.asset_uid = self.wml_client.repository.get_function_uid(published_function_details)
