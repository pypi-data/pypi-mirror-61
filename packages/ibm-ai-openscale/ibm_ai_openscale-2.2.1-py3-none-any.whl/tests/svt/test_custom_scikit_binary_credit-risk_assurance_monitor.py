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
from ibm_ai_openscale.utils.inject_demo_data import DemoData
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2

DAYS = 7
RECORDS_PER_DAY = 2880


class TestAIOpenScaleClient(unittest.TestCase):
    scoring_payload_data_set_id = None
    run_id = None
    hrefs_v2 = None
    log_loss_random = None
    business_data_set_id = None
    brier_score_loss = None
    corr_run_id = None
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
    correlation_run_id = None
    labels = None
    business_payload_records = None
    assurance_monitor_instance_id = None
    variables = None
    wml_client = None
    subscription = None
    binding_uid = None
    corr_monitor_instance_id = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    run_time = None
    drift_model_name = "drift_detection_model.tar.gz"
    drift_model_path = os.path.join(os.getcwd(), 'artifacts', 'drift_models')
    historical_data_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records')
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
                  ["no_checking",13,"credits_paid_to_date","car_new",1343,"100_to_500","1_to_4",2,"female","none",3,"savings_insurance",46,"none","own",2,"skilled",1,"none","yes"],
                  ["no_checking",24,"prior_payments_delayed","furniture",4567,"500_to_1000","1_to_4",4,"male","none",4,"savings_insurance",36,"none","free",2,"management_self-employed",1,"none","yes"],
                  ["0_to_200",26,"all_credits_paid_back","car_new",863,"less_100","less_1",2,"female","co-applicant",2,"real_estate",38,"none","own",1,"skilled",1,"none","yes"],
                  ["0_to_200",14,"no_credits","car_new",2368,"less_100","1_to_4",3,"female","none",3,"real_estate",29,"none","own",1,"skilled",1,"none","yes"],
                  ["0_to_200",4,"no_credits","car_new",250,"less_100","unemployed",2,"female","none",3,"real_estate",23,"none","rent",1,"management_self-employed",1,"none","yes"],
                  ["no_checking",17,"credits_paid_to_date","car_new",832,"100_to_500","1_to_4",2,"male","none",2,"real_estate",42,"none","own",1,"skilled",1,"none","yes"],
                  ["no_checking",33,"outstanding_credit","appliances",5696,"unknown","greater_7",4,"male","co-applicant",4,"unknown",54,"none","free",2,"skilled",1,"yes","yes"],
                  ["0_to_200",13,"prior_payments_delayed","retraining",1375,"100_to_500","4_to_7",3,"male","none",3,"real_estate",37,"none","own",2,"management_self-employed",1,"none","yes"],
                  ["no_checking", 63, "outstanding_credit", "appliances", 15696, "unknown", "greater_7", 4, "male", "co-applicant", 4, "unknown", 54, "none", "free", 2, "skilled", 1, "yes", "yes"],
                  ["0_to_200", 23, "prior_payments_delayed", "appliances", 13075, "100_to_500", "4_to_7", 3, "female", "none", 3, "real_estate", 47, "none", "own", 2, "management_self-employed", 1, "yes", "yes"]
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
        cls.database_credentials = get_database_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)
        cls.hd = DemoData(cls.aios_credentials, ai_client=cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
        print(self.ai_client.data_mart.get_details())

    def test_02_bind_custom(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("My Custom deployment", CustomMachineLearningInstance(self.credentials))
        print("Binding uid: {}".format(self.binding_uid))
        self.assertIsNotNone(self.binding_uid)

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_04_get_deployments(self):
        print('Available deployments: {}'.format(self.ai_client.data_mart.bindings.get_asset_deployment_details()))
        self.ai_client.data_mart.bindings.list_assets()
        self.ai_client.data_mart.bindings.get_asset_details()

    def test_05_subscribe_custom(self):
        subscription = self.ai_client.data_mart.subscriptions.add(
            CustomMachineLearningAsset(
                source_uid='credit',
                problem_type=ProblemType.BINARY_CLASSIFICATION,
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
        print("Subscription id: {}".format(self.subscription_uid))
        self.assertIsNotNone(self.subscription_uid)

    def test_06_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

    def test_07_score_model_and_log_payload(self):
        request, response, response_time = self.score(self.subscription.get_details())
        print('response: ' + str(response))
        records_list = [PayloadRecord(request=request, response=response, response_time=response_time)]

        self.subscription.payload_logging.store(records=records_list)

        time.sleep(30)

    def test_08_a_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=10)
        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content,
                                                    scoring_records=10)

        print('subscription details', TestAIOpenScaleClient.subscription.get_details())

    def test_08_b_get_payload_dataset(self):
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

    def test_09_define_business_app(self):
        payload = {
            "name": "Credit Risk Application ololo",
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

        response = requests.post(url=self.hrefs_v2.get_applications_href(),
                                 headers=TestAIOpenScaleClient.ai_client._get_headers(), json=payload, verify=False)
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 202)
        TestAIOpenScaleClient.b_app_uid = response.json()['metadata']['id']
        self.assertIsNotNone(TestAIOpenScaleClient.b_app_uid)

    def test_10_get_application_details(self):
        bapp_details = wait_for_business_app(
            url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.b_app_uid),
            headers=TestAIOpenScaleClient.ai_client._get_headers()
        )
        print(bapp_details)

        TestAIOpenScaleClient.application_instance_id = bapp_details['entity']['business_metrics_monitor_instance_id']
        TestAIOpenScaleClient.corr_monitor_instance_id = bapp_details['entity']['correlation_monitor_instance_id']
        TestAIOpenScaleClient.business_data_set_id = bapp_details['entity']['business_payload_data_set_id']

    def test_11_enable_assurance_monitor(self):
        print('heartbeat')

        h_url = self.ai_client._service_credentials['url'] + '/openscale/v2/assurance/heartbeat'
        response = requests.get(url=h_url)
        print(response.status_code, response.text)
        self.assertTrue(response.status_code == 200)

        payload = {
            "data_mart_id": self.ai_client._service_credentials['instance_guid'],
            "monitor_definition_id": "assurance",
            "target": {
                "target_type": "subscription",
                "target_id": TestAIOpenScaleClient.subscription_uid
            },
            "parameters": {
                "max_number_of_records": 100,
            }
        }

        response = requests.post(
            url=self.hrefs_v2.get_monitor_instances_href(),
            json=payload,
            headers=self.ai_client._get_headers()
        )

        print(payload)
        print(response.status_code, response.text)
        self.assertTrue(response.status_code == 202)
        TestAIOpenScaleClient.assurance_monitor_instance_id = response.json()['metadata']['id']
        self.assertIsNotNone(TestAIOpenScaleClient.assurance_monitor_instance_id)

        print('transaction_data_set_id = "' + TestAIOpenScaleClient.scoring_payload_data_set_id + '"')
        print('business_application_id = "' + TestAIOpenScaleClient.application_instance_id + '"')
        print('monitor_instance_id = "' + TestAIOpenScaleClient.assurance_monitor_instance_id + '"')

    def test_12_list_monitors_definitions(self):
        print('definitions:')
        self.ai_client.data_mart.monitors.list()

        print('instances')
        response = requests.get(url=self.hrefs_v2.get_monitor_instances_href(), headers=self.ai_client._get_headers(), verify=False)
        print(response.json())
        instances = response.json()['monitor_instances']

        for instance in instances:
            if instance['entity']['monitor_definition_id'] == 'assurance' and instance['entity']['target']['target_type'] == 'subscription' and instance['entity']['target']['target_id'] == self.subscription_uid:
                self.assertTrue(instance['metadata']['id'] == TestAIOpenScaleClient.assurance_monitor_instance_id)

        print('outcomes_stats_monitor_id', self.assurance_monitor_instance_id)

    def test_13_get_monitor_definition(self):
        details = self.ai_client.data_mart.monitors.get_details(monitor_uid='assurance')
        print(details)

    def test_14_run_assurance_monitor(self):
        TestAIOpenScaleClient.run_time = datetime.utcnow().isoformat() + 'Z'

        payload = {
            "triggered_by": "user",
            "parameters": {
                "max_number_of_records": "1000"
            }
        }

        url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.assurance_monitor_instance_id)
        print(url)

        response = requests.post(
            url=url,
            json=payload,
            headers=TestAIOpenScaleClient.ai_client._get_headers(),
            verify=False
        )
        print(response.status_code, response.text)
        self.assertEqual(response.status_code, 201)
        TestAIOpenScaleClient.run_id = response.json()['metadata']['id']

    def test_15_wait_for_assurance_monitor_finish(self):
        start_time = time.time()
        elapsed_time = 0
        status = ""

        while status != 'finished' and status != "error" and elapsed_time < 120:
            response = requests.get(
                url=self.hrefs_v2.get_monitor_instance_run_details_href(
                    TestAIOpenScaleClient.assurance_monitor_instance_id,
                    TestAIOpenScaleClient.run_id),
                headers=TestAIOpenScaleClient.ai_client._get_headers(),
                verify=False
            )
            status = response.json()['entity']['status']['state']
            elapsed_time = time.time() - start_time

        print(response.json())
        self.assertEqual(status, 'finished', msg="Assurance computation failed. Reason: {}".format(response.json()))

    def test_16_check_assurance_metrics(self):
        TestAIOpenScaleClient.subscription.monitoring.show_table('assurance')
        query = '?start={}&end={}'.format(TestAIOpenScaleClient.run_time, datetime.utcnow().isoformat() + 'Z')
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.assurance_monitor_instance_id) + query
        print(url)

        response = requests.get(url=url, headers=self.ai_client._get_headers(), verify=False)

        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('uncertainty' in str(response.json()))

        measurement_id = response.json()['measurements'][0]['metadata']['id']
        print('measurement_id', measurement_id)

        measurement_url = self.hrefs_v2.get_measurement_details_href(TestAIOpenScaleClient.assurance_monitor_instance_id, measurement_id)
        response = requests.get(url=measurement_url, headers=self.ai_client._get_headers(), verify=False)
        print(measurement_url, 'measurement_details', response.json())
        self.assertTrue('min' in str(response.json()))

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
