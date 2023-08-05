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
from utils.utils import check_if_binding_exists
from utils.wml_deployments.function import MultiplyFunction

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    function_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    binding_uid = None
    subscription = None
    final_run_details = None

    scoring_records = None
    feedback_records = None

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = MultiplyFunction()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

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

    def test_03_get_model_ids(self):
        TestAIOpenScaleClient.function_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

    def test_04_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.function_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='multiplication',
            label_column='label'
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid

        print("Subscription details: {}".format(subscription.get_details()))

    def test_05_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_06_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_07_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_08_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details, dynamic_schema_update=True)

    def test_09_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_10_score(self):
        payload_scoring = {"fields": ["x", "y"],
                           "values": [[2.0, 3.0], [3.1, 2.2]]}

        TestAIOpenScaleClient.scoring_records = 20
        for i in range(0, int(self.scoring_records/2)):
            scorings = self.deployment.score(payload_scoring)
            self.assertIsNotNone(scorings)
            print("Score result: {}".format(scorings))

    def test_11_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['x', 'y', 'multiplication'])

    def test_12_performance_monitoring(self):
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

    def test_13_enable_quality_monitoring(self):
        self.subscription.quality_monitoring.enable(threshold=0.7, min_records=10)

    def test_14_get_quality_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_15_send_feedback_data(self):
        feedback_data = []
        fields = ['x', 'y', 'label']

        TestAIOpenScaleClient.feedback_records = 48
        for i in range(0, int(self.feedback_records/4)):
            feedback_data.append([3.0, 5.0, 15.0])
            feedback_data.append([2.0, 10.0, 20.0])
            feedback_data.append([1.0, 10.0, 10.0])
            feedback_data.append([33.0, 3.0, 99.0])

        self.subscription.feedback_logging.store(feedback_data, fields=fields)
        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_16_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_17_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_18_get_quality_metrics(self):
        quality_monitoring_metrics = wait_for_quality_metrics(subscription=self.subscription)
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality',
                                                                                    asset_uid=quality_monitoring_metrics[0]['asset_id'])
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_19_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    def test_20_disable_quality_and_performance_monitoring(self):
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        self.subscription.quality_monitoring.disable()

        subscription_details = self.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
