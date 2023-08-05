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
from utils.utils import check_if_binding_exists
from utils.wml_deployments.xgboost import Iris

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
    subscription = None
    binding_uid = None

    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None
    scoring_records = None
    feedback_records = None
    final_run_details = None
    deployment = None

    start_date = datetime.utcnow().isoformat() + "Z"

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)

        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

    def test_00_get_wml_model_and_deployment_ids(self):
        TestAIOpenScaleClient.deployment = Iris()
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

    def test_03_subscribe(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(
                source_uid=self.model_uid,
                binding_uid=self.binding_uid,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                input_data_type=InputDataType.STRUCTURED,
                prediction_column='prediction',
                probability_column='probability',
                label_column='l1'
            )
        )
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid

    def test_04_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_06_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_07_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details, dynamic_schema_update=True)

    def test_08_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_09_score(self):
        fields = ['f0', 'f1', 'f2', 'f3']

        scoring_payload = {
            'fields': fields,
            'values': [
                [5.1, 3.5, 1.4, 0.2],
                [6.1, 2.9, 4.7, 1.4]
            ]
        }
        print("Scoring payload:\n{}".format(scoring_payload))

        TestAIOpenScaleClient.scoring_records = 20
        for i in range(0, int(self.scoring_records/2)):
            scoring_result = self.deployment.score(scoring_payload)

        print("Scoring result: {}".format(scoring_result))

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_10_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['f3', 'prediction'])

    def test_12_stats_on_performance_monitoring_table(self):
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

    def test_13_enable_quality_monitoring(self):
        print("Sub details: {}".format(self.subscription.get_details()))

        self.subscription.quality_monitoring.enable(threshold=0.7, min_records=10)

        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_14_feedback_logging(self):
        TestAIOpenScaleClient.feedback_records = 30

        from sklearn.datasets import load_iris
        iris_dataset = load_iris()

        data = pd.DataFrame(iris_dataset.data)
        data.columns = ['f0', 'f1', 'f2', 'f3']
        data['l1'] = iris_dataset['target']

        self.subscription.feedback_logging.store(
            feedback_data=data.sample(n=self.feedback_records).to_csv(index=False),
            feedback_format=FeedbackFormat.CSV,
            data_header=True,
            data_delimiter=',')

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_15_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_16_feedback_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        feedback_distribution_run = TestAIOpenScaleClient.subscription.feedback_logging.data_distribution.run(
            start_date=TestAIOpenScaleClient.start_date,
            end_date=end_date,
            group=['f0', 'f1'],
            agg=['count'])

        run_id = feedback_distribution_run['id']
        feedback_distribution = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=run_id)
        assert_data_distribution_run(
            data_distribution_result=feedback_distribution,
            no_columns=3,
            no_rows=3,
            columns=['f0', 'f1'],
            greater_comparision=True,
        )

    def test_17_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_18_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    def test_19_get_metrics(self):
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

    def test_20_disable_monitors(self):
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
