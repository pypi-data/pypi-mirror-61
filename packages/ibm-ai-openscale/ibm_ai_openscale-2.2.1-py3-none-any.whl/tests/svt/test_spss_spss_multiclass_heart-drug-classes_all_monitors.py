# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pandas as pd
from requests.auth import HTTPBasicAuth

from utils.assertions import *
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import SPSSMachineLearningInstance, SPSSMachineLearningAsset
from ibm_ai_openscale.supporting_classes import ProblemType, InputDataType, PayloadRecord, Feature
from preparation_and_cleaning import *


@unittest.skipIf("ICP" not in get_env(), "Please run this test only on ICP env")
class TestAIOpenScaleClient(unittest.TestCase):

    ai_client = None
    data_df = None
    deployment_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    wml_client = None
    subscription = None
    binding_uid = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    training_data_statistics = None
    source_uid = None
    request = None
    response = None
    transaction_id = None
    scoring_records = None
    feedback_records = None
    final_run_details = None
    start_date = datetime.utcnow().isoformat() + "Z"

    model_uid = 'ai_drug_mlp_proba_BiasQA'
    # SPSS C&DS
    credentials = get_spss_cnds_credentials()

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



    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        assert_datamart_details(details, schema=self.schema, state='active')

    def test_03_bind_spss_cds_instance(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("SPSS C&DS instance on ICP", SPSSMachineLearningInstance(self.credentials))

    def test_04_get_binding_details(self):
        print("Binding details:\n{}".format(self.ai_client.data_mart.bindings.get_details(self.binding_uid)))

    def test_05_get_asset_id(self):
        assets_uids = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()
        self.assertGreater(len(assets_uids), 1)
        print('Assets uids: ' + str(assets_uids))

        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()
        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details()
        print('Assets details: ' + str(asset_details))

        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_asset_deployments()

        for detail in asset_details:
            if self.model_uid == detail['name']:
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_06_subscribe_spss_asset(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            SPSSMachineLearningAsset(source_uid=TestAIOpenScaleClient.source_uid,
                                     binding_uid=TestAIOpenScaleClient.binding_uid,
                                     input_data_type=InputDataType.STRUCTURED,
                                     problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                                     label_column="Drug",
                                     prediction_column="$N-Drug",
                                     class_probability_columns=['$NP-drugA', '$NP-drugB', '$NP-drugC', '$NP-drugX', '$NP-drugY'],
                                     feature_columns=['Age', 'Sex', 'BP', 'Cholesterol', 'Na', 'K'],
                                     categorical_columns=['Sex', 'BP', 'Cholesterol']
                                     ), deployment_uids="ai_drug_mlp_proba")

        TestAIOpenScaleClient.subscription_uid = subscription.uid

    def test_07_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_08_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_09_score_and_log_payload(self):
        binding_details = self.ai_client.data_mart.bindings.get_details(self.binding_uid)
        binding_credentials = binding_details['entity']['credentials']
        self.assertEqual(self.credentials['username'], binding_credentials['username'])
        self.assertEqual(self.credentials['password'], binding_credentials['password'])
        self.assertEqual(self.credentials['url'], binding_credentials['url'])

        subscription_details = self.subscription.get_details()
        scoring_endpoint = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']
        input_table_id = subscription_details['entity']['asset_properties']['input_data_schema']['id']

        scoring_payload = {
           "id": self.model_uid,
           "requestInputTable": [
              {
                 "id": input_table_id,
                 "requestInputRow": [
                    {
                       "input": [
                          {
                             "name": "Age",
                             "value": "23"
                          },
                          {
                             "name": "Sex",
                             "value": "F"
                          },
                          {
                             "name": "BP",
                             "value": "HIGH"
                          },
                          {
                             "name": "Cholesterol",
                             "value": "HIGH"
                          },
                          {
                             "name": "Na",
                             "value": "0.792535"
                          },
                          {
                             "name": "K",
                             "value": "0.031258"
                          }
                       ]
                    }
                 ]
              }
           ]
        }

        TestAIOpenScaleClient.request = scoring_payload

        start_time = time.time()
        resp_score = requests.post(url=scoring_endpoint, json=scoring_payload, auth=HTTPBasicAuth(username=binding_credentials['username'], password=binding_credentials['password']))
        response_time = time.time() - start_time

        print(resp_score.status_code)
        print(resp_score.text)

        result = resp_score.json()

        print("Scoring payload:\n{}".format(scoring_payload))
        print("Scoring result:\n{}".format(result))

        TestAIOpenScaleClient.scoring_records = 20
        records_list = []
        for i in range(0, self.scoring_records):
            records_list.append(PayloadRecord(request=scoring_payload, response=result, response_time=int(response_time)))

        self.subscription.payload_logging.store(records=records_list)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_10_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        self.subscription.payload_logging.show_table()
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        assert_payload_logging_pandas_table_content(pandas_table_content=table_content, scoring_records=self.scoring_records)

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        assert_payload_logging_python_table_content(python_table_content=python_table_content, fields=['$N-Drug'])

    def test_11_payload_logging_data_distribution(self):
        end_date = datetime.utcnow().isoformat() + "Z"
        data_distribution_run = TestAIOpenScaleClient.subscription.payload_logging.data_distribution.run(
            start_date=self.start_date,
            end_date=end_date,
            group=['Age', 'Cholesterol', '$N-Drug'],
            background_mode=False)

        run_id = data_distribution_run['id']
        data_distribution = self.subscription.payload_logging.data_distribution.get_run_result(run_id=run_id)

        print('Payload data distribution')
        print(data_distribution)

        self.assertEqual(data_distribution.shape[0], 1)
        self.assertEqual(data_distribution.shape[1], 4)
        data_columns = data_distribution.columns.values
        self.assertIn("Age", data_columns)
        self.assertIn("Cholesterol", data_columns)
        self.assertIn("$N-Drug", data_columns)
        self.assertIn("count", data_columns)

    def test_12_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_13_get_quality_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_14_send_feedback_data(self):
        from ibm_ai_openscale.supporting_classes.enums import FeedbackFormat
        feedback_records = {
                            "Age": "48.0",
                            "Sex": "M",
                            "BP": "HIGH",
                            "Cholesterol": "NORMAL",
                            "Na": "0.510179",
                            "K": "079788",
                            "Drug": "drugA"
                          }

        feedback_data = []
        TestAIOpenScaleClient.feedback_records = 20
        for i in range(0, self.feedback_records):
            feedback_data.append(feedback_records)

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_data, feedback_format=FeedbackFormat.DICT)

    def test_15_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=self.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_16_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    def test_17_stats_on_feedback_logging_table(self):
        self.subscription.feedback_logging.show_table()
        self.subscription.feedback_logging.print_table_schema()
        self.subscription.feedback_logging.describe_table()

        feedback_pd = self.subscription.feedback_logging.get_table_content(format='pandas')
        assert_feedback_pandas_table_content(pandas_table_content=feedback_pd, feedback_records=self.feedback_records)

    def test_18_get_quality_metrics(self):
        print("\nQuality metrics test: ")
        quality_monitoring_metrics = self.subscription.quality_monitoring.get_metrics()
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_multiclass_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_19_stats_on_performance_monitoring_table(self):
        self.subscription.performance_monitoring.print_table_schema()
        self.subscription.performance_monitoring.show_table()
        self.subscription.performance_monitoring.describe_table()

        performance_table_pandas = self.subscription.performance_monitoring.get_table_content()
        assert_performance_monitoring_pandas_table_content(pandas_table_content=performance_table_pandas)

        performance_table_python = self.subscription.performance_monitoring.get_table_content(format='python')
        assert_performance_monitoring_python_table_content(python_table_content=performance_table_python)

    def test_20_get_metrics(self):
        print("Old metrics:")
        print(self.ai_client.data_mart.get_deployment_metrics())
        print(self.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(self.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(self.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))

        ### MULTICLASS CHECK

        metrics = {
            'threshold': None,
            'accuracy': None,
            'weighted_true_positive_rate': None,
            'weighted_precision': None,
            'weighted_recall': None,
            'weighted_f_measure': None,
            'weighted_false_positive_rate': None
        }

        quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        print("Old quality metric:\n{}".format(quality_metrics))

        for metric in quality_metrics['deployment_metrics'][0]['metrics'][0]['value']['metrics']:
            if metric['name'] in metrics.keys():
                metrics[metric['name']] = metric['value']

        metrics['threshold'] = quality_metrics['deployment_metrics'][0]['metrics'][0]['value']['threshold']

        ootb_quality_metrics = self.subscription.quality_monitoring.get_metrics()
        print("New quality metrics:\n{}".format(ootb_quality_metrics))

        for metric in ootb_quality_metrics[0]['metrics']:
            if metric['id'] in metrics.keys():
                print("Comparing metric: {}".format(metric['id']))
                self.assertEqual(metric['value'], metrics[metric['id']],
                                 msg="metric {} has different value in ootb api".format(metric['id']))
                if 'lower_limit' in metric.keys():
                    self.assertEqual(metric['lower_limit'], metrics['threshold'],
                                     msg="lower_limit is not the same as threshold!")

        print(self.subscription.quality_monitoring.get_metrics(format="samples"))

    def test_21_get_transaction_id(self):
        pandas_pd = self.subscription.payload_logging.get_table_content()
        no_payloads = len(pandas_pd['scoring_id'].values)

        # select random record from payload table
        import random
        random_record = random.randint(0, no_payloads-1)
        TestAIOpenScaleClient.transaction_id = pandas_pd['scoring_id'].values[random_record]

        print("Selected trainsaction id: {}".format(self.transaction_id))

    def test_22_setup_explainability(self):
        TestAIOpenScaleClient.data_df = pd.read_csv(
            "./datasets/BestHeartDrug/drug_train_data.csv",
            dtype={'Age': float},
            delimiter=';'
        )

        TestAIOpenScaleClient.subscription.explainability.enable(training_data=TestAIOpenScaleClient.data_df)

    def test_23_run_explainability(self):
        explainability_run = TestAIOpenScaleClient.subscription.explainability.run(
            transaction_id=self.transaction_id,
            background_mode=False
        )
        assert_explainability_run(explainability_run_details=explainability_run)

    def test_23b_list_explanations(self):
        TestAIOpenScaleClient.subscription.explainability.list_explanations()

    def test_24_stats_on_explainability_table(self):
        TestAIOpenScaleClient.subscription.explainability.print_table_schema()
        TestAIOpenScaleClient.subscription.explainability.show_table()
        TestAIOpenScaleClient.subscription.explainability.describe_table()

        pandas_df = TestAIOpenScaleClient.subscription.explainability.get_table_content()
        assert_explainability_pandas_table_content(pandas_table_content=pandas_df)

        python_table_content = TestAIOpenScaleClient.subscription.explainability.get_table_content(format='python')
        assert_explainability_python_table_content(python_table_content=python_table_content)

    def test_25_setup_fairness_monitoring(self):

        TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
            features=[
                Feature("Sex", majority=['M'], minority=['F'], threshold=0.8)
            ],
            deployment_uid='ai_drug_mlp_proba',
            favourable_classes=['drugA', 'drugC', 'drugY'],
            unfavourable_classes=['drugB', 'drugX'],
            min_records=4,
            training_data=TestAIOpenScaleClient.data_df
        )

    def test_26_get_fairness_monitoring_details(self):
        details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
        assert_fairness_configuration(fairness_monitoring_details=details)

    def test_27_run_fairness(self):
        fairness_run = TestAIOpenScaleClient.subscription.fairness_monitoring.run(background_mode=False)
        assert_fairness_run(fairness_run_details=fairness_run)

    def test_28_stats_on_fairness_monitoring_table(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
        TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()

        pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
        assert_fairness_monitoring_pandas_table_content(pandas_table_content=pandas_df)

        python_table_content = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python')
        assert_fairness_monitoring_python_table_content(python_table_content=python_table_content)

    def test_29_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_30_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
