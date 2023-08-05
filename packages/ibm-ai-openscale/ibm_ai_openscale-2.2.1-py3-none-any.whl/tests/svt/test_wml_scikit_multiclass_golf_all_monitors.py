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
from utils.wml_deployments.scikit import MulticlassGolf

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
    deployment = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None
    scoring_records = 15
    feedback_records = 10
    transaction_id = None
    data_df = None
    final_run_details = None
    assurance_monitor_instance_id = None
    assurance_run_time = None

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

        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)

    def test_00_get_model_and_deployment_ids(self):
        TestAIOpenScaleClient.deployment = MulticlassGolf()
        TestAIOpenScaleClient.model_uid = self.deployment.get_asset_id()
        TestAIOpenScaleClient.deployment_uid = self.deployment.get_deployment_id()

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

    def test_03_subscribe(self):
        label_column = ['total_label']
        feature_list_columns = ['crowd_score', 'gesture_score', 'face_score',
                                'speaker_sound_score', 'age', 'country', 'years_professional',
                                'tourn_entered', 'play_status', 'hole',
                                'ground', 'stroke', 'par_number', 'hole_yardage', 'hit_bunker',
                                'hit_fairway', 'green_in_regulation', 'putts', 'sand_save',
                                'player_rank',
                                'player_in_top10', 'player_tied', 'in_water', 'ball_position',
                                'shot_length', 'penalty', 'last_shot', 'is_eagle_or_better',
                                'is_birdie', 'is_par',
                                'is_bogey', 'is_double_bogey_or_worse', 'close_approach',
                                'long_putt', 'feels_like', 'temperature', 'heat_index',
                                'barometric_pressure',
                                'relative_humidity']
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(
                source_uid=self.model_uid,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                input_data_type=InputDataType.STRUCTURED,
                prediction_column='prediction',
                probability_column='probability',
                label_column=label_column[0],
                feature_columns=feature_list_columns,
                categorical_columns=[]
            )
        )

        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid
        print("Subscription details: {}".format(self.subscription.get_details()))

    def test_04_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_05_list_deployments(self):
        self.subscription.list_deployments()

    def test_06_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_07_get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_08_score(self):
        payload_scoring = {
            "fields": ['crowd_score', 'gesture_score', 'face_score', 'speaker_sound_score', 'age', 'country', 'years_professional', 'tourn_entered', 'play_status', 'hole',
                       'ground', 'stroke', 'par_number', 'hole_yardage', 'hit_bunker', 'hit_fairway', 'green_in_regulation', 'putts', 'sand_save', 'player_rank', 'player_in_top10',
                       'player_tied', 'in_water', 'ball_position', 'shot_length', 'penalty', 'last_shot', 'is_eagle_or_better', 'is_birdie', 'is_par', 'is_bogey',
                       'is_double_bogey_or_worse', 'close_approach', 'long_putt', 'feels_like', 'temperature', 'heat_index', 'barometric_pressure', 'relative_humidity'],
            "values": [
                [1.0, 0.02346348849600732, 0.3999998298937997, 1.0, 24.0, 0.00000000000000006347042126323393, 7.0, 4.0, 0.0000000000000000124100802683715, 12.0, 4.0, 2.0, 3.0,
                 155.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 1.0, 0.0, 1.0, 329.3, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 14.0, 14.0, 14.0, 999.47, 46.0]]
        }

        TestAIOpenScaleClient.payload_scoring = payload_scoring
        TestAIOpenScaleClient.scoring_records = 20
        for i in range(0, int(self.scoring_records)):
            TestAIOpenScaleClient.scoring_result = self.deployment.score(payload=payload_scoring)
            print("Scoring result: {}".format(self.scoring_result))
            self.assertIsNotNone(self.scoring_result)

    def test_09_stats_on_payload_logging_table(self):
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
        assert_payload_logging_python_table_content(python_table_content=python_table_content,
                                                    fields=['prediction', 'probability'])

    def test_10_v2_performance_monitoring(self):
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

    # def test_13_stats_on_performance_monitoring_table(self):
    #     if self.scoring_result is None:
    #         self.skipTest(reason="Scoring failed. Skipping performance table check.")
    #
    #     if is_icp():
    #         self.skipTest("Performance monitoring is not working on ICP with WML scoring.")
    #
    #     wait_for_performance_table(subscription=self.subscription)
    #
    #     self.subscription.performance_monitoring.print_table_schema()
    #     self.subscription.performance_monitoring.show_table()
    #     self.subscription.performance_monitoring.describe_table()
    #     self.subscription.performance_monitoring.get_table_content()
    #
    #     performance_metrics = self.subscription.performance_monitoring.get_table_content(format='python')
    #     print("Performance metrics:\n{}".format(performance_metrics))
    #     self.assertGreater(len(performance_metrics['values']), 0)

    def test_11_enable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.7, min_records=5)

        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_12_feedback_logging(self):
        from ibm_ai_openscale.supporting_classes import FeedbackFormat

        with open(self.deployment.filename, 'rb') as csvFile:
            TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=csvFile, feedback_format=FeedbackFormat.CSV, data_header=True, data_delimiter=',')

        wait_for_feedback_table(subscription=self.subscription, feedback_records=500)

    def test_13_stats_on_feedback_logging(self):
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()

    def test_14_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_15_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_16_get_quality_metrics(self):
        print("\nQuality metrics test: ")
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)
    #
    # def test_19_setup_explainability(self):
    #     TestAIOpenScaleClient.data_df = pd.read_csv("datasets/golf/golf_train_data.csv")
    #
    #     TestAIOpenScaleClient.subscription.explainability.enable(
    #         training_data=TestAIOpenScaleClient.data_df
    #     )
    #
    # def test_20_get_details(self):
    #     details = TestAIOpenScaleClient.subscription.explainability.get_details()
    #     assert_explainability_configuration(explainability_details=details)
    #
    # def test_21_get_transaction_id(self):
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
    # def test_22_run_explainability(self):
    #     explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id=self.transaction_id,
    #         background_mode=False
    #     )
    #     assert_explainability_run(explainability_run_details=explainability_run)
    #
    # def test_22b_list_explanations(self):
    #     TestAIOpenScaleClient.subscription.explainability.list_explanations()
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
    #
    # def test_24_setup_fairness_monitoring(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         features=[
    #             Feature("age", majority=[[30, 80]], minority=[[15, 29]], threshold=0.6)
    #         ],
    #         favourable_classes=[1.0],
    #         unfavourable_classes=[2.0, 3.0, 4.0],
    #         min_records=12,
    #         training_data=TestAIOpenScaleClient.data_df
    #     )
    #
    # def test_25_get_fairness_monitoring_details(self):
    #     details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
    #     assert_fairness_configuration(fairness_monitoring_details=details)
    #
    # def test_26_run_fairness(self):
    #     fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
    #     assert_fairness_run(fairness_run_details=fairness_run)
    #
    # def test_27_stats_on_fairness_monitoring_table(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)
    #
    #     python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
    #     assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)
    #
    # def test_28_debias(self):
    #     debias_result = TestAIOpenScaleClient.subscription.fairness_monitoring.debias(payload=TestAIOpenScaleClient.payload_scoring)
    #     print('debias_result', debias_result)
    #     self.assertTrue('debiased_probability' in str(debias_result))

    def test_29_enable_assurance_monitor(self):
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
                "max_number_of_records": 1000,
            },
            "thresholds": [
                {
                    "metric_id": "confidence",
                    "type": "lower_limit",
                    "value": 0.8
                },
                {
                    "metric_id": "uncertainty",
                    "type": "upper_limit",
                    "value": 0.9
                }
            ]
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

    def test_30_run_assurance_monitor(self):
        TestAIOpenScaleClient.assurance_run_time = datetime.utcnow().isoformat() + 'Z'

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

    def test_31_wait_for_assurance_monitor_finish(self):
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

    def test_32_check_assurance_metrics(self):
        TestAIOpenScaleClient.subscription.monitoring.show_table('assurance')
        query = '?start={}&end={}'.format(TestAIOpenScaleClient.assurance_run_time, datetime.utcnow().isoformat() + 'Z')
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

    def test_33_disable_assurance_monitor(self):
        response = requests.delete(
            url=self.hrefs_v2.get_monitor_instance_details_href(TestAIOpenScaleClient.assurance_monitor_instance_id),
            headers=self.ai_client._get_headers())

        print('response', response.status_code, response.text)
        self.assertTrue(response.status_code == 202)

    def test_34_disable_all_monitors(self):
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


