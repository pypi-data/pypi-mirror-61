# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pandas as pd
from requests.auth import HTTPBasicAuth

from utils.assertions import *
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import SPSSMachineLearningInstance, SPSSMachineLearningAsset
from ibm_ai_openscale.supporting_classes import ProblemType, InputDataType, PayloadRecord
from preparation_and_cleaning import *


@unittest.skipIf("ICP" not in get_env(), "Please run this test only on ICP env")
class TestAIOpenScaleClient(unittest.TestCase):

    ai_client = None
    deployment_uid = None
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
    request = None
    response = None
    training_data_statistics = None
    scoring_records = 12
    feedback_records = 18
    final_run_details = None

    test_uid = str(uuid.uuid4())
    data_df = pd.read_csv("datasets/customer-visits/customer_train.csv")

    model_uid = 'customer_visits'
    credentials = get_spss_cnds_credentials()

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)



    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        print(details)
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_03_bind_spss_cds_instance(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("SPSS C&DS instance on ICP",
                                                                                  SPSSMachineLearningInstance(self.credentials))

    def test_04_get_binding_details(self):
        print('Binding details: :' + str(TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)))
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_05_get_assets(self):
        assets_uids = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()
        self.assertGreater(len(assets_uids), 1)
        print('Assets uids: ' + str(assets_uids))

        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()
        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details()
        print('Assets details: ' + str(asset_details))

        for detail in asset_details:
            if self.model_uid == detail['name']:
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        self.assertIsNotNone(TestAIOpenScaleClient.source_uid, msg="Asset with model uid: {} not found".format(self.model_uid))

    def test_06_subscribe_spss_asset(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            SPSSMachineLearningAsset(source_uid=TestAIOpenScaleClient.source_uid,
                                     binding_uid=TestAIOpenScaleClient.binding_uid,
                                     input_data_type=InputDataType.STRUCTURED,
                                     problem_type=ProblemType.BINARY_CLASSIFICATION,
                                     label_column="product_id",
                                     feature_columns=['customer_id', 'campaign', 'age', 'age_youngest_child',
                                                'branch', 'debt_equity', 'gender', 'bad_payment', 'gold_card',
                                                'pension_plan', 'household_debt_to_equity_ratio', 'income', 'marital',
                                                'members_in_household', 'months_current_account', 'months_customer',
                                                'call_center_contacts', 'loan_accounts', 'number_products',
                                                'number_transactions', 'non_worker_percentage', 'white_collar_percentage',
                                                'rfm_score'],
                                     categorical_columns=['campaign', 'age', 'branch', 'gender', 'marital'],
                                     prediction_column="$C-product_id",
                                     class_probability_columns=['$CC-product_id']
                                     ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid

        print('Subscription details: ' + str(subscription.get_details()))

    def test_07_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        print('Subscription details: ' + str(TestAIOpenScaleClient.subscription.get_details()))

    def test_08_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_09_score_and_log_payload(self):
        binding_details = self.ai_client.data_mart.bindings.get_details(self.binding_uid)
        binding_credentials = binding_details['entity']['credentials']
        self.assertEqual(self.credentials['username'], binding_credentials['username'])
        self.assertEqual(self.credentials['password'], binding_credentials['password'])
        self.assertEqual(self.credentials['url'], binding_credentials['url'])

        subscription_details = self.subscription.get_details()
        scoring_endpoint = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']
        input_table_id = subscription_details['entity']['asset_properties']['input_data_schema']['id']

        scoring_payload = {
            'id': self.model_uid,
            'requestInputTable': [
                {"id": input_table_id,
                 'requestInputRow': [
                     {'input': [
                         {'name': 'customer_id', 'value': '7.000'},
                         {'name': 'campaign', 'value': '2.000'},
                         {'name': 'age', 'value': '19.000'},
                         {'name': 'age_youngest_child', 'value': '5.000'},
                         {'name': 'branch', 'value': 'Catburg'},

                         {'name': 'debt_equity', 'value': '45.000'},
                         {'name': 'gender', 'value': 'F'},
                         {'name': 'bad_payment', 'value': '0.000'},
                         {'name': 'gold_card', 'value': '0.000'},
                         {'name': 'pension_plan', 'value': '0.000'},

                         {'name': 'household_debt_to_equity_ratio', 'value': '65.000'},
                         {'name': 'income', 'value': '13362.000'},
                         {'name': 'marital', 'value': 'U'},
                         {'name': 'members_in_household', 'value': '2.000'},
                         {'name': 'months_current_account', 'value': '33.000'},
                         {'name': 'months_customer', 'value': '36'},

                         {'name': 'call_center_contacts', 'value': '1.000'},
                         {'name': 'loan_accounts', 'value': '4.000'},
                         {'name': 'number_products', 'value': '2.000'},
                         {'name': 'number_transactions', 'value': '1.000'},
                         {'name': 'non_worker_percentage', 'value': '7.000'},

                         {'name': 'white_collar_percentage', 'value': '24.000'},
                         {'name': 'rfm_score', 'value': '0.000'}
                        ]
                     }
                 ]
                 }
            ]
        }

        start_time = time.time()
        resp_score = requests.post(url=scoring_endpoint, json=scoring_payload, auth=HTTPBasicAuth(username=binding_credentials['username'], password=binding_credentials['password']))

        print("Response scoring: {}".format(resp_score.text))
        response_time = time.time() - start_time
        result = resp_score.json()

        print('Scoring result:', result)

        TestAIOpenScaleClient.request = scoring_payload
        TestAIOpenScaleClient.response = result

        records_list = []

        for i in range(0, self.scoring_records):
            records_list.append(PayloadRecord(request=TestAIOpenScaleClient.request, response=TestAIOpenScaleClient.response, response_time=int(response_time)))

        self.subscription.payload_logging.store(records=records_list)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_10_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['$C-product_id', '$CC-product_id'])

    def test_11_setup_quality_monitoring(self):
        print('Subscription details: ' + str(TestAIOpenScaleClient.subscription.get_details()))

        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_12_get_quality_monitoring_details(self):
        print(str(TestAIOpenScaleClient.subscription.quality_monitoring.get_details()))
        TestAIOpenScaleClient.subscription.quality_monitoring.get_details()

    def test_13_send_feedback_data(self):
        from ibm_ai_openscale.supporting_classes.enums import FeedbackFormat

        with open(file='datasets/customer-visits/customer_train_feedback.csv') as file:
            feedback_data = file.read()
        self.assertIsNotNone(feedback_data, msg="Unable to load feedback data from file.")

        TestAIOpenScaleClient.feedback_records = 30
        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_data, feedback_format=FeedbackFormat.CSV, data_header=True, data_delimiter=';')

    def test_14_stats_on_feedback_logging_table(self):
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()
        TestAIOpenScaleClient.subscription.feedback_logging.get_table_content()
        feedback_logging = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='python')
        self.assertTrue(len(feedback_logging['values']) > 0)

    def test_15_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_16_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_18_get_quality_metrics(self):
        deployment_uid = TestAIOpenScaleClient.subscription.get_deployment_uids()[0]

        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='quality'))
        print(TestAIOpenScaleClient.subscription.quality_monitoring.get_metrics(deployment_uid=deployment_uid))

        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='quality')['deployment_metrics'][0]['metrics']) > 0)

        print("\nQuality metrics test: ")
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_binary_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_19_stats_on_performance_metrics(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_20_get_performance_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance'))
        print(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestAIOpenScaleClient.subscription.get_deployment_uids()[0]))

        self.assertTrue(
            len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance')['deployment_metrics'][
                                0]['metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestAIOpenScaleClient.subscription.get_deployment_uids()[0])['metrics']) > 0)

    def test_21_setup_explainability(self):
        TestAIOpenScaleClient.subscription.explainability.enable(
            training_data=TestAIOpenScaleClient.data_df
        )

    def test_22_get_details(self):
        details = TestAIOpenScaleClient.subscription.explainability.get_details()
        assert_explainability_configuration(explainability_details=details)

    def test_23_get_transaction_id(self):
        pandas_pd = self.subscription.payload_logging.get_table_content()
        no_payloads = len(pandas_pd['scoring_id'].values)

        # select random record from payload table
        import random
        random_record = random.randint(0, no_payloads - 1)
        TestAIOpenScaleClient.transaction_id = pandas_pd['scoring_id'].values[random_record]

    def test_24_run_explainability(self):
        explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
            transaction_id=self.transaction_id,
            background_mode=False
        )
        assert_explainability_run(explainability_run_details=explainability_run)

    def test_24b_list_explanations(self):
        TestAIOpenScaleClient.subscription.explainability.list_explanations()

    def test_25_stats_on_explainability_table(self):
        TestAIOpenScaleClient.subscription.explainability.print_table_schema()
        TestAIOpenScaleClient.subscription.explainability.show_table()
        TestAIOpenScaleClient.subscription.explainability.describe_table()

        pandas_df = TestAIOpenScaleClient.subscription.explainability.get_table_content()
        assert_explainability_pandas_table_content(pandas_table_content=pandas_df)

        python_table_content = TestAIOpenScaleClient.subscription.explainability.get_table_content(format='python')
        assert_explainability_python_table_content(python_table_content=python_table_content)

    def test_26_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_27_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )

if __name__ == '__main__':
    unittest.main()
