# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pandas as pd
from datetime import datetime, timedelta

from utils.assertions import *
from utils.cleanup import *
from utils.waits import *
from utils.wml_deployments.spark import GermanCreditRisk
from utils.utils import check_if_binding_exists
from utils.request_handler import request_session

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *

from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from ibm_ai_openscale.utils.inject_demo_data import DemoData
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType


DAYS = 7
RECORDS_PER_DAY = 72


class TestAIOpenScaleClient(unittest.TestCase):
    hrefs_v2 = None
    log_loss_random = None
    brier_score_loss = None
    business_metrics_monitor_instance_id = None
    drift_instance_id = None
    business_data_set_id = None
    transaction_batches_data_set_id = None
    scoring_payload_data_set_id = None
    ai_client = None
    deployment_uid = None
    assurance_run_id = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    business_application_id = None
    x_uid = None
    labels = None
    corr_monitor_instance_id = None
    variables = None
    wml_client = None
    subscription = None
    binding_uid = None
    deployment = None
    correlation_run_id = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    business_payload_records = 0
    business_metrics_ids = None
    correlation_monitor_run_id = None
    business_metrics_monitor_run_id = None

    query_measurements = '?start=2018-11-06T09:22:48.708970Z&end={}Z'.format((datetime.utcnow()+timedelta(weeks=1)).isoformat())
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

    def test_04_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.BINARY_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='predictedLabel',
            probability_column='probability',
            transaction_id_column='transaction_id',
            feature_columns=['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount',
                             'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan',
                             'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing',
                             'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'],
            categorical_columns=['CheckingStatus', 'CreditHistory', 'LoanPurpose', 'ExistingSavings',
                                 'EmploymentDuration', 'Sex', 'OthersOnLoan', 'OwnsProperty', 'InstallmentPlans',
                                 'Housing', 'Job', 'Telephone', 'ForeignWorker'],
        ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid

    def test_05_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        print("Subscription details: {}".format(self.subscription.get_details()))

    def test_06_payload_logging_update(self):
        self.subscription.payload_logging.enable(dynamic_schema_update=True)
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_07_load_historical_scoring_payload(self):
        self.hd.load_historical_scoring_payload(
            TestAIOpenScaleClient.subscription,
            TestAIOpenScaleClient.deployment_uid,
            TestAIOpenScaleClient.historical_data_path,
            day_template="history_correlation_payloads_short_72_recs_{}.json")

    def test_08_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=RECORDS_PER_DAY*DAYS)
        records_no = TestAIOpenScaleClient.subscription.payload_logging.get_records_count()
        print("Rows {} stored in payload table".format(records_no))

        TestAIOpenScaleClient.subscription.payload_logging.show_table(limit=5)
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()

    def test_09_get_payload_dataset(self):
        response = request_session.get(
            self.hrefs_v2.get_data_sets_href(),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        self.assertEqual(response.status_code, 200, msg="Unable to get datasets: {}".format(response.text))

        payload_data_set = None
        for dataset in response.json()['data_sets']:
            if dataset['entity']['type'] == 'payload_logging' and dataset['entity']['target']['target_type'] == 'subscription' and dataset['entity']['target']['target_id'] == self.subscription_uid:
                payload_data_set = dataset

        self.assertIsNotNone(payload_data_set)

        self.assertEqual(payload_data_set['entity']['schema_update_mode'], 'auto', msg="Payload auto update is not set. Details {}".format(payload_data_set))
        self.assertEqual(payload_data_set['entity']['status']['state'], 'active', msg="Payload dataset status is not active. Details {}".format(payload_data_set))

        TestAIOpenScaleClient.scoring_payload_data_set_id = payload_data_set['metadata']['id']

        print("Payload dataset id: {}".format(self.scoring_payload_data_set_id))
        print("Payload dataset location: {}".format(payload_data_set['entity']['location']))

    def test_10_check_payload_dataset_schema(self):
        response = request_session.get(
            self.hrefs_v2.get_data_set_details_href(TestAIOpenScaleClient.scoring_payload_data_set_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        self.assertEqual(response.status_code, 200, "Unable to get payload dataset details: {}".format(response.text))

        dataset_details = response.json()
        self.assertIn('transaction_id_key', str(dataset_details), msg="Transaction_id_key is not set in payload data set. Details: {}".format(dataset_details))
        print("Payload data schema:\n{}".format(dataset_details['entity']['data_schema']))

    def test_11_get_payload_dataset_records(self):
        response = requests.get(
            url="{}/records".format(self.hrefs_v2.get_data_set_details_href(TestAIOpenScaleClient.scoring_payload_data_set_id)),
            headers=TestAIOpenScaleClient.ai_client._get_headers(), verify=False
        )
        self.assertEqual(response.status_code, 200, msg="Unable to get datasets records: {}".format(response.text))

        dataset_records = response.json()['records']
        print("Dataset records number: {}".format(len(dataset_records)))
        print("Dataset sample record:\n{}".format(dataset_records[0]))

    def test_12_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))
        self.assertIn('transaction_id_key', str(subscription_details), msg="transaction_id_key not found set in subscription details")

    def test_13_enable_drift(self):
        self.subscription.drift_monitoring.enable(threshold=0.6, min_records=10, model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_14_check_drift_monitor_instance_v2(self):
        response = request_session.get(
            url=self.hrefs_v2.get_monitor_instances_href(),
            headers=self.ai_client._get_headers()
        )
        self.assertEqual(200, response.status_code, msg="Unable to get monitor instance: {}".format(response.text))

        drift_monitor_instance = None
        for monitor_instance in response.json()['monitor_instances']:
            if monitor_instance['entity']['monitor_definition_id'] == 'drift' and monitor_instance['entity']['target']['target_type'] == 'subscription' and monitor_instance['entity']['target']['target_id'] == self.subscription_uid:
                drift_monitor_instance = monitor_instance

        self.assertIsNotNone(drift_monitor_instance, msg="Drift monitor instance not found. Details: {}".format(response.json()))
        print("Drift instance details:\n{}".format(drift_monitor_instance))

        TestAIOpenScaleClient.drift_instance_id = drift_monitor_instance['metadata']['id']
        print("Drift monitor instance id: {}".format(self.drift_instance_id))

    def test_15_define_business_app(self):
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
                            "default": 52,
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
                            "default": 130000,
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
            ]
        }

        response = request_session.post(
            url=self.hrefs_v2.get_applications_href(),
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json=payload
        )

        self.assertEqual(response.status_code, 202, msg="Unable to create business application. Reason: {}".format(response.text))
        TestAIOpenScaleClient.business_application_id = response.json()['metadata']['id']
        TestAIOpenScaleClient.business_metrics_ids = [b_metric['id'] for b_metric in response.json()['entity']['business_metrics']]
        self.assertIsNotNone(TestAIOpenScaleClient.business_application_id)
        print("Business application id: {}".format(self.business_application_id))

    def test_16_get_application_details(self):
        bapp_details = wait_for_business_app(
            url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.business_application_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        print("Business app details: {}".format(bapp_details))

        self.assertEqual(bapp_details['entity']['status']['state'], 'active', msg="Business application is not active, reason: {}".format(bapp_details))

        TestAIOpenScaleClient.business_metrics_monitor_instance_id = bapp_details['entity']['business_metrics_monitor_instance_id']
        TestAIOpenScaleClient.corr_monitor_instance_id = bapp_details['entity']['correlation_monitor_instance_id']
        TestAIOpenScaleClient.business_data_set_id = bapp_details['entity']['business_payload_data_set_id']

    def test_17_check_monitors_instances(self):
        self.ai_client.data_mart.monitors.list()

        self.assertIsNotNone(TestAIOpenScaleClient.business_metrics_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.corr_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.drift_instance_id)
        print('application_instance_id', self.business_metrics_monitor_instance_id)
        print('corr_monitor_instance_id', self.corr_monitor_instance_id)
        print('drift_instance_id', self.drift_instance_id)

    def test_18_get_business_payload_data_set_details(self):
        dataset_details = wait_for_dataset(
            dataset_url=self.hrefs_v2.get_data_set_details_href(self.business_data_set_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        print("Dataset details: {}".format(dataset_details))

    def test_19_insert_business_payload(self):
        self.hd.load_historical_business_payload(
            file_path=TestAIOpenScaleClient.historical_data_path,
            data_set_id=TestAIOpenScaleClient.business_data_set_id,
            file_name="history_business_payloads_short_504_recs_week.csv"
        )
        TestAIOpenScaleClient.business_payload_records = RECORDS_PER_DAY*DAYS

    def test_20_stats_on_business_payload_data(self):
        business_records_no = wait_for_records_in_data_set(
            url_get_data_set_records=self.hrefs_v2.get_data_set_records_href(TestAIOpenScaleClient.business_data_set_id),
            headers=self.ai_client._get_headers(),
            data_set_records=self.business_payload_records,
            waiting_timeout=270
        )
        print(business_records_no)
        self.assertEqual(self.business_payload_records, business_records_no)

    def test_21_run_business_application(self):
        run_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.business_metrics_monitor_instance_id)
        payload = {
              "triggered_by": "user",
              "parameters": {
                "correlation_monitor": {
                  "trigger_on_completion": True,
                  "parameters": {
                    "max_number_of_days": 1000}}}}

        response = requests.post(
            url=run_url,
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json=payload, verify=False
        )
        self.assertEqual(response.status_code, 201, "Run business application failed: {}".format(response.text))

        TestAIOpenScaleClient.business_metrics_monitor_run_id = response.json()['metadata']['id']
        final_run_details = wait_for_monitor_instance(
            run_url,
            run_id=TestAIOpenScaleClient.business_metrics_monitor_run_id,
            headers=self.ai_client._get_headers())
        self.assertIsNot(
            final_run_details['entity']['status']['state'],
            'failure',
            msg="Error during computing BKPIs. Run details: {}".format(final_run_details))

    def test_22_get_bkpis(self):
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.business_metrics_monitor_instance_id) + self.query_measurements
        wait_for_measurements(
            measurements_url=url,
            no_measurements=7,
            headers=self.ai_client._get_headers()
        )

    def test_23_get_drift_measurements(self):
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.drift_instance_id) + self.query_measurements

        measurements = wait_for_measurements(
            measurements_url=url,
            no_measurements=7,
            headers=self.ai_client._get_headers()
        )
        self.assertGreaterEqual(len(measurements['measurements']), 7, msg="Not enough drift measurements. {}".format(measurements))
        print("Drift measurements: {}".format(measurements))


    def test_24_check_correlations_metrics(self):
        start_time = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'
        current_time = datetime.utcnow().isoformat() + 'Z'
        query = "?start={}&end={}".format(start_time, current_time)
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.corr_monitor_instance_id) + query

        measurements = wait_for_measurements(
            measurements_url=url,
            no_measurements=1,
            headers=self.ai_client._get_headers()
        )
        print("Correlation measurements:\n", measurements)

        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.corr_monitor_instance_id) + self.query_measurements
        response = requests.get(url=url, headers=self.ai_client._get_headers(), verify=False)
        self.assertEqual(response.status_code, 200, msg="Unable to get correlation measurements: {}".format(response.text))
        self.assertTrue('significant_coefficients' in str(response.json()), msg="Significant correlation not found: {}".format(response.json()))

        corr_metrics = response.json()['measurements'][0]['entity']['values'][0]['metrics']
        self.assertGreater([metric['value'] for metric in corr_metrics if metric['id'] == 'significant_coefficients'][0], 0, msg="No significant coefficients")

    def test_29_delete_business_application(self):
        response = request_session.delete(
            url=self.hrefs_v2.get_application_details_href(self.business_application_id),
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            json={})
        print("Status code: {}, response: {}".format(response.status_code, response.text))
        self.assertEqual(202, response.status_code)
        self.subscription.drift_monitoring.disable()

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
