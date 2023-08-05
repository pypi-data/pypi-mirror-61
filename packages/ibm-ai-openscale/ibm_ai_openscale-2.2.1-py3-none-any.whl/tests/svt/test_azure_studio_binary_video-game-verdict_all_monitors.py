# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pandas as pd

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.utils import *
from utils.configuration import get_azure_credentials

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature
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
    payload_table_content = None
    final_run_details = None
    start_date = datetime.utcnow().isoformat() + "Z"
    data_df = None

    credentials = None

    def score(self, subscription_details):
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

        df = pd.read_csv("datasets/video-games-rating/video_game_sales_with_verdict.csv")
        l = ['Year_of_Release', 'NA_Sales', 'User_Score', 'Verdict']
        feature_cols = [i for i in list(df.columns) if i not in l]

        categorical_columns = ['Name', 'Platform', 'Genre', 'Publisher', 'Developer', 'Rating']
        df = df.dropna()
        input_values = df[feature_cols].values.tolist()[:200:5]

        input1 = [{field: value for field, value in zip(feature_cols, input_value)} for input_value in input_values]

        data = {
            "Inputs": {
                "input1": input1
            },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        token = subscription_details['entity']['deployments'][0]['scoring_endpoint']['credentials']['token']
        headers = subscription_details['entity']['deployments'][0]['scoring_endpoint']['request_headers']
        headers['Authorization'] = ('Bearer ' + token)

        start_time = time.time()
        response = requests.post(url=scoring_url, data=body, headers=headers)
        response_time = time.time() - start_time
        result = response.json()
        print('--> Azure\nScoring payload: {}\nScoring result: {}\nResponse time: {}'.format(data, result, response_time))

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
        assert_datamart_details(details, schema=self.schema, state='active')

    def test_02_bind_azure(self):
        TestAIOpenScaleClient.binding_uid = check_if_binding_exists(
            self.ai_client,
            self.credentials,
            type='azure_machine_learning')

        if TestAIOpenScaleClient.binding_uid is None:
            print("Binding does not exist. Creating a new one.")
            TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add(
                "Azure ml engine", AzureMachineLearningStudioInstance(self.credentials))

        print("Binding uid: {}".format(self.binding_uid))

    def test_03_get_binding_details(self):
        print('Binding details: {}'.format(TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)))
        self.ai_client.data_mart.bindings.list()

    def test_04_get_assets(self):

        # NOTE
        #
        # It takes a long time to get all assets
        # to decrease execution time asset uid is hardcoded

        # assets_uids = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()
        # self.assertGreater(len(assets_uids), 1)
        # print('Assets uids: ' + str(assets_uids))
        #
        # TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()
        # asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details(
        #     binding_uid=TestAIOpenScaleClient.binding_uid)
        # print('Assets details: ' + str(asset_details))
        # #
        # for detail in asset_details:
        #     if 'videogameverdict.binary' in detail['name']:
        #         TestAIOpenScaleClient.source_uid = detail['source_uid']
        #
        #         print("Selected asset details: {}".format(detail))
        #
        # print("Source uid: {}".format(self.source_uid))

        TestAIOpenScaleClient.source_uid = "20a23d9de1ab5762b880d7bc4ce09ff2"
        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_05_subscribe_azure_asset(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            AzureMachineLearningStudioAsset(
                source_uid=TestAIOpenScaleClient.source_uid,
                binding_uid=TestAIOpenScaleClient.binding_uid,
                input_data_type=InputDataType.STRUCTURED,
                problem_type=ProblemType.BINARY_CLASSIFICATION,
                probability_column='Scored Probabilities',
                label_column='Verdict',
                prediction_column='Scored Labels',
                feature_columns=['Name', 'Platform', 'Genre', 'Publisher', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Count', 'Developer', 'Rating'],
                categorical_columns=['Name', 'Platform', 'Genre', 'Publisher', 'Developer', 'Rating']
            )
        )

        TestAIOpenScaleClient.subscription_uid = subscription.uid

    def test_06_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        details = self.subscription.get_details()

        assert_subscription_details(subscription_details=details, no_deployments=1, text_included='azureml', enabled_monitors=['payload_logging', 'performance_monitoring'])

    def test_07_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_check_default_monitors_enablement(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_09_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details, dynamic_schema_update=False)

    def test_10_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_11_score_model_and_log_payload(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        request, response, response_time = self.score(subscription_details)
        records_list = []
        import random
        TestAIOpenScaleClient.scoring_records = 10

        for i in range(0, self.scoring_records):
            records_list.append(PayloadRecord(request=request, response=response, response_time=random.randint(0, 10)))

        TestAIOpenScaleClient.scoring_records = len(records_list) * len(request['Inputs']['input1'])

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_12_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        TestAIOpenScaleClient.payload_table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(
            pandas_table_content=self.payload_table_content,
            scoring_records=self.scoring_records
        )

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['Scored Probabilities', 'Scored Labels'])

        print('subscription details', TestAIOpenScaleClient.subscription.get_details())

    def test_13_payload_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        data_distribution_run = TestAIOpenScaleClient.subscription.payload_logging.data_distribution.run(
            start_date=self.start_date,
            end_date=end_date,
            group=['Platform', 'Publisher'],
            background_mode=False)

        run_id = data_distribution_run['id']
        data_distribution = self.subscription.payload_logging.data_distribution.get_run_result(run_id=run_id)
        print('Payload data distribution')
        print(data_distribution)

        self.assertTrue("10" in str(data_distribution))

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
        TestAIOpenScaleClient.feedback_records = 40

        df = pd.read_csv("datasets/video-games-rating/video_game_sales_with_verdict-feedback.csv", sep=';').sample(n=self.feedback_records)
        feedback_records = []

        fields = df.columns.tolist()

        for index, row in df.iterrows():
            feedback_records.append(row.tolist())

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_records, fields=fields)

        print("Waiting 30 seconds for propagation.")
        time.sleep(30)

    def test_18_stats_on_feedback_logging_table(self):
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
            group=['Platform', 'Publisher'],
            background_mode=True)

        distribution_run_id = feedback_distribution['id']
        print("Feedback data distribution run:")
        print(feedback_distribution)

        status = feedback_distribution['status']
        run_details = ""
        while status == 'initializing' or status == 'running':
            run_details = self.subscription.feedback_logging.data_distribution.get_run_details(run_id=distribution_run_id)
            status = run_details['status']
            print("Distribution run status: {}".format(status))
            time.sleep(10)

        self.assertNotEqual(status, 'failed', msg="Feedback data distribution failed! Reason: {}".format(run_details))

        run_result = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=distribution_run_id)
        print("Distribution run result:\n{}".format(run_result))

        self.assertGreater(run_result.shape[0], 1)
        self.assertGreater(run_result.shape[1], 1)
        data_columns = run_result.columns.values
        self.assertIn("Publisher", data_columns)
        self.assertIn("Platform", data_columns)
        self.assertIn("count", data_columns)

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
    #     assert_quality_metrics_binary_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)
    #
    # def test_23_get_performance_metrics(self):
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
    #     print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance'))
    #     print(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.subscription.get_deployment_uids()[0]))
    #
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance')['deployment_metrics'][0]['metrics']) > 0)
    #     self.assertTrue(len(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.subscription.get_deployment_uids()[0])['metrics']) > 0)
    #
    # def test_24_setup_explainability(self):
    #     data_df = pd.read_csv("datasets/video-games-rating/video_game_sales_with_verdict.csv")
    #     TestAIOpenScaleClient.data_df = data_df.dropna().copy()
    #
    #     TestAIOpenScaleClient.subscription.explainability.enable(
    #         training_data=TestAIOpenScaleClient.data_df
    #     )
    #
    # def test_25_get_details(self):
    #     details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=details)
    #
    # def test_26_get_transaction_id(self):
    #     pandas_pd = self.subscription.payload_logging.get_table_content()
    #     no_payloads = len(pandas_pd['scoring_id'].values)
    #
    #     # select random record from payload table
    #     import random
    #     random_record = random.randint(0, no_payloads - 1)
    #     TestAIOpenScaleClient.transaction_id = pandas_pd['scoring_id'].values[random_record]
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
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         features=[
    #             Feature("Platform", majority=["Wii"], minority=["X360"], threshold=0.8)
    #         ],
    #         favourable_classes=["Hit"],
    #         unfavourable_classes=["Flop"],
    #         min_records=5,
    #         training_data=TestAIOpenScaleClient.data_df
    #     )
    #
    # def test_30_get_fairness_monitoring_details(self):
    #     details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
    #     assert_fairness_configuration(fairness_monitoring_details=details)
    #
    # def test_31_run_fairness(self):
    #     fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
    #     assert_fairness_run(fairness_run_details=fairness_run)
    #
    # def test_32_stats_on_fairness_monitoring_table(self):
    #     time.sleep(5)
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
    #     assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)

    def test_33_disable_monitors(self):
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        self.subscription.quality_monitoring.disable()
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
