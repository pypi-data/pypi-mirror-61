# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import boto3
import pandas as pd

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.utils import check_if_binding_exists

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature, InputDataType


class TestAIOpenScaleClient(unittest.TestCase):
    scoring_records = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    wml_client = None
    subscription = None
    binding_uid = None

    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None
    transaction_id = None
    final_run_details = None

    test_uid = str(uuid.uuid4())

    data_df = pd.read_csv("datasets/balance-scale/balance-scale.csv")

    def score(self, binding_details, subscription_details):
        access_id = binding_details['entity']['credentials']['access_key_id']
        access_key = binding_details['entity']['credentials']['secret_access_key']
        region = binding_details['entity']['credentials']['region']
        endpoint_name = subscription_details['entity']['deployments'][0]['name']

        runtime = boto3.client('sagemaker-runtime',
                               region_name=region,
                               aws_access_key_id=access_id,
                               aws_secret_access_key=access_key)

        fields = ['L-Weight', 'L-Distance', 'R-Weight', 'R-Distance']
        payload = "1, 3, 1, 3"

        start_time = time.time()
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           ContentType='text/csv',
                                           Body=payload)
        response_time = time.time() - start_time
        result = json.loads(response['Body'].read().decode())

        values = []
        for v in payload.split('\n'):
            values.append([float(s) for s in v.split(',')])

        request = {'fields': fields, 'values': values}
        response = {
            'fields': list(result['predictions'][0]),
            'values': [list(x.values()) for x in result['predictions']]
        }

        return request, response, response_time

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.credentials = get_aws_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_sagemaker(self):
        TestAIOpenScaleClient.binding_uid = check_if_binding_exists(
            self.ai_client,
            self.credentials,
            type='amazon_sagemaker')

        if TestAIOpenScaleClient.binding_uid is None:
            print("Binding does not exist. Creating a new one.")
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add(
                "SageMaker ml engine",
                SageMakerMachineLearningInstance(self.credentials))

        print("Binding uid: {}".format(self.binding_uid))

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_04_get_assets(self):
        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details(binding_uid=self.binding_uid)
        print("Assets details: {}".format(asset_details))

        asset_name = ""
        for detail in asset_details:
            if 'linear-learner-2019-06-03-05-14-56' in detail['name']:
                asset_name = detail['name']
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        print("asset name: {}".format(asset_name))
        print("asset uid: {}".format(TestAIOpenScaleClient.source_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_05_get_asset_deployments(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_asset_deployments()

    def test_06_subscribe_sagemaker_asset(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            SageMakerMachineLearningAsset(
                source_uid=TestAIOpenScaleClient.source_uid,
                binding_uid=TestAIOpenScaleClient.binding_uid,
                input_data_type=InputDataType.STRUCTURED,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                prediction_column='predicted_label',
                probability_column='score',
                label_column='Class',
                feature_columns=['L-Weight', 'L-Distance', 'R-Weight', 'R-Distance'],
                categorical_columns=[],
            ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription uid: ".format(TestAIOpenScaleClient.subscription_uid))

    def test_07_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        details = TestAIOpenScaleClient.subscription.get_details()
        print('Subscription details: ' + str(details))

        self.assertTrue('s3' in str(details))

    def test_08_list_deployments(self):
        print("Listing deployments:\n")
        self.subscription.list_deployments()

    def test_09_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_initial_subscription_configuration(subscription_details=subscription_details)

    def test_10_score_model_and_log_payload(self):
        binding_details = self.ai_client.data_mart.bindings.get_details(self.binding_uid)
        subscription_details = self.subscription.get_details()

        TestAIOpenScaleClient.scoring_records = 40

        request, response, response_time = self.score(binding_details=binding_details, subscription_details=subscription_details)
        records_list = []

        for i in range(0, int(self.scoring_records)):
            records_list.append(PayloadRecord(request=request, response=response, response_time=int(response_time)))

        self.subscription.payload_logging.store(records=records_list)
        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_11_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['predicted_label', 'prediction_probability'])

    def test_12_stats_on_performance_monitoring_table(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertGreater(len(performance_metrics['values']), 0)

    def test_13_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_14_get_quality_monitoring_details(self):
        print("Quality monitoring details:\n{}".format(TestAIOpenScaleClient.subscription.quality_monitoring.get_details()))

    # def test_15_setup_explainability(self):
    #     TestAIOpenScaleClient.subscription.explainability.enable(
    #         training_data=self.data_df
    #     )
    #
    # def test_16_get_explainability_details(self):
    #     explain_details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=explain_details)
    #
    # def test_17_setup_fairness(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         features=[
    #             Feature("L-Weight", majority=[[4, 5]], minority=[[0, 3]], threshold=0.8)
    #         ],
    #         favourable_classes=["R"],
    #         unfavourable_classes=["L", "B"],
    #         min_records=10,
    #         training_data=self.data_df
    #     )
    #
    # def test_18_get_fairness_monitoring_details(self):
    #     print("Fairness details:\n{}".format(TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()))
    #
    # def test_19_validate_subscription_configuration_with_all_monitors(self):
    #     subscription_details = TestAIOpenScaleClient.subscription.get_details()
    #     assert_monitors_enablement(subscription_details=subscription_details, quality=True, payload=True, performance=True, fairness=True, explainability=True)

    def test_20_send_feedback_data(self):
        feedback_records = []

        fields = ['L-Weight', 'L-Distance', 'R-Weight', 'R-Distance', 'Class']

        for i in range(1, 20):
            feedback_records.append(
                [1,3,1,4, 2.0])
            feedback_records.append(
                [1,3,1,4, 2.0])

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_records, fields=fields)

        wait_for_feedback_table(subscription=self.subscription, feedback_records=feedback_records)

    def test_21_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=TestAIOpenScaleClient.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_22_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_22b_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))

        print("\nQuality metrics test: ")
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_23_stats_on_feedback_logging_table(self):
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()
        TestAIOpenScaleClient.subscription.feedback_logging.get_table_content()
        feedback_logging = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='python')
        self.assertTrue(len(feedback_logging['values']) > 0)

    # def test_24_run_fairness(self):
    #     fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
    #     print('fairness_run', fairness_run)
    #
    #     assert_fairness_run(fairness_run_details=fairness_run)
    #
    # def test_25_stats_on_fairness_monitoring_table(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
    #     assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)

    def test_26_disable_all_monitors(self):
        self.subscription.quality_monitoring.disable()
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        # self.subscription.explainability.disable()
        # self.subscription.fairness_monitoring.disable()


        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        for configuration in subscription_details['entity']['configurations']:
            self.assertFalse(configuration['enabled'])

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
