# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.wml_deployments.auto_ai import CarPrice
from utils.utils import check_if_binding_exists

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import Feature
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType


class TestAIOpenScaleClient(unittest.TestCase):
    transaction_id = None
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
    final_run_details = None
    deployment = None

    scoring_records = 0
    feedback_records = 0

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = CarPrice()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        assert_datamart_details(details, schema=self.schema, state='active')

    def test_03_bind_wml_instance(self):
        if is_icp():
            TestAIOpenScaleClient.binding_uid = check_if_binding_exists(
                self.ai_client,
                {},
                type='watson_machine_learning')

            if TestAIOpenScaleClient.binding_uid is None:
                TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add(
                    "WML instance on ICP",
                    WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = check_if_binding_exists(
                self.ai_client,
                self.wml_credentials,
                type='watson_machine_learning')

            if TestAIOpenScaleClient.binding_uid is None:
                TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add(
                    "WML instance on Cloud",
                    WatsonMachineLearningInstance(self.wml_credentials))

        print("Binding uid: {}".format(self.binding_uid))
        self.assertIsNotNone(self.binding_uid)

    def test_04_list_assets(self):
        self.ai_client.data_mart.bindings.list_assets()
        self.ai_client.data_mart.bindings.list_asset_deployments()

    def test_05_get_model_ids(self):
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.REGRESSION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='prediction',
            feature_columns=["car_ID", "symboling", "CarName", "fueltype", "aspiration", "doornumber", "carbody",
                             "drivewheel", "enginelocation", "wheelbase", "carlength", "carwidth", "carheight",
                             "curbweight", "enginetype", "cylindernumber", "enginesize", "fuelsystem", "boreratio",
                             "stroke", "compressionratio", "horsepower", "peakrpm", "citympg", "highwaympg"],
            categorical_columns=[],
            label_column='Price'
        ))
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription details: {}".format(subscription.get_details()))

    def test_07_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

    def test_08_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_09_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_10_score(self):
        # payload_scoring = {
        #         "fields": ["car_ID", "symboling", "CarName", "fueltype", "aspiration", "doornumber", "carbody",
        #                    "drivewheel", "enginelocation", "wheelbase", "carlength", "carwidth", "carheight",
        #                    "curbweight", "enginetype", "cylindernumber", "enginesize", "fuelsystem", "boreratio",
        #                    "stroke", "compressionratio", "horsepower", "peakrpm", "citympg", "highwaympg"],
        #         "values": [
        #             [12, 0, "bmw 320i", "gas", "std", "four", "sedan", "rwd", "front", 101.2, 176.8, 64.8, 54.3, 2395,
        #              "ohc", "four",
        #              108, "mpfi", 3.5, 2.8, 8.8, 101, 5800, 23, 29],
        #             [201, -1, "volvo 145e (sw)", "gas", "std", "four", "sedan", "rwd", "front", 109.1, 188.8, 68.9, 55.5,
        #              2952, "ohc", "four", 141, "mpfi", 3.78, 3.15, 9.5, 114, 5400, 23, 28, 16845],
        #             [177, -1, "toyota corolla", "gas", "std", "four", "sedan", "fwd", "front", 102.4, 175.6, 66.5,
        #              54.9, 2414, "ohc", "four", 122, "mpfi", 3.31, 3.54, 8.7, 92, 4200, 27, 32, 10898],
        #             [147, 0, "subaru trezia", "gas", "std", "four", "wagon", "fwd", "front", 97, 173.5, 65.4, 53, 2290,
        #              "ohcf", "four", 108, "2bbl", 3.62, 2.64, 9, 82, 4800, 28, 32, 7463]
        #         ]
        #     }
        payload_scoring = {
            "fields": ["car_ID", "symboling", "CarName", "fueltype", "aspiration", "doornumber", "carbody",
                       "drivewheel", "enginelocation", "wheelbase", "carlength", "carwidth", "carheight",
                       "curbweight", "enginetype", "cylindernumber", "enginesize", "fuelsystem", "boreratio",
                       "stroke", "compressionratio", "horsepower", "peakrpm", "citympg", "highwaympg"],
            "values": [
                [12, 0, "bmw 320i", "gas", "std", "four", "sedan", "rwd", "front", 101.2, 176.8, 64.8, 54.3, 2395,
                 "ohc", "four", 108, "mpfi", 3.5, 2.8, 8.8, 101, 5800, 23, 29]
            ]
        }

        TestAIOpenScaleClient.scoring_records = 10
        for _ in range(0, int(self.scoring_records)):
            TestAIOpenScaleClient.scoring_result = self.deployment.score(payload=payload_scoring)

    def test_11_stats_on_payload_logging_table(self):
        if self.scoring_result is None:
            self.skipTest(reason="Scoring failed. Skipping payload logging table check.")

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()
        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content,
                                                    scoring_records=self.scoring_records)
        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['prediction'])

    def test_12_payload_logging_data_distribution(self):
        payload_data_distribution_run = TestAIOpenScaleClient.subscription.payload_logging.data_distribution.run(
            group=['CarName', 'carbody'],
            background_mode=False)

        distribution_run_id = payload_data_distribution_run['id']
        print("Payload data distribution run:")
        print(payload_data_distribution_run)

        data_distribution = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=distribution_run_id)

        print('Payload data distribution:')
        print(data_distribution)

        self.assertGreater(data_distribution.shape[0], 0)
        self.assertGreater(data_distribution.shape[1], 0)
        data_columns = data_distribution.columns.values
        self.assertIn("CarName", data_columns)
        self.assertIn("carbody", data_columns)

    def test_13_stats_on_performance_monitoring_table(self):
        if is_icp():
            self.skipTest("Performance monitoring is not working on ICP with WML scoring.")

        wait_for_performance_table(subscription=self.subscription)

        self.subscription.performance_monitoring.print_table_schema()
        self.subscription.performance_monitoring.show_table()
        self.subscription.performance_monitoring.describe_table()

        performance_table_pandas = self.subscription.performance_monitoring.get_table_content()
        assert_performance_monitoring_pandas_table_content(pandas_table_content=performance_table_pandas)

        performance_table_python = self.subscription.performance_monitoring.get_table_content(format='python')
        assert_performance_monitoring_python_table_content(python_table_content=performance_table_python)

    def test_14_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_15_get_quality_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_16_send_feedback_data(self):
        feedback_records = []

        TestAIOpenScaleClient.feedback_records = 40
        for i in range(0, int(self.feedback_records/4)):
            feedback_records.append([1, 3, "alfa-romero stelvio", "gas", "std", "two", "convertible", "rwd", "front",
                                     88.6, 168.8, 64.1, 48.8, 2548, "dohc", "four", 130, "mpfi", 3.47, 2.68, 9,
                                     111, 5000, 21, 27, 16500])
            feedback_records.append([6, 2, "audi fox", "gas", "std", "two", "sedan", "fwd", "front", 99.8, 177.3, 66.3,
                                     53.1, 2507, "ohc", "five", 136, "mpfi", 3.19, 3.4, 8.5, 110, 5500, 19, 25, 15250])
            feedback_records.append([65, 0, "mazda 626", "gas", "std", "four", "hatchback", "fwd", "front", 98.8, 177.8,
                                     66.5, 55.5, 2425, "ohc", "four", 122, "2bbl", 3.39, 3.39, 8.6, 84, 4800, 26, 32, 11245])
            feedback_records.append([189, 2, "volkswagen dasher", "gas", "std", "four", "sedan", "fwd", "front", 97.3,
                                     171.7, 65.5, 55.7, 2300, "ohc", "four", 109, "mpfi", 3.19, 3.4, 10, 100, 5500,
                                     26, 32, 9995])


        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_records)

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_18_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_19_feedback_logging_data_distribution(self):
        feedback_distribution = TestAIOpenScaleClient.subscription.feedback_logging.data_distribution.run(
            group=['enginetype', 'cylindernumber'],
            background_mode=True)
        distribution_run_id = feedback_distribution['id']
        print("Feedback data distribution run:")
        print(feedback_distribution)

        status = feedback_distribution['status']
        while status == 'initializing' or status == 'running':
            run_details = self.subscription.feedback_logging.data_distribution.get_run_details(run_id=distribution_run_id)
            status = run_details['status']
            print("Distribution run status: {}".format(status))
            time.sleep(10)

        run_result = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=distribution_run_id)
        print("Distribution run result:\n{}".format(run_result))

        self.assertGreater(run_result.shape[0], 1)
        self.assertGreater(run_result.shape[1], 1)
        data_columns = run_result.columns.values
        self.assertIn("enginetype", data_columns)
        self.assertIn("cylindernumber", data_columns)
        self.assertIn("count", data_columns)

    def test_20_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
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

    # def test_22_setup_explainability(self):
    #     TestAIOpenScaleClient.subscription.explainability.enable()
    #
    # def test_23_get_details(self):
    #     details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=details)
    #
    # def test_24_get_transaction_id(self):
    #     pandas_pd = self.subscription.payload_logging.get_table_content()
    #     no_payloads = len(pandas_pd['scoring_id'].values)
    #
    #     # select random record from payload table
    #     import random
    #     random_record = random.randint(0, no_payloads-1)
    #     TestAIOpenScaleClient.transaction_id = pandas_pd['scoring_id'].values[random_record]
    #
    #     print("Selected trainsaction id: {}".format(self.transaction_id))
    #
    # def test_25_run_explainability(self):
    #     explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id=self.transaction_id,
    #         background_mode=False
    #     )
    #     assert_explainability_run(explainability_run_details=explainability_run)
    #
    # def test_25b_list_explanations(self):
    #     TestAIOpenScaleClient.subscription.explainability.list_explanations()
    #
    # def test_26_stats_on_explainability_table(self):
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
    # def test_27_setup_fairness_monitoring(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         features=[
    #             Feature("Sex", majority=['male'], minority=['female'], threshold=0.95),
    #             Feature("Age", majority=[[26, 75]], minority=[[18, 25]], threshold=0.95)
    #         ],
    #         favourable_classes=['No Risk'],
    #         unfavourable_classes=['Risk'],
    #         min_records=4,
    #     )
    #
    # def test_28_get_fairness_monitoring_details(self):
    #     details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
    #     assert_fairness_configuration(fairness_monitoring_details=details)
    #
    # def test_29_run_fairness(self):
    #     fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
    #     assert_fairness_run(fairness_run_details=fairness_run)
    #
    # def test_30_stats_on_fairness_monitoring_table(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
    #     assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)

    def test_31_get_metrics(self):
        print("Old metrics:")
        print(self.ai_client.data_mart.get_deployment_metrics())
        print(self.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(self.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(self.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))

        print("\nQuality metrics test: ")
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_regression_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_32_disable_monitors(self):
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
