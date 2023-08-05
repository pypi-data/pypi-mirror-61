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
from utils.wml import *
from utils.wml_deployments.spark import RegressionCustomerSatisfaction

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat


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
    transaction_id = None
    scoring_records = None
    feedback_records = None
    final_run_details = None

    start_date = datetime.utcnow().isoformat() + "Z"
    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = RegressionCustomerSatisfaction()

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
        from ibm_ai_openscale.supporting_classes.enums import ProblemType
        from ibm_ai_openscale.supporting_classes.enums import InputDataType

        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(
                training_data_reference=get_db2_training_data_reference(dataset="CustomerChurn"),
                source_uid=self.model_uid,
                binding_uid=self.binding_uid,
                label_column='TotalCharges',
                # prediction_column='prediction',
                probability_column='probability',
                problem_type=ProblemType.REGRESSION,
                input_data_type=InputDataType.STRUCTURED,
                # feature_columns=["customerID", "gender", 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges'],
                # categorical_columns=["gender", "SeniorCitizen", "PaymentMethod"]
            )
        )
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid
        print("Subscription details: {}".format(self.subscription.get_details()))

    def test_05_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_06_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_07_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_08_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_09_score(self):
        scoring_payload = {
            "fields": ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
                       "MultipleLines", "InternetService", "OnlineSecurity",
                       "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
                       "PaperlessBilling", "PaymentMethod", "MonthlyCharges"],
            "values": [
                [
                    "9237-HQITU",
                    "Female",
                    0,
                    "No",
                    "No",
                    20,
                    "Yes",
                    "No",
                    "Fiber optic",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No",
                    "Month-to-month",
                    "Yes",
                    "Electronic check",
                    70.7
                ],
                [
                    "3638-WEABW",
                    "Female",
                    0,
                    "Yes",
                    "No",
                    58,
                    "Yes",
                    "Yes",
                    "DSL",
                    "No",
                    "Yes",
                    "No",
                    "Yes",
                    "No",
                    "No",
                    "Two year",
                    "Yes",
                    "Credit card (automatic)",
                    59.900
                ],
                [
                    "8665-UTDHZ",
                    "Male",
                    0,
                    "Yes",
                    "Yes",
                    1,
                    "No",
                    "No phone service",
                    "DSL",
                    "No",
                    "Yes",
                    "No",
                    "No",
                    "No",
                    "No",
                    "Month-to-month",
                    "No",
                    "Electronic check",
                    30.200
                ],
                [
                    "8773-HHUOZ",
                    "Female",
                    0,
                    "No",
                    "Yes",
                    17,
                    "Yes",
                    "No",
                    "DSL",
                    "No",
                    "No",
                    "No",
                    "No",
                    "Yes",
                    "Yes",
                    "Month-to-month",
                    "Yes",
                    "Mailed check",
                    64.700
                ]
            ]
        }
        print("Scoring payload:\n{}".format(scoring_payload))

        TestAIOpenScaleClient.scoring_records = 20
        for i in range(0, int(self.scoring_records / 4)):
            scoring_result = self.deployment.score(payload=scoring_payload)
            self.assertIsNotNone(scoring_result)

        print("Scoring result:\n{}".format(scoring_result))

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_10_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content,
                                                    scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content,
                                                    fields=['prediction', 'probability'])

        print('Subscription details', TestAIOpenScaleClient.subscription.get_details())

    def test_11_payload_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        data_distribution_run = TestAIOpenScaleClient.subscription.payload_logging.data_distribution.run(
            start_date=self.start_date,
            end_date=end_date,
            group=['gender', 'InternetService'],
            background_mode=False,
            agg=['MonthlyCharges:sum'],
            filter=['InternetService:in:[DSL]'])

        run_id = data_distribution_run['id']
        data_distribution = self.subscription.payload_logging.data_distribution.get_run_result(run_id=run_id)

        assert_data_distribution_run(
            data_distribution_result=data_distribution,
            no_rows=2,
            no_columns=3,
            columns=['gender', 'InternetService', 'MonthlyCharges:sum']
        )

    def test_14_stats_on_performance_monitoring_table(self):
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

    def test_15_enable_quality_monitoring(self):
        self.subscription.quality_monitoring.enable(threshold=0.7, min_records=10)

        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_16_feedback_logging(self):

        TestAIOpenScaleClient.feedback_records = 50

        training_data = pd.read_csv('datasets/SparkMlibRegression/WA_FnUseC_TelcoCustomerChurn.csv', sep=',')

        self.subscription.feedback_logging.store(
            feedback_data=training_data.sample(n=self.feedback_records).to_csv(index=False),
            feedback_format=FeedbackFormat.CSV,
            data_header=True,
            data_delimiter=',')

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_17_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_18_feedback_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        feedback_distribution_run = TestAIOpenScaleClient.subscription.feedback_logging.data_distribution.run(
            start_date=TestAIOpenScaleClient.start_date,
            end_date=end_date,
            group=['MonthlyCharges', 'OnlineBackup'],
            agg=['count'],
            filter=['OnlineBackup:eq:Yes'])

        run_id = feedback_distribution_run['id']
        feedback_distribution = self.subscription.feedback_logging.data_distribution.get_run_result(run_id=run_id)
        assert_data_distribution_run(
            data_distribution_result=feedback_distribution,
            no_columns=3,
            no_rows=2,
            columns=['MonthlyCharges', 'OnlineBackup', 'count'],
            greater_comparision=True
        )

    def test_19_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_20_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    # def test_19_get_transaction_id(self):
    #     python_table_content = self.subscription.payload_logging.get_table_content(format='python')
    #     no_payloads = len(python_table_content['values'])
    #
    #     # select random record from payload table
    #     import random
    #     random_record = random.randint(0, no_payloads - 1)
    #     TestAIOpenScaleClient.transaction_id = [dict(zip(python_table_content['fields'], row)) for row in python_table_content['values']][random_record]['scoring_id']
    #
    #     print("Selected trainsaction id: {}".format(self.transaction_id))

    # SKIPPED FOR NOW
    #
    # def test_20_setup_explainability(self):
    #     TestAIOpenScaleClient.subscription.explainability.enable()
    #
    # def test_21_get_explainability_details(self):
    #     details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=details)
    #
    # def test_22_run_explainability(self):
    #     explainability_run_detais = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id=self.transaction_id,
    #         background_mode=False
    #     )
    #     assert_explainability_run(explainability_run_details=explainability_run_detais)
    #
    # def test_23_stats_on_explainability_table(self):
    #     TestAIOpenScaleClient.subscription.explainability.print_table_schema()
    #     TestAIOpenScaleClient.subscription.explainability.show_table()
    #     TestAIOpenScaleClient.subscription.explainability.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.explainability.get_table_content()
    #     assert_explainability_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.explainability.get_table_content(format='python')
    #     assert_explainability_python_table_content(python_table_content=python_table_content)

    def test_24_get_metrics(self):
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

    def test_25_disable_monitors(self):
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()
        self.subscription.quality_monitoring.disable()
        # self.subscription.explainability.disable()

        subscription_details = self.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
