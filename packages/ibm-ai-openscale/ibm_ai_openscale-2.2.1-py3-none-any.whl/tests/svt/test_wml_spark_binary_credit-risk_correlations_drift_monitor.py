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
from utils.utils import check_if_binding_exists, get_application_details
from utils.wml_deployments.spark import GermanCreditRisk

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat

from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from ibm_ai_openscale.utils.inject_demo_data import DemoData

from utils.logger import SVTLogger
logger = SVTLogger(__file__).get_logger()


DAYS = 7
RECORDS_PER_DAY = 2880


class TestAIOpenScaleClient(unittest.TestCase):
    hrefs_v2 = None
    log_loss_random = None
    brier_score_loss = None
    application_instance_id = None
    drift_instance_id = None
    data_set_id = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    b_app_uid = None
    x_uid = None
    labels = None
    corr_monitor_instance_id = None
    variables = None
    wml_client = None
    subscription = None
    binding_uid = None
    deployment = None
    scoring_records = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_run_id = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    business_payload_records = 0
    drift_model_name = "drift_detection_model.tar.gz"
    drift_model_path = os.path.join(os.getcwd(), 'artifacts', 'drift_models')
    historical_data_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records')
    data_df = pd.read_csv(
        "./datasets/German_credit_risk/credit_risk_training.csv",
        dtype={'LoanDuration': int, 'LoanAmount': int, 'InstallmentPercent': int, 'CurrentResidenceDuration': int,
               'Age': int, 'ExistingCreditsCount': int, 'Dependents': int})

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()
        cls.deployment = GermanCreditRisk()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        cls.hd = DemoData(cls.aios_credentials, ai_client=cls.ai_client)

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
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()
        logger.info("Asset id: {}, Model id: {}".format(self.model_uid, self.deployment_uid))

    def test_04_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.BINARY_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='predictedLabel',
            probability_column='probability',
            feature_columns=['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount',
                             'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan',
                             'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing',
                             'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'],
            categorical_columns=['CheckingStatus', 'CreditHistory', 'LoanPurpose', 'ExistingSavings',
                                 'EmploymentDuration', 'Sex', 'OthersOnLoan', 'OwnsProperty', 'InstallmentPlans',
                                 'Housing', 'Job', 'Telephone', 'ForeignWorker']
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        logger.info("Subscription details: {}".format(subscription.get_details()))

    def test_05_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

    def test_06_score(self):
        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
             "savings_insurance", 46, "none", "own", 2, "skilled", 1, "none", "yes"],
            ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
             4, "savings_insurance", 36, "none", "free", 2, "management_self-employed", 1, "none", "yes"],
            ["0_to_200", 26, "all_credits_paid_back", "car_new", 863, "less_100", "less_1", 2, "female", "co-applicant",
             2, "real_estate", 38, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 14, "no_credits", "car_new", 2368, "less_100", "1_to_4", 3, "female", "none", 3, "real_estate",
             29, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["0_to_200", 4, "no_credits", "car_new", 250, "less_100", "unemployed", 2, "female", "none", 3,
             "real_estate", 23, "none", "rent", 1, "management_self-employed", 1, "none", "yes"],
            ["no_checking", 17, "credits_paid_to_date", "car_new", 832, "100_to_500", "1_to_4", 2, "male", "none", 2,
             "real_estate", 42, "none", "own", 1, "skilled", 1, "none", "yes"],
            ["no_checking", 33, "outstanding_credit", "appliances", 5696, "unknown", "greater_7", 4, "male",
             "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
            ["0_to_200", 13, "prior_payments_delayed", "retraining", 1375, "100_to_500", "4_to_7", 3, "male", "none", 3,
             "real_estate", 37, "none", "own", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload_scoring = {"fields": fields, "values": values}
        print("Scoring payload: {}".format(payload_scoring))

        TestAIOpenScaleClient.scoring_records = 32
        for i in range(0, int(self.scoring_records/8)):
            self.deployment.score(payload_scoring)

    def test_07_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['prediction', 'probability'])

    def test_08_enable_drift(self):
        self.subscription.drift_monitoring.enable(threshold=0.6, min_records=10, model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription.monitoring.get_details(monitor_uid='drift')
        logger.info('Drift monitor details: {}'.format(drift_monitor_details))

    def test_09_define_business_app(self):
        payload = {
            "name": "Credit Risk Application",
            "description": "Test Business Application",
                "payload_fields": [
                    {
                        "name": "LoanDuration",
                        "type": "number",
                        "description": "Duration of the loan"
                    },
                    {
                        "name": "LoanPurpose",
                        "type": "string",
                        "description": "Purpose of the loan"
                    },
                    {
                        "name": "LoanAmount",
                        "type": "number",
                        "description": "Amount of the loan"
                    },
                    {
                        "name": "InstallmentPercent",
                        "type": "number",
                        "description": "Installment percents"
                    },
                    {
                        "name": "AcceptedPercent",
                        "type": "number"
                    },
                    {
                        "name": "AmountGranted",
                        "type": "number",
                        "description": "Risk percent"
                    },
                    {
                        "name": "Accepted",
                        "type": "number",
                        "description": "Number of loans accepted"
                    }
                ],
            "business_metrics": [
                {
                    "name": "Accepted Credits",
                    "description": "Accepted Credits Daily",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 502,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "Accepted",
                        "aggregation": "sum",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                },
                {
                    "name": "Credit Amount Granted",
                    "description": "Credit Amount Granted Daily",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 1000,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "AmountGranted",
                        "aggregation": "sum",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                }
            ],
            "subscription_ids": [
                TestAIOpenScaleClient.subscription_uid
            ],
        }

        response = request_session.post(
            url=self.hrefs_v2.get_applications_href(),
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json=payload)

        logger.debug("Status code: {}, response: {}".format(response.status_code, response.text))
        self.assertEqual(response.status_code, 202)
        TestAIOpenScaleClient.b_app_uid = response.json()['metadata']['id']
        logger.info("Business app id: {}".format(self.b_app_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.b_app_uid)

    def test_10_get_application_details(self):
        application_details = wait_for_business_app(
            url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.b_app_uid),
            headers=TestAIOpenScaleClient.ai_client._get_headers())

        print(application_details)

        TestAIOpenScaleClient.application_instance_id = application_details['entity']['business_metrics_monitor_instance_id']
        TestAIOpenScaleClient.corr_monitor_instance_id = application_details['entity']['correlation_monitor_instance_id']

    def test_11_list_monitors_instances(self):
        self.ai_client.data_mart.monitors.list()
        response = request_session.get(
            url=self.hrefs_v2.get_monitor_instances_href(),
            headers=self.ai_client._get_headers()
        )
        self.assertEquals(response.status_code, 200, msg="Invalid response: {}".format(response.text))
        instances = response.json()['monitor_instances']

        for instance in instances:
            if instance['entity']['monitor_definition_id'] == 'drift' and instance['entity']['target']['target_type'] == 'subscription' and instance['entity']['target']['target_id'] == self.subscription_uid:
                TestAIOpenScaleClient.drift_instance_id = instance['metadata']['id']

        self.assertIsNotNone(TestAIOpenScaleClient.application_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.corr_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.drift_instance_id)
        print('application_instance_id', self.application_instance_id)
        print('corr_monitor_instance_id', self.corr_monitor_instance_id)
        print('drift_instance_id', self.drift_instance_id)

    def test_12_load_historical_bkpis(self):
        self.hd.load_historical_kpi_measurements(
            file_path=TestAIOpenScaleClient.historical_data_path,
            monitor_instance_id=self.application_instance_id,
        )

    def test_13_get_historical_kpi(self):
        current_time = datetime.utcnow().isoformat() + 'Z'
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        query = "?start={}&end={}&limit={}".format(start_time, current_time, 1000)
        metrics_url = self.hrefs_v2.get_measurements_href(self.application_instance_id) + query

        wait_for_measurements(
            measurements_url=metrics_url,
            no_measurements=7,
            headers=self.ai_client._get_headers()
        )

    def test_14_store_drift_measurements(self):
        self.hd.load_historical_drift_measurements(
            file_path=TestAIOpenScaleClient.historical_data_path,
            monitor_instance_id=self.drift_instance_id,
            business_application_id=self.b_app_uid)

    def test_15_get_drift_measurements(self):
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        current_time = datetime.utcnow().isoformat() + 'Z'
        query = "?start={}&end={}".format(start_time, current_time)
        metrics_url = self.hrefs_v2.get_measurements_href(self.drift_instance_id) + query

        measurements = wait_for_measurements(
            measurements_url=metrics_url,
            no_measurements=7,
            headers=self.ai_client._get_headers()
        )

    def test_16_validate_correlation_prerequisites(self):
        filter_statement = "business_application_id:eq:{}&business_metric_id:eq:{}&transaction_batch_id:exists".format(
            TestAIOpenScaleClient.b_app_uid,
            'credit_amount_granted')
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        current_time = datetime.utcnow().isoformat() + 'Z'
        query = "?start={}&end={}&filter={}".format(start_time, current_time, filter_statement)
        metrics_url = self.hrefs_v2.get_measurements_href(self.drift_instance_id) + query

        response = request_session.get(
            url=metrics_url,
            headers=self.ai_client._get_headers()
        )
        self.assertEquals(200, response.status_code, msg="Invalid response: {}".format(response.text))
        self.assertGreaterEqual(len(response.json()['measurements']), 7, msg="Requirement not met for {}. No measurements: {}".format('credit_amount_granted', len(response.json()['measurements'])))

        filter_statement = "business_application_id:eq:{}&business_metric_id:eq:{}&transaction_batch_id:exists".format(
            TestAIOpenScaleClient.b_app_uid,
            'accepted_credits')
        query = "?start={}&end={}&filter={}".format(start_time, current_time, filter_statement)
        metrics_url = self.hrefs_v2.get_measurements_href(self.drift_instance_id) + query

        response = request_session.get(
            url=metrics_url,
            headers=self.ai_client._get_headers()
        )
        self.assertEquals(200, response.status_code, msg="Invalid response: {}".format(response.text))
        self.assertGreaterEqual(len(response.json()['measurements']), 7, msg="Requirement not met for {}. No measurements: {}".format('accepted_credits', len(response.json()['measurements'])))

    def test_17_run_correlation_monitor(self):
        payload = {
            "triggered_by": "user",
            "parameters": {
                "max_number_of_days": "1000"
            },
            "business_metric_context": {
                "business_application_id": TestAIOpenScaleClient.b_app_uid,
                "metric_id": "",
                "transaction_data_set_id": "",
                "transaction_batch_id": ""
            }
        }

        response = request_session.post(
            url=self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id),
            json=payload,
            headers=TestAIOpenScaleClient.ai_client._get_headers())

        logger.debug("Status code: {}, response: {}".format(response.status_code, response.text))
        self.assertEqual(response.status_code, 201)
        TestAIOpenScaleClient.correlation_run_id = response.json()['metadata']['id']

    def test_18_wait_for_correlation_finish(self):
        run_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id)
        final_run_details = wait_for_monitor_instance(run_url, run_id=self.correlation_run_id, headers=self.ai_client._get_headers())
        self.assertIsNot(final_run_details['entity']['status']['state'], 'error',
                         msg="Error during computing correlations. Run details: {}".format(final_run_details))

    def test_19_check_correlations_metrics(self):
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        current_time = datetime.utcnow().isoformat() + 'Z'
        query = "?start={}&end={}".format(start_time, current_time)
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.corr_monitor_instance_id) + query

        measurements = wait_for_measurements(
            measurements_url=url,
            no_measurements=1,
            headers=self.ai_client._get_headers()
        )

        print(measurements)

        self.assertTrue('significant_coefficients' in str(measurements))

        corr_metrics = measurements['measurements'][0]['entity']['values'][0]['metrics']
        self.assertGreater([metric['value'] for metric in corr_metrics if metric['id'] == 'significant_coefficients'][0], 0, msg="No significant coefficients")

    def test_20_update_business_application(self):
        prev_app_details = get_application_details(self.hrefs_v2, self.b_app_uid, self.ai_client._get_headers())
        no_business_metrics = len(prev_app_details['entity']['business_metrics'])
        self.assertGreater(no_business_metrics, 0, msg="No business metrics in application details")

        payload = [
                      {
                        "op": "remove",
                        "path": "/business_metrics/0"
                      }
                    ]
        response = request_session.patch(
            url=self.hrefs_v2.get_application_details_href(self.b_app_uid),
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json=payload)
        logger.debug("Status code: {}, response: {}".format(response.status_code, response.text))
        self.assertEqual(200, response.status_code)
        app_details = get_application_details(self.hrefs_v2, self.b_app_uid, self.ai_client._get_headers())

        self.assertGreater(no_business_metrics, len(app_details['entity']['business_metrics']),
                           msg="Business metric wasn't delated, number of business metrics: \n - before patch: {} \n - after patch: {}".format(no_business_metrics, len(app_details['entity']['business_metrics'])))

    def test_21_delete_business_application(self):
        response = request_session.delete(
            url=self.hrefs_v2.get_application_details_href(self.b_app_uid),
            headers=TestAIOpenScaleClient.ai_client._get_headers())
        logger.debug("Status code: {}, response: {}".format(response.status_code, response.text))
        self.assertEqual(202, response.status_code)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
