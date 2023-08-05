# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


import pandas as pd

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.utils import *

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    binding_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())
    source_uid = None
    transaction_id = None
    scoring_records = None
    feedback_records = None
    final_run_details = None
    credentials = None

    start_date = datetime.utcnow().isoformat() + "Z"
    data_df = pd.read_csv(
        "datasets/campaign-effects/campain_effectivenes_train.csv", sep=",")


    def score(self, subscription_details):
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

        if 'credentials' not in subscription_details['entity']['deployments'][0]['scoring_endpoint'].keys():
            print("---> Impacted subscription details:")
            print(subscription_details['entity']['deployments'][0]['scoring_endpoint'])
            print(subscription_details['entity']['deployments'][0])
            print(subscription_details['entity']['deployments'])
            print(subscription_details['entity'])

        data = {"input": [{'campaign': 2.0,
                           'age': 19.0,
                           'age_youngest_child': 0.0,
                           'branch': 'Ravensville',
                           'debt_equity': 19.0,
                           'gender': 'M',
                           'bad_payment': 0.0,
                           'gold_card': 0.0,
                           'pension_plan': 0.0,
                           'household_debt_to_equity_ratio': 64.0,
                           'income': 13362.0,
                           'marital': 'S',
                           'members_in_household': 2.0,
                           'months_current_account': -4.0,
                           'months_customer': 0.0,
                           'call_center_contacts': 1.0,
                           'loan_accounts': 1.0,
                           'number_products': 1.0,
                           'number_transactions': 0.0,
                           'non_worker_percentage': 9.0,
                           'white_collar_percentage': 26.0,
                           'rfm_score': 0.0},
                          {'campaign': 2.0,
                           'age': 44.0,
                           'age_youngest_child': 12.0,
                           'branch': 'Catburg',
                           'debt_equity': 44.0,
                           'gender': 'M',
                           'bad_payment': 0.0,
                           'gold_card': 0.0,
                           'pension_plan': 0.0,
                           'household_debt_to_equity_ratio': 65.0,
                           'income': 13453.0,
                           'marital': 'S',
                           'members_in_household': 2.0,
                           'months_current_account': 17.0,
                           'months_customer': 24.0,
                           'call_center_contacts': 0.0,
                           'loan_accounts': 0.0,
                           'number_products': 0.0,
                           'number_transactions': 0.0,
                           'non_worker_percentage': 14.0,
                           'white_collar_percentage': 19.0,
                           'rfm_score': 0.0}]}

        body = str.encode(json.dumps(data))
        headers = subscription_details['entity']['deployments'][0]['scoring_endpoint']['request_headers']
        token = subscription_details['entity']['deployments'][0]['scoring_endpoint']['credentials']['token']
        headers['Authorization'] = 'Bearer ' + token

        start_time = time.time()
        response = requests.post(url=scoring_url, data=body, headers=headers)
        response_time = time.time() - start_time
        result = response.json()
        print('--> Azure Service\nScoring payload: {}\nScoring result: {}\nResponse time: {}'.format(data, result,
                                                                                                     response_time))

        return data, result, response_time

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.credentials = get_azure_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        print(details)

    def test_02_bind_azure(self):
        TestAIOpenScaleClient.binding_uid = check_if_binding_exists(
            self.ai_client,
            self.credentials,
            type='azure_machine_learning_service')

        if TestAIOpenScaleClient.binding_uid is None:
            print("Binding does not exist. Creating a new one.")
            TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add(
                "Azure ml service engine", AzureMachineLearningServiceInstance(self.credentials))

        print("Binding uid: {}".format(self.binding_uid))

    def test_03_get_binding_details(self):
        print('Binding details: {}'.format(
            TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)))
        self.ai_client.data_mart.bindings.list()

    def test_04_get_assets(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details(
            binding_uid=TestAIOpenScaleClient.binding_uid)
        assets_uids = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()
        self.assertGreater(len(assets_uids), 1)
        print('Assets uids: ' + str(assets_uids))

        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()
        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details(
            binding_uid=TestAIOpenScaleClient.binding_uid)
        print('Assets details: ' + str(asset_details))

        for detail in asset_details:
            if 'campaign-effectiveness' == detail['name']:
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        print("Source uid: {}".format(self.source_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_05_subscribe_azure_asset(self):
        feature_columns = ['campaign', 'age', 'age_youngest_child', 'branch', 'debt_equity', 'gender', 'bad_payment',
                           'gold_card', 'pension_plan', 'household_debt_to_equity_ratio', 'income', 'marital',
                           'members_in_household', 'months_current_account', 'months_customer', 'call_center_contacts',
                           'loan_accounts', 'number_products', 'number_transactions', 'non_worker_percentage',
                           'white_collar_percentage', 'rfm_score']

        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            AzureMachineLearningServiceAsset(
                source_uid=TestAIOpenScaleClient.source_uid,
                binding_uid=TestAIOpenScaleClient.binding_uid,
                input_data_type=InputDataType.STRUCTURED,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                probability_column='Scored Probabilities',
                label_column='product_code',
                prediction_column='Scored Labels',
                feature_columns=feature_columns,
                categorical_columns=[]
            )
        )

        TestAIOpenScaleClient.subscription_uid = subscription.uid

    def test_06_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(
            TestAIOpenScaleClient.subscription_uid)
        details = self.subscription.get_details()

        assert_subscription_details(subscription_details=details, no_deployments=1, text_included='azureml',
                                    enabled_monitors=['payload_logging', 'performance_monitoring'])

    def test_07_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_check_default_monitors_enablement(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_09_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details,
                                             dynamic_schema_update=False)

    def test_10_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_11_score_model_and_log_payload(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        request, response, response_time = self.score(subscription_details)
        records_list = []

        import random
        TestAIOpenScaleClient.scoring_records = 10
        for i in range(0, TestAIOpenScaleClient.scoring_records):
            records_list.append(PayloadRecord(request=request, response=response, response_time=random.randint(0, 10)))

        print('Number of requests: ', len(records_list), 'Number of rec in request: ', len(request['input']))
        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

    def test_12_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content,
                                                    scoring_records=self.scoring_records * 2)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')

        assert_payload_logging_python_table_content(python_table_content=python_table_content,
                                                    fields=['Scored Probabilities', 'Scored Labels'])
        print('subscription details', TestAIOpenScaleClient.subscription.get_details())

    def test_13_payload_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        data_distribution_run = TestAIOpenScaleClient.subscription.payload_logging.data_distribution.run(
            start_date=self.start_date,
            end_date=end_date,
            group=['Scored Labels', 'marital', 'income'],
            background_mode=False)

        run_id = data_distribution_run['id']
        data_distribution = self.subscription.payload_logging.data_distribution.get_run_result(run_id=run_id)
        print('Payload data distribution')
        print(data_distribution)

        self.assertTrue("20" in str(data_distribution))

    def test_14_stats_on_performance_monitoring_table(self):
        self.subscription.performance_monitoring.print_table_schema()
        self.subscription.performance_monitoring.show_table()
        self.subscription.performance_monitoring.describe_table()

        performance_table_pandas = self.subscription.performance_monitoring.get_table_content()
        assert_performance_monitoring_pandas_table_content(pandas_table_content=performance_table_pandas)

        performance_table_python = self.subscription.performance_monitoring.get_table_content(format='python')
        assert_performance_monitoring_python_table_content(python_table_content=performance_table_python)

    def test_15_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_16_get_quality_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_17_send_feedback_data(self):
        print(self.subscription.get_details())
        TestAIOpenScaleClient.feedback_records = 40

        feedback_data = pd.read_csv('datasets/campaign-effects/campain_effectivenes_train.csv', sep=",")

        self.subscription.feedback_logging.store(
            feedback_data=feedback_data.sample(n=self.feedback_records).to_csv(index=False),
            feedback_format=FeedbackFormat.CSV,
            data_header=True,
            data_delimiter=',')

    def test_18_stats_on_feedback_logging_table(self):
        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_19_feedback_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        feedback_distribution = TestAIOpenScaleClient.subscription.feedback_logging.data_distribution.run(
            start_date=TestAIOpenScaleClient.start_date,
            end_date=end_date,
            group=['gender'],
            agg=['product_code:avg', 'number_transactions:avg'],
            background_mode=True)
        distribution_run_id = feedback_distribution['id']
        print("Feedback data distribution run:")
        print(feedback_distribution)

        status = feedback_distribution['status']
        while status == 'initializing' or status == 'running':
            run_details = self.subscription.feedback_logging.data_distribution.get_run_details(
                run_id=distribution_run_id)
            status = run_details['status']
            print("Distribution run status: {}".format(status))
            time.sleep(10)

        run_result = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=distribution_run_id)
        print("Distribution run result:\n{}".format(run_result))

        self.assertGreater(run_result.shape[0], 1)
        self.assertEqual(run_result.shape[1], 3)
        data_columns = run_result.columns.values
        self.assertIn("gender", data_columns)
        self.assertIn("product_code:avg", data_columns)
        self.assertIn("number_transactions:avg", data_columns)

    def test_20_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=TestAIOpenScaleClient.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_21_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    # def test_22_get_metrics(self):
    #     print("Old metrics:")
    #     print(self.ai_client.data_mart.get_deployment_metrics())
    #     print(self.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
    #     print(self.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
    #     print(self.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
    #
    #     print("\nQuality metrics test: ")
    #     quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
    #     data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
    #     assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)
    #
    #     quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
    #     assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)
    #
    # def test_23_get_performance_metrics(self):
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         deployment_uid=TestAIOpenScaleClient.deployment_uid))
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         subscription_uid=TestAIOpenScaleClient.subscription.uid))
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         asset_uid=TestAIOpenScaleClient.subscription.source_uid))
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance'))
    #     print(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(
    #         deployment_uid=TestAIOpenScaleClient.subscription.get_deployment_uids()[0]))
    #
    #     self.assertTrue(
    #         len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
    #         asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance')['deployment_metrics'][
    #                             0]['metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(
    #         deployment_uid=TestAIOpenScaleClient.subscription.get_deployment_uids()[0])['metrics']) > 0)
    #
    # def test_24_setup_explainability(self):
    #     details = self.subscription.get_details()
    #     print(details)
    #     TestAIOpenScaleClient.subscription.explainability.enable(training_data=self.data_df)
    #
    # def test_25_get_details(self):
    #     details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=details)
    #
    # def test_26_get_transaction_id(self):
    #     python_table_content = self.subscription.payload_logging.get_table_content(format='python')
    #     no_payloads = len(python_table_content['values'])
    #
    #     # select random record from payload table
    #     import random
    #     random_record = random.randint(0, no_payloads - 1)
    #     TestAIOpenScaleClient.transaction_id = python_table_content['values'][random_record][0]
    #
    #     print("Selected trainsaction id: {}".format(self.transaction_id))
    #     print('subscription_details', TestAIOpenScaleClient.subscription.get_details())
    #
    # def test_27_run_explainability(self):
    #     explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id=self.transaction_id,
    #         background_mode=False
    #     )
    #     assert_explainability_run(explainability_run_details=explainability_run)
    #
    # def test_27b_list_explanations(self):
    #     TestAIOpenScaleClient.subscription.explainability.list_explanations()
    #
    # def test_28_stats_on_explainability_table(self):
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
    # def test_29_setup_fairness_monitoring(self):
    #
    #     from ibm_ai_openscale.supporting_classes.feature import Feature
    #
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         training_data=self.data_df,
    #         features=[
    #             Feature("gender", majority=['M'], minority=['F'], threshold=0.95),
    #             Feature("age", majority=[[26, 75]], minority=[[18, 25]], threshold=0.95)
    #         ],
    #         deployment_uid=None,
    #         favourable_classes=[1],
    #         unfavourable_classes=[2, 0],
    #         min_records=5
    #     )
    #
    # def test_30_get_fairness_monitoring_details(self):
    #
    #     details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
    #     assert_fairness_configuration(fairness_monitoring_details=details)
    #
    # def test_31_run_fairness(self):
    #
    #     fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
    #     assert_fairness_run(fairness_run_details=fairness_run)
    #
    # def test_32_stats_on_fairness_monitoring_table(self):
    #
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
    #     assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)
    #
    # def test_33_fairness_deployment_metrics(self):
    #
    #     fairness_metrics = TestAIOpenScaleClient.subscription.fairness_monitoring.get_deployment_metrics(deployment_uid = TestAIOpenScaleClient.deployment_uid)
    #     assert_deployment_metrics(fairness_metrics)
    #
    #     deployment_metrics = fairness_metrics['deployment_metrics'][0]['metrics']
    #     metrics_type =deployment_metrics[0]['metric_type']
    #     self.assertEqual(metrics_type,"fairness")
    #     rows_analyzed = deployment_metrics[0]['value']['rows_analyzed']
    #     self.assertEqual(rows_analyzed, 5)
    #
    #
    # def test_34_run_debias(self):
    #
    #     payload = {
    #                 "fields": ["campaign","age","age_youngest_child","branch","debt_equity","gender","bad_payment","gold_card","pension_plan",
    #                 "household_debt_to_equity_ratio","income","marital","members_in_household","months_current_account","months_customer","call_center_contacts",
    #                 "loan_accounts","number_products","number_transactions","non_worker_percentage","white_collar_percentage","rfm_score" ],
    #                 "values": [  [2.0, 19.0, 0.0, "Ravensville", 19.0, "M", 0.0, 0.0, 0.0, 64.0, 13362.0, "S", 2.0, -4.0, 0.0, 1.0, 1.0, 1.0, 0.0, 9.0, 26.0, 0.0]
    #                 ]
    #         }
    #
    #     debias_response = TestAIOpenScaleClient.subscription.fairness_monitoring.debias(payload, deployment_uid = TestAIOpenScaleClient.deployment_uid)
    #     debias_response_fields = debias_response['fields']
    #     debias_response_values = debias_response['values']
    #
    #     self.assertTrue(len(debias_response_fields)>0)
    #     self.assertTrue(len(debias_response_values)>0)
    #     self.assertIn('debiased_prediction', debias_response_fields)
    #     self.assertIn('debiased_probability', debias_response_fields)

    def test_35_disable_payload_logging_and_performance_monitoring(self):
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        self.subscription.quality_monitoring.disable()
        #
        # self.subscription.explainability.disable()
        # self.subscription.fairness_monitoring.disable()

        subscription_details = self.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
