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
from utils.wml import *
from utils.wml_deployments.scikit import MulticlassDigits

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2


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
    final_run_details = None
    scoring_records = 15
    feedback_records = 10

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = MulticlassDigits()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_wml_instance(self):
        if is_icp():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP",
                                                                                      WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud",
                                                                                      WatsonMachineLearningInstance(
                                                                                          self.wml_credentials))

    def test_03_get_model_ids(self):
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_04_subscribe(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(
                source_uid=self.model_uid,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                prediction_column='prediction'))
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid
        print("Subscription details: {}".format(self.subscription.get_details()))

    def test_05_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_06_list_deployments(self):
        self.subscription.list_deployments()

    def test_07_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_08_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_09_score(self):
        payload_scoring = {"values": [
            [0, 0, 5, 16, 16, 3, 0, 0, 0, 0, 9, 16, 7, 0, 0, 0, 0, 0, 12, 15, 2, 0, 0, 0, 0, 1, 15, 16, 15, 4, 0, 0, 0, 0,
             9, 13, 16, 9, 0, 0, 0, 0, 0, 0, 14, 12, 0, 0, 0, 0, 5, 12, 16, 8, 0, 0, 0, 0, 3, 15, 15, 1, 0, 0],
            [0, 0, 6, 16, 12, 1, 0, 0, 0, 0, 5, 16, 13, 10, 0, 0, 0, 0, 0, 5, 5, 15, 0, 0, 0, 0, 0, 0, 8, 15, 0, 0, 0, 0, 0,
             0, 13, 13, 0, 0, 0, 0, 0, 6, 16, 9, 4, 1, 0, 0, 3, 16, 16, 16, 16, 10, 0, 0, 5, 16, 11, 9, 6, 2]]}

        TestAIOpenScaleClient.scoring_records = 30
        for i in range(0, int(self.scoring_records/2)):
            TestAIOpenScaleClient.scoring_result = self.deployment.score(payload=payload_scoring)
            self.assertIsNotNone(self.scoring_result)

        print(self.scoring_result)

    def test_10_stats_on_payload_logging_table(self):
        if self.scoring_result is None:
            self.skipTest(reason="Scoring failed. Skipping payload logging table check.")

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['prediction', 'probability'])

    def test_11_performance_monitoring(self):
        if is_icp():
            self.skipTest("Performance monitoring is not working on ICP with WML scoring.")

        if not is_ypqa():
            self.skipTest("Performance monitoring V2 is only on YP-QA env.")

        print("Performance V2")
        hrefs_v2 = AIHrefDefinitionsV2(get_aios_credentials())

        response = request_session.get(
            url=hrefs_v2.get_monitor_instances_href(),
            headers=self.ai_client._get_headers()
        )

        performance_monitor_id = None
        result = response.json()
        for monitor_instance in result["monitor_instances"]:
            if monitor_instance["entity"]["monitor_definition_id"] == "performance" and \
                    monitor_instance["entity"]["target"]["target_id"] == self.subscription_uid:
                performance_monitor_id = monitor_instance["metadata"]["id"]

        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        current_time = datetime.utcnow().isoformat() + 'Z'
        query = "?start={}&end={}".format(start_time, current_time)
        url = hrefs_v2.get_measurements_href(performance_monitor_id) + query

        requests_count = wait_for_v2_performance_measurements(
            measurements_url=url,
            no_request=TestAIOpenScaleClient.scoring_records,
            headers=self.ai_client._get_headers()
        )

        self.assertEquals(TestAIOpenScaleClient.scoring_records, requests_count,
                          msg="Request count calculated by the performance monitor is different than scored in the WML")

    def test_12_enable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.7, min_records=5)

        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_13_feedback_logging(self):
        records = []
        feedback_payload = [0, 0, 5, 16, 16, 3, 0, 0, 0, 0, 9, 16, 7, 0, 0, 0, 0, 0, 12, 15, 2, 0, 0, 0, 0, 1, 15, 16, 15, 4, 0, 0, 0,
                            0, 9, 13, 16, 9, 0, 0, 0, 0, 0, 0, 14, 12, 0, 0, 0, 0, 5, 12, 16, 8, 0, 0, 0, 0, 3, 15, 15, 1, 0, 0, 2]

        for i in range(0, 10):
            records.append(feedback_payload)
        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=records)

        wait_for_feedback_table(subscription=self.subscription, feedback_records=len(records))

    def test_14_stats_on_feedback_logging(self):
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()

    def test_15_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_16_get_quality_metrics(self):
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_17_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_18_disable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()
        TestAIOpenScaleClient.subscription.performance_monitoring.disable()
        TestAIOpenScaleClient.subscription.quality_monitoring.disable()

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()


