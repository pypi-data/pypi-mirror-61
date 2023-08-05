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
from utils.wml_deployments.keras import StackOverflow

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2

import pickle


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
        cls.deployment = StackOverflow()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        with open('artifacts/stack-overflow/tokenize.pickle', 'rb') as handle:
            cls.tokenizer = pickle.load(handle)

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
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(
                source_uid=self.model_uid,
                binding_uid=self.binding_uid,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                input_data_type=InputDataType.UNSTRUCTURED_TEXT,
                label_column='label'
            )
        )
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription details: {}".format(subscription.get_details()))

    def test_05_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_06_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        print(str(TestAIOpenScaleClient.subscription.get_details()))

    def test_07_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_09_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_10_get_performance_monitor_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_11_score(self):
        posts = [
            "is there a way i can restyle form items on iphone   i m working on making my site responsive and i have a form on my site. i restyled my form using css  but on iphone the styles  gone lost  and they have default styles of iphone.    is there any way i can style them      thanks ",
            "apple archive errors  i m trying to uploading my app to apple through archive in xcode but i m having these issues:    1)iphone/ipod touch: info.plist: unable to verify icon dimensions  no icon found. you must define cfbundleicons  cfbundleiconsfiles  cfbundleiconfile  or provide a default icon.png that is 57x57    2) unable to extract code signing entitlements from you application. please make sure myappname-prefix.pchmynameapp is a valid match executable that s properly code signed.    i dragged in the boxes the 2 icons and the screenshots (retina and not) but i don t know how to resolve it. also the other issues i don t know how to resolve them.    thanks",
            "how to trigger ngchange event when user pastes something in a content editable div using mouse right click   i ve a content editable div and when user pastes something in it using mouse right click and paste  i want to trigger a function. i already have ng-change event bound so if i can trigger that  that s also fine",
            "how to make jcoverflip loop   i searched and found questions similar to my question  however none has the specific solution i need. i currently have jcoverflip without the scroll bar or any next/prev buttons... what i would like to accomplish is... on hover  have the gallery scroll and when it reaches to the end it loops instead of having scroll all the way backwards. i m currently new to javascript/jquery and would appreciate any help..also if you have any alternative scripts in mind  i am open to suggestions",
            "what is system.activator.createinstance   what is system.activator.createinstance and when should i use it",
        ]

        tokenized_posts = self.tokenizer.texts_to_matrix(posts)

        scoring_payload = {'values': tokenized_posts.tolist()}
        scoring_payload = json.dumps(scoring_payload)
        scoring_payload = json.loads(scoring_payload)

        no_scoring_requests = 5
        TestAIOpenScaleClient.scoring_records = len(posts) * no_scoring_requests
        for i in range(0, no_scoring_requests):
            scores = self.deployment.score(payload=scoring_payload)
            self.assertIsNotNone(scores)

        print(scores)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_12_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        assert_payload_logging_unstructured_data(subscription=self.subscription, scoring_records=self.scoring_records)

    def test_13_performance_monitoring(self):
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

    def test_14_enable_quality_monitoring(self):
        self.subscription.quality_monitoring.enable(threshold=0.7, min_records=10)

        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_15_feedback_logging(self):

        posts = [
            "how to zoom imageview in android  i have an imageview declared in main.xml . i want it to be zoomed . how can this be done in android",
            "angularjs ng- click with external link without controller   i need to redirect the external link while we click on the radio button. is any possible without use controller",
            "how to use mouseleave with if  when checkbox checked    mouseleave-enter events be false  when unchecked mouseleave-enter events be true. how can i do them   sorry for my bad language",
            "two subviews in uiscrollview  i want to use two views in uiscrollview. in the first view  when i scale down to 50% its size then the second view will show and then the first view will hide then the second view will continue scrolling down. now my problem is how can i scroll down the second view     thanks",
            "why is it that an overridden method can t throw a new checked exception  i have two questions :   <ol> <li>what is the purpose of the constraint that an overridden method can t throw a new checked exception </li> <li>why it is allowed that an overridden method can only throw all or none  or a subset of the checked exceptions that are specified in the throws clause of the overridden method in the superclass </li> </ol>",
        ]

        labels = [
            "1",
            "2",
            "5",
            "10",
            "1"
        ]

        tokenized_posts = self.tokenizer.texts_to_matrix(posts)

        feedback_payload = ""
        for i in range(0, len(posts)):
            feedback_payload += "{};{}\n".format(tokenized_posts.tolist()[i], labels[i])

        TestAIOpenScaleClient.feedback_records = 5 * len(posts)
        for i in range(0, 5):
            self.subscription.feedback_logging.store(feedback_data=feedback_payload, feedback_format=FeedbackFormat.CSV, data_header=False, data_delimiter=';')

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_16_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        assert_feedback_logging_unstructured_data(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_17_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=TestAIOpenScaleClient.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_18_get_metrics(self):
        quality_monitoring_metrics = wait_for_quality_metrics(subscription=self.subscription)
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
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

    @classmethod
    def tearDownClass(cls):
        cls.ai_client.data_mart.subscriptions.delete(
            subscription_uid=cls.subscription_uid
        )


if __name__ == '__main__':
    unittest.main()
