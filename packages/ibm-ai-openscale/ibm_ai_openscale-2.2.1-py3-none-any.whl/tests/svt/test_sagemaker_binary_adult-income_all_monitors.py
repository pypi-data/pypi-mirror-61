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
from ibm_ai_openscale.supporting_classes import PayloadRecord


class TestAIOpenScaleClient(unittest.TestCase):

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
    scoring_records = 0
    feedback_records = 0

    test_uid = str(uuid.uuid4())

    def score(self, binding_details, subscription_details):
        access_id = binding_details['entity']['credentials']['access_key_id']
        access_key = binding_details['entity']['credentials']['secret_access_key']
        region = binding_details['entity']['credentials']['region']
        endpoint_name = subscription_details['entity']['deployments'][0]['name']

        runtime = boto3.client('sagemaker-runtime',
                               region_name=region,
                               aws_access_key_id=access_id,
                               aws_secret_access_key=access_key)

        fields = ['Age', 'Capital Gain', 'Hours per week', 'Capital Loss', 'Workclass_ Federal-gov', 'Workclass_ Local-gov', 'Workclass_ Never-worked', 'Workclass_ Private', 'Workclass_ Self-emp-inc', 'Workclass_ Self-emp-not-inc', 'Workclass_ State-gov', 'Workclass_ Without-pay', 'Education_ 10th', 'Education_ 11th', 'Education_ 12th', 'Education_ 1st-4th', 'Education_ 5th-6th', 'Education_ 7th-8th', 'Education_ 9th', 'Education_ Assoc-acdm', 'Education_ Assoc-voc', 'Education_ Bachelors', 'Education_ Doctorate', 'Education_ HS-grad', 'Education_ Masters', 'Education_ Preschool', 'Education_ Prof-school', 'Education_ Some-college', 'Martial Status_ Divorced', 'Martial Status_ Married-AF-spouse', 'Martial Status_ Married-civ-spouse', 'Martial Status_ Married-spouse-absent', 'Martial Status_ Never-married', 'Martial Status_ Separated', 'Martial Status_ Widowed', 'Occupation_ Adm-clerical', 'Occupation_ Armed-Forces', 'Occupation_ Craft-repair', 'Occupation_ Exec-managerial', 'Occupation_ Farming-fishing', 'Occupation_ Handlers-cleaners', 'Occupation_ Machine-op-inspct', 'Occupation_ Other-service', 'Occupation_ Priv-house-serv', 'Occupation_ Prof-specialty', 'Occupation_ Protective-serv', 'Occupation_ Sales', 'Occupation_ Tech-support', 'Occupation_ Transport-moving', 'Relationship_ Husband', 'Relationship_ Not-in-family', 'Relationship_ Other-relative', 'Relationship_ Own-child', 'Relationship_ Unmarried', 'Relationship_ Wife', 'Race_ Amer-Indian-Eskimo', 'Race_ Asian-Pac-Islander', 'Race_ Black', 'Race_ Other', 'Race_ White', 'Sex_ Female', 'Sex_ Male', 'Country_ Cambodia', 'Country_ Canada', 'Country_ China', 'Country_ Columbia', 'Country_ Cuba', 'Country_ Dominican-Republic', 'Country_ Ecuador', 'Country_ El-Salvador', 'Country_ England', 'Country_ France', 'Country_ Germany', 'Country_ Greece', 'Country_ Guatemala', 'Country_ Haiti', 'Country_ Holand-Netherlands', 'Country_ Honduras', 'Country_ Hong', 'Country_ Hungary', 'Country_ India', 'Country_ Iran', 'Country_ Ireland', 'Country_ Italy', 'Country_ Jamaica', 'Country_ Japan', 'Country_ Laos', 'Country_ Mexico', 'Country_ Nicaragua', 'Country_ Outlying-US(Guam-USVI-etc)', 'Country_ Peru', 'Country_ Philippines', 'Country_ Poland', 'Country_ Portugal', 'Country_ Puerto-Rico', 'Country_ Scotland', 'Country_ South', 'Country_ Taiwan', 'Country_ Thailand', 'Country_ Trinadad&Tobago', 'Country_ United-States', 'Country_ Vietnam', 'Country_ Yugoslavia']
        payload = "25,0,30,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0"
        start_time = time.time()
        try:
            response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                               ContentType='text/csv',
                                               Body=payload)

        except Exception:
            print("Unable to score sagemaker!")
        finally:
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



        cls.data_df = pd.read_csv("./datasets/Adult-income/adult_income_train.csv")

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        assert_datamart_details(details, schema=self.schema, state='active')

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
        binding_details = self.ai_client.data_mart.bindings.get_details(self.binding_uid)
        print("Binding details: {}".format(binding_details))

    def test_04_list_bindings(self):
        self.ai_client.data_mart.bindings.list()

    def test_05_get_assets(self):
        asset_details = self.ai_client.data_mart.bindings.get_asset_details(binding_uid=self.binding_uid)

        asset_name = ""
        for detail in asset_details:
            if 'linear-learner-2019-05-30-05-44' in detail['name']:
                asset_name = detail['name']
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        print("asset name: {}".format(asset_name))
        print("asset uid: {}".format(self.source_uid))
        self.assertIsNotNone(self.source_uid)

    def test_06_subscribe_sagemaker_asset(self):
        from ibm_ai_openscale.supporting_classes.enums import ProblemType, InputDataType

        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            SageMakerMachineLearningAsset(
                source_uid=self.source_uid,
                binding_uid=self.binding_uid,
                input_data_type=InputDataType.STRUCTURED,
                problem_type=ProblemType.BINARY_CLASSIFICATION,
                prediction_column='predicted_label',
                probability_column='score',
                label_column='Income',
                feature_columns=[
                    'Age', 'Capital Gain', 'Hours per week', 'Capital Loss', 'Workclass_ Federal-gov', 'Workclass_ Local-gov', 'Workclass_ Never-worked', 'Workclass_ Private', 'Workclass_ Self-emp-inc', 'Workclass_ Self-emp-not-inc', 'Workclass_ State-gov', 'Workclass_ Without-pay', 'Education_ 10th', 'Education_ 11th', 'Education_ 12th', 'Education_ 1st-4th', 'Education_ 5th-6th', 'Education_ 7th-8th', 'Education_ 9th', 'Education_ Assoc-acdm', 'Education_ Assoc-voc', 'Education_ Bachelors', 'Education_ Doctorate', 'Education_ HS-grad', 'Education_ Masters', 'Education_ Preschool', 'Education_ Prof-school', 'Education_ Some-college', 'Martial Status_ Divorced', 'Martial Status_ Married-AF-spouse', 'Martial Status_ Married-civ-spouse', 'Martial Status_ Married-spouse-absent', 'Martial Status_ Never-married', 'Martial Status_ Separated', 'Martial Status_ Widowed', 'Occupation_ Adm-clerical', 'Occupation_ Armed-Forces', 'Occupation_ Craft-repair', 'Occupation_ Exec-managerial', 'Occupation_ Farming-fishing', 'Occupation_ Handlers-cleaners', 'Occupation_ Machine-op-inspct', 'Occupation_ Other-service', 'Occupation_ Priv-house-serv', 'Occupation_ Prof-specialty', 'Occupation_ Protective-serv', 'Occupation_ Sales', 'Occupation_ Tech-support', 'Occupation_ Transport-moving', 'Relationship_ Husband', 'Relationship_ Not-in-family', 'Relationship_ Other-relative', 'Relationship_ Own-child', 'Relationship_ Unmarried', 'Relationship_ Wife', 'Race_ Amer-Indian-Eskimo', 'Race_ Asian-Pac-Islander', 'Race_ Black', 'Race_ Other', 'Race_ White', 'Sex_ Female', 'Sex_ Male', 'Country_ Cambodia', 'Country_ Canada', 'Country_ China', 'Country_ Columbia', 'Country_ Cuba', 'Country_ Dominican-Republic', 'Country_ Ecuador', 'Country_ El-Salvador', 'Country_ England', 'Country_ France', 'Country_ Germany', 'Country_ Greece', 'Country_ Guatemala', 'Country_ Haiti', 'Country_ Holand-Netherlands', 'Country_ Honduras', 'Country_ Hong', 'Country_ Hungary', 'Country_ India', 'Country_ Iran', 'Country_ Ireland', 'Country_ Italy', 'Country_ Jamaica', 'Country_ Japan', 'Country_ Laos', 'Country_ Mexico', 'Country_ Nicaragua', 'Country_ Outlying-US(Guam-USVI-etc)', 'Country_ Peru', 'Country_ Philippines', 'Country_ Poland', 'Country_ Portugal', 'Country_ Puerto-Rico', 'Country_ Scotland', 'Country_ South', 'Country_ Taiwan', 'Country_ Thailand', 'Country_ Trinadad&Tobago', 'Country_ United-States', 'Country_ Vietnam', 'Country_ Yugoslavia'
                ],
                categorical_columns=[],
            ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription uid: {}".format(TestAIOpenScaleClient.subscription_uid))

    def test_07_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        details = TestAIOpenScaleClient.subscription.get_details()

        assert_subscription_details(subscription_details=details, no_deployments=1, text_included="s3", enabled_monitors=['payload_logging', 'performance_monitoring'])

    def test_08_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()
        deployment_uids = TestAIOpenScaleClient.subscription.get_deployment_uids()
        self.assertGreater(len(deployment_uids), 0)

    def test_09_score_model_and_log_payload(self):
        binding_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)
        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        request, response, response_time = self.score(binding_details=binding_details, subscription_details=subscription_details)

        TestAIOpenScaleClient.scoring_records = 15
        records_list = []
        for i in range(0, self.scoring_records):
            records_list.append(PayloadRecord(request=request, response=response, response_time=int(response_time)))

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_10_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['score', 'predicted_label'])

    def test_11_stats_on_performance_monitoring_table(self):
        self.subscription.performance_monitoring.print_table_schema()
        self.subscription.performance_monitoring.show_table()
        self.subscription.performance_monitoring.describe_table()

        performance_table_pandas = self.subscription.performance_monitoring.get_table_content()
        assert_performance_monitoring_pandas_table_content(pandas_table_content=performance_table_pandas)

        performance_table_python = self.subscription.performance_monitoring.get_table_content(format='python')
        assert_performance_monitoring_python_table_content(python_table_content=performance_table_python)

    def test_12_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_13_get_quality_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_14_send_feedback_data(self):

        feedback_records = []

        fields = ['Age', 'Capital Gain', 'Hours per week', 'Capital Loss', 'Workclass_ Federal-gov', 'Workclass_ Local-gov', 'Workclass_ Never-worked', 'Workclass_ Private', 'Workclass_ Self-emp-inc', 'Workclass_ Self-emp-not-inc', 'Workclass_ State-gov', 'Workclass_ Without-pay', 'Education_ 10th', 'Education_ 11th', 'Education_ 12th', 'Education_ 1st-4th', 'Education_ 5th-6th', 'Education_ 7th-8th', 'Education_ 9th', 'Education_ Assoc-acdm', 'Education_ Assoc-voc', 'Education_ Bachelors', 'Education_ Doctorate', 'Education_ HS-grad', 'Education_ Masters', 'Education_ Preschool', 'Education_ Prof-school', 'Education_ Some-college', 'Martial Status_ Divorced', 'Martial Status_ Married-AF-spouse', 'Martial Status_ Married-civ-spouse', 'Martial Status_ Married-spouse-absent', 'Martial Status_ Never-married', 'Martial Status_ Separated', 'Martial Status_ Widowed', 'Occupation_ Adm-clerical', 'Occupation_ Armed-Forces', 'Occupation_ Craft-repair', 'Occupation_ Exec-managerial', 'Occupation_ Farming-fishing', 'Occupation_ Handlers-cleaners', 'Occupation_ Machine-op-inspct', 'Occupation_ Other-service', 'Occupation_ Priv-house-serv', 'Occupation_ Prof-specialty', 'Occupation_ Protective-serv', 'Occupation_ Sales', 'Occupation_ Tech-support', 'Occupation_ Transport-moving', 'Relationship_ Husband', 'Relationship_ Not-in-family', 'Relationship_ Other-relative', 'Relationship_ Own-child', 'Relationship_ Unmarried', 'Relationship_ Wife', 'Race_ Amer-Indian-Eskimo', 'Race_ Asian-Pac-Islander', 'Race_ Black', 'Race_ Other', 'Race_ White', 'Sex_ Female', 'Sex_ Male', 'Country_ Cambodia', 'Country_ Canada', 'Country_ China', 'Country_ Columbia', 'Country_ Cuba', 'Country_ Dominican-Republic', 'Country_ Ecuador', 'Country_ El-Salvador', 'Country_ England', 'Country_ France', 'Country_ Germany', 'Country_ Greece', 'Country_ Guatemala', 'Country_ Haiti', 'Country_ Holand-Netherlands', 'Country_ Honduras', 'Country_ Hong', 'Country_ Hungary', 'Country_ India', 'Country_ Iran', 'Country_ Ireland', 'Country_ Italy', 'Country_ Jamaica', 'Country_ Japan', 'Country_ Laos', 'Country_ Mexico', 'Country_ Nicaragua', 'Country_ Outlying-US(Guam-USVI-etc)', 'Country_ Peru', 'Country_ Philippines', 'Country_ Poland', 'Country_ Portugal', 'Country_ Puerto-Rico', 'Country_ Scotland', 'Country_ South', 'Country_ Taiwan', 'Country_ Thailand', 'Country_ Trinadad&Tobago', 'Country_ United-States', 'Country_ Vietnam', 'Country_ Yugoslavia', 'Income']

        TestAIOpenScaleClient.feedback_records = 15
        for i in range(0, self.feedback_records):
            feedback_records.append(
                [45,0,35,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0])

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_records, fields=fields)
        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_15_stats_on_feedback_logging_table(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_16_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=TestAIOpenScaleClient.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(run_uid=run_details['id'])

    def test_17_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    def test_17b_get_quality_metrics(self):
        print("Quality metrics test: ")
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_binary_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)
    #
    # def test_18_get_transaction_id(self):
    #     python_table_content = self.subscription.payload_logging.get_table_content(format='python')
    #     no_payloads = len(python_table_content['values'])
    #
    #     # select random record from payload table
    #     import random
    #     random_record = random.randint(0, no_payloads-1)
    #     TestAIOpenScaleClient.transaction_id = python_table_content['values'][random_record][0]
    #
    #     print("Selected transaction id: {}".format(self.transaction_id))
    #
    # def test_19_setup_explainability(self):
    #     TestAIOpenScaleClient.subscription.explainability.enable(
    #         training_data=self.data_df
    #     )
    #
    # def test_20_get_explainability_details(self):
    #     details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=details)
    #
    # def test_21_run_explainability(self):
    #     explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id=self.transaction_id,
    #         background_mode=False
    #     )
    #     print("status ", explainability_run['entity']['status'])
    #
    #     assert_explainability_run(explainability_run_details=explainability_run)
    #
    # def test_21b_list_explanations(self):
    #     TestAIOpenScaleClient.subscription.explainability.list_explanations()
    #
    # def test_22_stats_on_explainability_table(self):
    #     TestAIOpenScaleClient.subscription.explainability.print_table_schema()
    #     TestAIOpenScaleClient.subscription.explainability.show_table()
    #     TestAIOpenScaleClient.subscription.explainability.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.explainability.get_table_content()
    #     assert_explainability_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.explainability.get_table_content(format='python')
    #     assert_explainability_python_table_content(python_table_content=python_table_content)
    #
    # def test_23_setup_fairness_monitoring(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         training_data=self.data_df,
    #         features=[
    #             Feature("Age", majority=[[26, 74]], minority=[[19, 25]], threshold=0.8),
    #             Feature("Sex_ Male", majority=[[1,1]], minority=[[0,0]], threshold=0.8)
    #         ],
    #         deployment_uid=None,
    #         favourable_classes=[1],
    #         unfavourable_classes=[0],
    #         min_records=5
    #     )
    #
    # def test_24_get_fairness_monitoring_details(self):
    #     details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
    #     assert_fairness_configuration(fairness_monitoring_details=details)
    #
    # def test_25_run_fairness(self):
    #     fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
    #     assert_fairness_run(fairness_run_details=fairness_run)
    #
    # def test_26_stats_on_fairness_table(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
    #     assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)

    def test_27_disable_all_monitors(self):
        self.subscription.quality_monitoring.disable()
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        # self.subscription.fairness_monitoring.disable()
        # self.subscription.explainability.disable()

        assert_monitors_enablement(subscription_details=self.subscription.get_details())

    def test_28_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
