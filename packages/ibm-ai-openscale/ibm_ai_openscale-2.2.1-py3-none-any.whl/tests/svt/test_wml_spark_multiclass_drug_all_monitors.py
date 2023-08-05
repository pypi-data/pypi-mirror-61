# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from utils.assertions import *
from utils.waits import *
from utils.wml_deployments.spark import Drug
from utils.utils import check_if_binding_exists

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.feature import Feature
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType


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
    deployment = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None
    transaction_id = None
    final_run_details = None

    start_date = datetime.utcnow().isoformat() + "Z"
    feedback_records = 0
    scoring_records = 0

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

    def test_00_prepare_wml_deployment(self):
        TestAIOpenScaleClient.deployment = Drug()
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_wml_instance(self):
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

    def test_04_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='predictedLabel',
            probability_column='probability',
            feature_columns=["AGE", "SEX", "BP", "CHOLESTEROL", "NA", "K"],
            categorical_columns=["SEX", "BP", "CHOLESTEROL"],
            training_data_reference=get_cos_training_data_reference()
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid

        print("Subscription details: {}".format(subscription.get_details()))

    def test_05_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

    def test_06_score(self):
        fields = ["AGE", "SEX", "BP", "CHOLESTEROL", "NA", "K"]
        values = [
            [54, "M", "HIGH", "HIGH", 0.657, 0.234]
        ]

        payload_scoring = {"fields": fields, "values": values}
        print("Scoring payload: {}".format(payload_scoring))

        TestAIOpenScaleClient.scoring_records = 20
        for i in range(0, self.scoring_records):
            self.deployment.score(payload_scoring)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_07_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['prediction', 'probability'])

    def test_08_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_09_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_10_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_11_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_12_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_13_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_14_get_quality_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_15_send_feedback_data(self):
        feedback_data = [
                [74.0, 'M', 'HIGH', 'HIGH', 0.715337, 0.074773, 'drugB'],
                [58.0, 'F', 'HIGH', 'NORMAL', 0.868924, 0.061023, 'drugB'],
                [68.0, 'F', 'HIGH', 'NORMAL', 0.77541, 0.0761, 'drugB'],
                [65.0, 'M', 'HIGH', 'NORMAL', 0.635551, 0.056043, 'drugB'],
                [60.0, 'F', 'HIGH', 'HIGH', 0.800607, 0.060181, 'drugB'],
                [70.0, 'M', 'HIGH', 'HIGH', 0.658606, 0.047153, 'drugB'],
                [60.0, 'M', 'HIGH', 'HIGH', 0.805651, 0.057821, 'drugB'],
                [59.0, 'M', 'HIGH', 'HIGH', 0.816356, 0.058583, 'drugB'],
                [60.0, 'F', 'HIGH', 'HIGH', 0.800607, 0.060181, 'drugB'],
                [70.0, 'M', 'HIGH', 'HIGH', 0.658606, 0.047153, 'drugB'],
                [60.0, 'M', 'HIGH', 'HIGH', 0.805651, 0.057821, 'drugB'],
                [59.0, 'M', 'HIGH', 'HIGH', 0.816356, 0.058583, 'drugB'],
                [26.0, 'F', 'LOW', 'HIGH', 0.578002, 0.040819, 'drugC'],
                [32.0, 'F', 'LOW', 'HIGH', 0.730854, 0.075256, 'drugC'],
                [50.0, 'F', 'NORMAL', 'NORMAL', 0.601915, 0.048957, 'drugX'],
                [66.0, 'F', 'NORMAL', 'NORMAL', 0.611333, 0.075412, 'drugX']
            ]
        TestAIOpenScaleClient.subscription.feedback_logging.store(
            feedback_data=feedback_data,
            fields=['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K', 'DRUG']
        )

        TestAIOpenScaleClient.feedback_records = len(feedback_data)

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_16_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_17_feedback_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        feedback_distribution = TestAIOpenScaleClient.subscription.feedback_logging.data_distribution.run(
            start_date=self.start_date,
            end_date=end_date,
            group=['AGE', 'SEX'],
            agg=['count'],
            max_bins=3,
            background_mode=True)
        distribution_run_id = feedback_distribution['id']

        wait_for_feedback_data_distribution(subscription=self.subscription, distribution_run_id=distribution_run_id)
        run_result = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=distribution_run_id)

        assert_data_distribution_run(
            data_distribution_result=run_result,
            no_columns=3,
            no_rows=4,
            columns=['AGE', 'SEX', 'count']
        )

    def test_18_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_19_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    def test_20_stats_on_performance_monitoring_table(self):
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
    #
    # def test_23_get_transaction_id(self):
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
    # def test_24_setup_explainability(self):
    #     TestAIOpenScaleClient.subscription.explainability.enable()
    #
    # def test_25_run_explainability(self):
    #     explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id=self.transaction_id,
    #         background_mode=False
    #     )
    #     assert_explainability_run(explainability_run_details=explainability_run)
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

    def test_27_setup_fairness_monitoring(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
            features=[
                Feature("AGE", majority=[[20, 50], [60, 70]], minority=[[51, 59]], threshold=0.8)
            ],
            favourable_classes=['drugY'],
            unfavourable_classes=['drugA', 'drugB', 'drugC'],
            min_records=12
        )

    def test_28_get_fairness_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
        assert_fairness_configuration(fairness_monitoring_details=details)

    def test_29_run_fairness(self):
        fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
        assert_fairness_run(fairness_run_details=fairness_run)

    def test_30_stats_on_fairness_monitoring_table(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
        TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()

        pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
        assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)

        python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
        assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)

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
        assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_32_disable_monitors(self):
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        self.subscription.quality_monitoring.disable()
        # self.subscription.explainability.disable()
        self.subscription.fairness_monitoring.disable()

        subscription_details = self.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
