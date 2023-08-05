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
from utils.wml_deployments.keras import PolandHousePrices

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat

import pickle
import pandas as pd
from keras.preprocessing.sequence import pad_sequences


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    binding_uid = None
    subscription = None
    scoring_result = None
    test_uid = str(uuid.uuid4())
    scoring_records = None
    feedback_records = None
    final_run_details = None

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = PolandHousePrices()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()


        with open('artifacts/poland_house_prices/poland_prices_tokenizer.pickle', 'rb') as handle:
            cls.tokenizer = pickle.load(handle)

        with open('artifacts/poland_house_prices/poland_prices_scaler.pickle', 'rb') as handle:
            cls.scaler = pickle.load(handle)

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



    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(
                source_uid=self.model_uid,
                binding_uid=self.binding_uid,
                problem_type=ProblemType.REGRESSION,
                input_data_type=InputDataType.UNSTRUCTURED_TEXT,
                label_column='price'
            )
        )
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription details: {}".format(subscription.get_details()))

    def test_07_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_08_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_09_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_10_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_11_get_performance_monitor_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_12_score(self):
        messages = [
            "Poznań, Rynek Wildecki, wielkopolskie, Powierzchnia w m2: 44.82, Liczba pokoi: 2, Piętro: 1, Typ zabudowy: kamienica, Liczba pięter w budynku: 6, Nazwa inwestycji: Rynek Wildecki 3",
            "Poznań, Rynek Wildecki, wielkopolskie, Powierzchnia w m2: 34.84, Liczba pokoi: 1, Piętro: 5,  Typ zabudowy: kamienica, Liczba pięter w budynku: 6, Nazwa inwestycji: Rynek Wildecki 3",
            "Łódź, Bałuty, łódzkie, Powierzchnia w m2: 51.96, Liczba pokoi: 2, Piętro: parter, Typ zabudowy: blok, Liczba pięter w budynku: 4, Nazwa inwestycji: Villa Romanów",
            "Kraków, Prokocim, małopolskie, Powierzchnia w m2: 55.14, Liczba pokoi: 3, Piętro: 2, Typ zabudowy: blok, Liczba pięter w budynku: 3, Miejsce parkingowe: przynależne na ulicy",
            "Wrocław, Wojszyce, dolnośląskie, Powierzchnia w m2: 46.48, Liczba pokoi: 2, Piętro: parter, Typ zabudowy: blok, Liczba pięter w budynku: 2, Nazwa inwestycji: Małe Wojszyce",
            "Wrocław, Krzyki, dolnośląskie, Powierzchnia w m2: 66.59, Liczba pokoi: 3, Piętro: 6, Typ zabudowy: blok, Liczba pięter w budynku: 8, Nazwa inwestycji: Kamienna 145",
            "Warszawa, Gocław, mazowieckie, Powierzchnia w m2: 78.49, Liczba pokoi: 4, Piętro: 15, Liczba pięter w budynku: 17, Nazwa inwestycji: Korona Pragi, ID Inwestycji: 65298180",
            "Warszawa, Służewiec, mazowieckie, Powierzchnia w m2: 61.36, Liczba pokoi: 3, Piętro: 6, Typ zabudowy: blok, Liczba pięter w budynku: 9, Nazwa inwestycji: Osiedle Krzemowe",
            "Wrocław, Klecina, dolnośląskie, Powierzchnia w m2: 59.62, Liczba pokoi: 3, Piętro: parter, Typ zabudowy: blok, Liczba pięter w budynku: 3, Nazwa inwestycji: Między Parkami",
            "Warszawa, Wola, mazowieckie, Powierzchnia w m2: 74.03, Liczba pokoi: 4, Piętro: 3, Typ zabudowy: blok, Liczba pięter w budynku: 7, Nazwa inwestycji: Osiedle Na Woli"
            ]
        tokenized_messages = self.tokenizer.texts_to_sequences(messages)
        tokenized_messages = pad_sequences(tokenized_messages, padding='post', maxlen=28)
        scoring_payload = {'values': tokenized_messages.tolist()}

        TestAIOpenScaleClient.scoring_records = len(messages)

        scores = self.deployment.score(payload=scoring_payload)
        self.assertIsNotNone(scores)
        print("Scoring result: {}".format(scores))

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_13_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        assert_payload_logging_unstructured_data(subscription=self.subscription, scoring_records=self.scoring_records)

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
        feedback_data = pd.read_csv('datasets/poland_house_prices/poland_house_prices_feedback.txt', names=["text", "price"], sep=";")
        for index, row in feedback_data.iterrows():
            tokenized_messages = self.tokenizer.texts_to_sequences([row['text']])
            tokenized_messages = pad_sequences(tokenized_messages, padding='post', maxlen=28).tolist()
            target_field = self.scaler.transform(row['price']).tolist()[0][0]
            feedback_data_row = [[tokenized_messages[0], target_field]]
            self.subscription.feedback_logging.store(feedback_data=feedback_data_row, feedback_format=FeedbackFormat.WML, fields=['scoring_input', 'target'])

        TestAIOpenScaleClient.feedback_records = 40

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_17_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        assert_feedback_logging_unstructured_data(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_18_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=TestAIOpenScaleClient.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_19_stats_on_quality_monitoring_table(self):
        self.subscription.quality_monitoring.print_table_schema()
        self.subscription.quality_monitoring.show_table()
        self.subscription.quality_monitoring.show_table(limit=None)
        self.subscription.quality_monitoring.describe_table()

        quality_monitoring_table = self.subscription.quality_monitoring.get_table_content()
        assert_quality_monitoring_pandas_table_content(pandas_table_content=quality_monitoring_table)

        quality_metrics = self.subscription.quality_monitoring.get_table_content(format='python')
        assert_quality_monitoring_python_table_content(python_table_content=quality_metrics)

    def test_20_get_metrics(self):
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

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
