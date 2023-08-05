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
from utils.request_handler import request_session

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from ibm_ai_openscale.utils.inject_historical_data import load_historical_kpi_measurement, \
    load_historical_drift_measurement


DAYS = 7


class TestAIOpenScaleClient(unittest.TestCase):
    corr_run_id = None
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

    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    drift_model_name = "drift_detection_model.tar.gz"
    drift_model_path = os.path.join(os.getcwd(), 'artifacts', 'drift_models')
    data_df = pd.read_csv(
        "./datasets/German_credit_risk/credit_risk_training.csv",
        dtype={'LoanDuration': int, 'LoanAmount': int, 'InstallmentPercent': int, 'CurrentResidenceDuration': int,
               'Age': int, 'ExistingCreditsCount': int, 'Dependents': int})

    test_uid = str(uuid.uuid4())

    def score(self, subscription_details):
        fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
                  "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
                  "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
                  "Telephone", "ForeignWorker"]
        values = [
            ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
             "savings_insurance", 25, "none", "own", 2, "skilled", 1, "none", "yes"],
            ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
             4, "savings_insurance", 60, "none", "free", 2, "management_self-employed", 1, "none", "yes"]
        ]

        payload = {"fields": fields, "values": values}
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer xxx'}
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

        response = requests.post(scoring_url, json=payload, headers=header)

        return payload, response.json(), 25

    @classmethod
    def setUpClass(cls):
        cls.credentials = get_custom_credentials()

        try:
            requests.get(url="{}/v1/deployments".format(cls.credentials['url']), timeout=10)
        except:
            raise unittest.SkipTest("Custom app is not available.")

        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_custom(self):
        TestAIOpenScaleClient.binding_uid = check_if_binding_exists(
            self.ai_client,
            self.credentials,
            type='custom_machine_learning')

        if TestAIOpenScaleClient.binding_uid is None:
            print("Binding does not exist. Creating a new one.")
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add(
                "Custom ML engine",
                CustomMachineLearningInstance(self.credentials))

        print("Binding uid: {}".format(self.binding_uid))
        self.assertIsNotNone(self.binding_uid)

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_04_get_deployments(self):
        print('Available deployments: {}'.format(self.ai_client.data_mart.bindings.get_asset_deployment_details(binding_uid=self.binding_uid)))
        print("Asset details: {}".format(self.ai_client.data_mart.bindings.get_asset_details(binding_uid=self.binding_uid)))

    def test_05_subscribe_custom(self):
        subscription = self.ai_client.data_mart.subscriptions.add(
            CustomMachineLearningAsset(
                source_uid='credit',
                label_column='Risk',
                prediction_column='prediction',
                probability_column='probability',
                feature_columns=['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount',
                                 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan',
                                 'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing',
                                 'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'],
                categorical_columns=['CheckingStatus', 'CreditHistory', 'LoanPurpose', 'ExistingSavings',
                                     'EmploymentDuration', 'Sex', 'OthersOnLoan', 'OwnsProperty', 'InstallmentPlans',
                                     'Housing', 'Job', 'Telephone', 'ForeignWorker'],
                binding_uid=self.binding_uid))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print('Subscription details: ', subscription.get_details())
        self.assertIsNotNone(self.subscription_uid)

    def test_06_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

    def test_07_score_model_and_log_payload(self):
        request, response, response_time = self.score(self.subscription.get_details())

        records_list = []
        for i in range(0, 5):
            records_list.append(PayloadRecord(request=request, response=response, response_time=response_time))

        self.subscription.payload_logging.store(records=records_list)

    def test_08_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=10)
        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=10)

    def test_09_enable_drift(self):
        self.subscription.drift_monitoring.enable(threshold=0.6, min_records=10, model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_10_define_business_app(self):
        payload = {
            "name": "Credit Risk Application Custom",
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
                    "name": "RiskPercent",
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
                    "description": "string",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 12100,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "Accepted",
                        "aggregation": "avg",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                },
                {
                    "name": "Credit Amount Granted",
                    "description": "string",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 41000000,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "LoanAmount",
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

        self.assertEqual(response.status_code, 202, msg="Business app creation failed. Reason: {}".format(response.text))
        TestAIOpenScaleClient.b_app_uid = response.json()['metadata']['id']
        self.assertIsNotNone(TestAIOpenScaleClient.b_app_uid)

    def test_11_get_application_details(self):
        bapp_details = wait_for_business_app(
            url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.b_app_uid),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        print(bapp_details)

        TestAIOpenScaleClient.application_instance_id = bapp_details['entity']['business_metrics_monitor_instance_id']
        TestAIOpenScaleClient.corr_monitor_instance_id = bapp_details['entity']['correlation_monitor_instance_id']

    def test_12_list_monitors_instances(self):
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

    def test_13_load_historical_bkpis(self):
        file_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records', 'history_kpi.json')

        load_historical_kpi_measurement(
            ai_client=self.ai_client,
            file_path=file_path,
            aios_credentials=self.aios_credentials,
            monitor_instance_id=self.application_instance_id,
            business_application_id=self.b_app_uid,
            days=DAYS
        )

        load_historical_kpi_measurement(
            ai_client=self.ai_client,
            file_path=file_path,
            aios_credentials=self.aios_credentials,
            monitor_instance_id=self.application_instance_id,
            business_application_id=self.b_app_uid,
            days=2,
            batch_id_start=200
        )

        load_historical_kpi_measurement(
            ai_client=self.ai_client,
            file_path=file_path,
            aios_credentials=self.aios_credentials,
            monitor_instance_id=self.application_instance_id,
            business_application_id=self.b_app_uid,
            days=2,
            batch_id_start=300,
            ignore_metrics=['number_accepted']
        )

    def test_14_get_historical_kpi(self):
        current_time = datetime.utcnow().isoformat() + 'Z'
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        query = "?start={}&end={}&limit={}".format(start_time, current_time, 1000)
        metrics_url = self.hrefs_v2.get_measurements_href(self.application_instance_id) + query

        wait_for_measurements(
            measurements_url=metrics_url,
            no_measurements=260,
            headers=self.ai_client._get_headers()
        )

    def test_15_get_business_payload_data_set_details(self):
        response = request_session.get(
            url=self.hrefs_v2.get_data_sets_href(),
            headers=self.ai_client._get_headers()
        )
        self.assertEqual(response.status_code, 200, msg="Invalid response: {}".format(response.text))

        data_sets = response.json()['data_sets']
        TestAIOpenScaleClient.data_set_id = [ds['metadata']['id'] for ds in data_sets if ds['entity']['type']=='business_payload'][0]
        print(TestAIOpenScaleClient.data_set_id)
        self.assertIsNotNone(TestAIOpenScaleClient.data_set_id)

    def test_16_store_drift_measurements(self):
        file_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records', 'history_drift.json')

        load_historical_drift_measurement(
            ai_client=self.ai_client,
            file_path=file_path,
            aios_credentials=self.aios_credentials,
            monitor_instance_id=self.drift_instance_id,
            business_application_id=self.b_app_uid,
            days=DAYS
            )

    def test_17_get_drift_measurements(self):
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        current_time = datetime.utcnow().isoformat() + 'Z'
        query = "?start={}&end={}".format(start_time, current_time)

        metrics_url = self.hrefs_v2.get_measurements_href(self.drift_instance_id) + query

        measurements = wait_for_measurements(
            measurements_url=metrics_url,
            no_measurements=50,
            headers=self.ai_client._get_headers()
        )
        print(measurements)

    def test_18_get_data_sets(self):
        response = request_session.get(
            url=self.hrefs_v2.get_data_sets_href(),
            headers=self.ai_client._get_headers()
        )
        self.assertEquals(200, response.status_code, msg="Invalid response: {}".format(response.text))
        data_sets = response.json()['data_sets']

    def test_19_validate_correlation_prerequisites(self):
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
        self.assertGreaterEqual(len(response.json()['measurements']), 7)

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
        self.assertGreaterEqual(len(response.json()['measurements']), 7)



    def test_21_run_correlation_monitor(self):
        payload = {
            "triggered_by": "user",
            "parameters": {
                "max_number_of_days": "1000"
            },
            "business_metric_context": {
                "business_application_id": TestAIOpenScaleClient.b_app_uid,
                "metric_id": "avg_revenue",
                "transaction_data_set_id": "",
                "transaction_batch_id": ""
            }
        }
        response = request_session.post(
            url=self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id),
            json=payload,
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        self.assertEqual(response.status_code, 201, msg="Invalid response: {}".format(response.text))
        TestAIOpenScaleClient.corr_run_id = response.json()['metadata']['id']

    def test_22_wait_for_correlation_finish(self):
        wait_for_monitor_instance(
            run_url=self.hrefs_v2.get_monitor_instance_run_details_href(TestAIOpenScaleClient.corr_monitor_instance_id, TestAIOpenScaleClient.corr_run_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )

    def test_23_check_correlations_metrics(self):
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

        measurement_id = measurements['measurements'][0]['metadata']['id']
        print('measurement_id', measurement_id)

        measurement_url = self.hrefs_v2.get_measurement_details_href(TestAIOpenScaleClient.corr_monitor_instance_id, measurement_id)
        response = request_session.get(
            url=measurement_url,
            headers=self.ai_client._get_headers()
        )
        print(measurement_url, 'measurement_details', response.json())
        self.assertTrue('data_drift' in str(response.json()))

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
