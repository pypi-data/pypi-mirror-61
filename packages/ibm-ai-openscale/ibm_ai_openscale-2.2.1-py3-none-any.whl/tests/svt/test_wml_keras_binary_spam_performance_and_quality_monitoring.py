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
from utils.wml_deployments.keras import BinarySpam

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType, FeedbackFormat
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2

import pickle
from numpy import zeros


def vectorize_sequences(sequences, dimension=4000):
    results = zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


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
    scoring_records = None
    feedback_records = None
    final_run_details = None

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()
        cls.deployment = BinarySpam()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        with open('artifacts/spam-classification/tokenizer.pickle', 'rb') as handle:
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
                problem_type=ProblemType.BINARY_CLASSIFICATION,
                input_data_type=InputDataType.UNSTRUCTURED_TEXT,
                label_column='label'
            )
        )
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription details: {}".format(subscription.get_details()))

    def test_05_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(subscription_uid=self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_06_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_07_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        assert_monitors_enablement(subscription_details=subscription_details, payload=True, performance=True)

    def test_08_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        assert_payload_logging_configuration(payload_logging_details=payload_logging_details)

    def test_09_get_performance_monitor_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        assert_performance_monitoring_configuration(performance_monitoring_details=performance_monitoring_details)

    def test_10_score(self):
        messages = [
            "Door moment let the to door lord soul so with his on and his than its. Gently beak was hauntedtell from fiery to the rapping only all what borrow bust was the we. Lordly metell ember curious to bore entrance linking art heart. Smiling undaunted its. Of is i word out my. Wrought to quoth sat respiterespite rare chamber footfalls bird moment god longer the. If or both whether sat surcease whispered see into said ungainly chamber much. Eyes laden and within. Undaunted hath the the ebony violet more. Core entreating unseen said and was bird. Evilprophet or answer the sad just.</p><p>Lady silence oer no whispered distinctly heart and from out me i usby rare fowl i sad metell.",
            "Pile there of den at relief. But ever on native than other as run or suits was counsel were of sacred a scorching sacred. Atonement stalked from shades longed been honeyed dwelt aye ee of childe are is pride fame day mood he. But a childe dwelt time are spent brow him with eremites than vast to adversity. Them prose from whom isle hight soon womans. Are nor his nor. None whence partings the there pride losel had chill along done resolved as. Sooth did none him childe flaunting made ye in her not condemned run be. Run take many. Whateer he and. Disporting had far talethis to bade or of his. Whateer maddest harold ne ah feel now of parasites to one. So in bower for her of forgot but begun a known through loved his. A partings the times shrine the given pile feud mirthful blazon deem alas flee change friends and feeble. Heart if of shamed at with agen heavenly ee are below harold was. Weary made was far sighed olden change crime sore nor ancient pillared he",
            "The the stopped that ominous lore bird whose respiterespite then curtain. That bust whom human that startled and god now. Be the placid human an the or ever divining bird perched feather bird hath my as. In was token nevermore distant floor grim smiling word floating the. Feather loneliness plutonian that. Door pondered a gently before more the me. Cannot rapping and.</p><p>Morrow and i to or what a said beguiling sought eagerly bird aptly of my soul swung. This no merely and this and wondering i my door nevermore into more door gave my in thy. My i it still take bird that of implore lamplight thy.</p><p>Tinkled and sought bends aptly i than on shaven stronger december only seraphim there with nights but. Placid its and hear within soul with a lies. Heard shorn the and master bust than soon hopes. His off a on sainted that of horror faintly. That no its. The this was soon the on from there. Fact he a in me take thing this though fiend if thereis doubtless to. Till the take i my nevermore respiterespite i heaven was the heart nevermore word tapping angels and lady and. Heard clasp only lie that shorn. Tapping or god bird sat lady mortals. Mystery and flitting floor respiterespite and floor hesitating answer visiter tossed midnight as above. Thou quoth here sign lent. At i my the my startled hath the ah grew kind the reply ah the. Is upon the i ease or rare lost thy cushions. Fancy more some flutter bird or of my soul tempter many bleak name the ghost i. There answer on in murmured sitting visiter usby. Other chamber as my. More that these the",
            "That the art agreeing weak caught hath quoth. Soul me the upstarting the oer flutter desolate raven methought door and shore. Chamber one hauntedtell still stately maiden broken angels maiden sinking was by and of whose.</p><p>With a door respiterespite leave the thereis as. Syllable then pallas and for my into wind door thy that seeming. Syllable nothing only nights a lining nevermore whether the. From bust metell napping.</p><p>Form of lies purple the and god beast again leave i felt angels demons at the upon press dream. Gloated and of nameless. Bird gave of. Scarce back days door and midnight fowl youhere the and the opened stillness nothing. The wind door though oh evilprophet a the whether youhere surely i enchanted shrieked each out. Napping or sought turning meaninglittle floor. Seeming wheeled divining did for my our at sitting came sure perfumed. Whether and quoth that truly startled the some implore angels still tempest myself dying there unseen morrow"]

        tokenized_messages = self.tokenizer.texts_to_sequences(messages)
        vectorized_messages = vectorize_sequences(tokenized_messages)

        scoring_payload = {'values': vectorized_messages.tolist()}

        scoring_payload = json.dumps(scoring_payload)
        scoring_payload = json.loads(scoring_payload)

        no_scoring_requests = 3
        TestAIOpenScaleClient.scoring_records = len(messages) * no_scoring_requests

        for i in range(0, no_scoring_requests):
            scores = self.deployment.score(payload=scoring_payload)
            self.assertIsNotNone(scores)

        wait_for_payload_table(subscription=self.subscription, payload_records=self.scoring_records)

    def test_11_stats_on_payload_logging_table(self):
        self.subscription.payload_logging.print_table_schema()
        assert_payload_logging_unstructured_data(subscription=self.subscription, scoring_records=self.scoring_records)

    def test_12_performance_monitoring(self):
        if is_icp():
            self.skipTest("Performance monitoring is not working on ICP with WML scoring.")

        if not is_ypqa():
            self.skipTest("Performance monitoring V2 is only on YP-QA env.")

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

    def test_13_enable_quality_monitoring(self):
        self.subscription.quality_monitoring.enable(threshold=0.7, min_records=10)

        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_monitoring_configuration(quality_monitoring_details=details)

    def test_14_feedback_logging(self):

        messages = [
            "Of to gently flown shrieked ashore such sad his the methought velvet me it burden of each so more. Parting god above sinking of that. In farther i only the the. For that it weak this days floating plume unhappy weak had many fancy.</p><p>Made and fiend burden lenore the kind the me burden and of eyes for bust curious be. Still still fancy the evermore and clasp long throws an chamber bird raven was little quoth. But stopped that lore other. To suddenly thy the theeby still thereis of. Had that at thou above that nevermore never an gaunt had on the that what beating entrance wretch take. Gaunt whom here thy my and art. And fantastic black longer upon above with god but tapping though i be silence. But though nevermore from gently lenore bird bore its. Bust a youhere countenance again the darkness above the eyes nevernevermore hath thy and moment its as forget. Again i lord i. From the grew above sat from whose if i within lenore. More flirt sought. And and thee into whether still he the rustling he if the one. Long weary loneliness swung oer i merely. Here tapping something rare no upon my into gave.</p><p>His my the my door this in countenance wide an lenore borrow have midnight. It token now. Minute hath days the in said floor at faintly lie flutter that. Again there as lenore explore beguiling raven. Grew above was. Silence rustling explore lenore door only lady late lamplight door off heart grew. It more shadow seat name rare i. This raven is if tinkled sorrow least such my of before ever and. Nevermore hope hauntedtell many a with it the for the. My flirt all more. Ancient rapping thee ominous let above me his above one here wide. Evermore that and",
            "Sight nor his his them. Maidens caught smile him his were for childe from deemed visit shameless but spoiled in waste partings more. Me he grief the heartless and. In deem full. Lines uses that before sins and tear. The and or from of shades. Lay since a mine true clay. None smile lands to long present days if. Him her oft brow a not long still the. Bower then the of would neer he condemned sea they and did might what have forgot joyless present disporting. True there blast which and into before. All ungodly to at childe lurked soon to to the glare vile sins wassailers joyless say had.</p><p>Vaunted his formed native his. Honeyed the artless not harold wins mighty ne oer to nor companie me atonement scene now. Was one not. Love and ever in joyless to flaunting time but for which that soils to. His parting he amiss seemed start misery bower of now nine. In joyless disappointed power days though albions  neer open olden he condemned none save dear pilgrimage but a not. And ways and dwelt from festal day but was tales his and who youth pillared pangs than through. Heavenly of condole flash his sick harold a his come long agen sullen haply. Grief loved was old sad crime.</p><p>Before save he the save if and vexed his the not haply for had labyrinth adversity shades his lineage. His in hellas and lone coffined little hight breast by me felt that revel but dome. Sad harolds her his ee alone breast with to could which. He shamed within",
            "Hellas himnot nor each and and. Lurked objects few longdeserted she than. Were monks yet once of fall a maidens along a none so. And that to blazon scorching come moths done sore losel.</p><p>Yet chill but name that resolved harold none will call his but begun thy she present his days drowsy. Beyond his pangs had scene if had open heart but if loved thy time shades a deemed. To or seek counsel been bliss to would by said glorious call childe land. Below sins childe so. Vast almost save his one lurked any for control for happy night the chaste was befell another. And and native oer chill known bacchanals for sacred a nor other nor a and riot. Where would a. Harolds wight him passion lowly shell so but lurked nor. Had from the him had reverie one of sister power say known one goodly to. For men did and condemned the ere deem. Thee little had and. Nor noontide vile the near and in rhyme pillared peace.</p><p>And scene oft flaunting had for delight or and was before maidens lowly. Olden are sun kiss perchance heavenly and domestic een. Fly are her crime nine and oer whom harold. Lemans cared but. With that youth he bower open sadness sought bliss atonement atonement dwell few concubines olden his sins none. Massy finds from. Them dome loved she through and longdeserted native from thence he any wight. Yes time festal he drop seemed sad mammon his but moths made of yet albions knew honeyed formed. Vulgar can sore native. For of when dear seraphs but joyless are. Pangs long oer things. Done made third begun friends suffice go. My that kiss sorrow sing when me come from stalked him his gathered ah to",
            "Whom the horror angels grave. Of said nevermore of and bird or at all god the. Of friends whom and from token an sculptured my his. A lonely and with the december. In angels beak aptly. Grew flown heard it a the sorrowsorrow tossed thereis. From but i an leave it tempest all soul that entreating one. Bird black friends the heart sir dreams. Lonely to said lining the fancy and ebony repeating uttered your said demons theeby the quoth shadow its and. Beast a and i aptly thereat and word here press pallid a whom. Whispered this a startled said shaven chamber long i door dreaming implore. Be or of fancy straight mefilled the. Bust and flitting heart cannot the placid each said i hopes. Shorn chamber my thy tell tufted velvet yet word but into the then of said shaven from. Many placid dreaming muttered.</p><p>Dying ancient this nightly betook and a thereis ghastly a sainted nothing leave the wide. His repeating only the chamber the thy thy wide for flirt stately but my clasp above unseen. Clasp pondered from heard that the. Answer raven chamber i and the nothing name hear napping that desolate one only lord into the. Me i quaint only bust bird. Of from in was fowl all my entrance perched my the. Lenore quoth and a seeing if nodded while its that raven his wind then. Something something angels that nevermore stillness fiery from the before in upon theeby friends ungainly stood sign door and. By just scarcely more desolate made for spoken nights thrilled wind the tempest. Over within one truly wandering heart disaster. Metell this balm still. Above above borrow perfumed shall flirt flitting. I respiterespite here sorrowsorrow lost whom this a gaunt lie devil here. A desert in wished separate within i what entrance bird. And had on that minute more and flown is violet burned angels was methought flirt.</p><p>Hauntedtell soul visiter of the implore sitting terrors though what form door thy soul rapping and. Eagerly over curtain lenore from merely unmerciful gave this hath tell velvet shore. An i chamber nevermore him of sat flutter and",
            "Of to gently flown shrieked ashore such sad his the methought velvet me it burden of each so more. Parting god above sinking of that. In farther i only the the. For that it weak this days floating plume unhappy weak had many fancy.</p><p>Made and fiend burden lenore the kind the me burden and of eyes for bust curious be. Still still fancy the evermore and clasp long throws an chamber bird raven was little quoth. But stopped that lore other. To suddenly thy the theeby still thereis of. Had that at thou above that nevermore never an gaunt had on the that what beating entrance wretch take. Gaunt whom here thy my and art. And fantastic black longer upon above with god but tapping though i be silence. But though nevermore from gently lenore bird bore its. Bust a youhere countenance again the darkness above the eyes nevernevermore hath thy and moment its as forget. Again i lord i. From the grew above sat from whose if i within lenore. More flirt sought. And and thee into whether still he the rustling he if the one. Long weary loneliness swung oer i merely. Here tapping something rare no upon my into gave.</p><p>His my the my door this in countenance wide an lenore borrow have midnight. It token now. Minute hath days the in said floor at faintly lie flutter that. Again there as lenore explore beguiling raven. Grew above was. Silence rustling explore lenore door only lady late lamplight door off heart grew. It more shadow seat name rare i. This raven is if tinkled sorrow least such my of before ever and. Nevermore hope hauntedtell many a with it the for the. My flirt all more. Ancient rapping thee ominous let above me his above one here wide. Evermore that and",
            "Sight nor his his them. Maidens caught smile him his were for childe from deemed visit shameless but spoiled in waste partings more. Me he grief the heartless and. In deem full. Lines uses that before sins and tear. The and or from of shades. Lay since a mine true clay. None smile lands to long present days if. Him her oft brow a not long still the. Bower then the of would neer he condemned sea they and did might what have forgot joyless present disporting. True there blast which and into before. All ungodly to at childe lurked soon to to the glare vile sins wassailers joyless say had.</p><p>Vaunted his formed native his. Honeyed the artless not harold wins mighty ne oer to nor companie me atonement scene now. Was one not. Love and ever in joyless to flaunting time but for which that soils to. His parting he amiss seemed start misery bower of now nine. In joyless disappointed power days though albions  neer open olden he condemned none save dear pilgrimage but a not. And ways and dwelt from festal day but was tales his and who youth pillared pangs than through. Heavenly of condole flash his sick harold a his come long agen sullen haply. Grief loved was old sad crime.</p><p>Before save he the save if and vexed his the not haply for had labyrinth adversity shades his lineage. His in hellas and lone coffined little hight breast by me felt that revel but dome. Sad harolds her his ee alone breast with to could which. He shamed within",
            "Hellas himnot nor each and and. Lurked objects few longdeserted she than. Were monks yet once of fall a maidens along a none so. And that to blazon scorching come moths done sore losel.</p><p>Yet chill but name that resolved harold none will call his but begun thy she present his days drowsy. Beyond his pangs had scene if had open heart but if loved thy time shades a deemed. To or seek counsel been bliss to would by said glorious call childe land. Below sins childe so. Vast almost save his one lurked any for control for happy night the chaste was befell another. And and native oer chill known bacchanals for sacred a nor other nor a and riot. Where would a. Harolds wight him passion lowly shell so but lurked nor. Had from the him had reverie one of sister power say known one goodly to. For men did and condemned the ere deem. Thee little had and. Nor noontide vile the near and in rhyme pillared peace.</p><p>And scene oft flaunting had for delight or and was before maidens lowly. Olden are sun kiss perchance heavenly and domestic een. Fly are her crime nine and oer whom harold. Lemans cared but. With that youth he bower open sadness sought bliss atonement atonement dwell few concubines olden his sins none. Massy finds from. Them dome loved she through and longdeserted native from thence he any wight. Yes time festal he drop seemed sad mammon his but moths made of yet albions knew honeyed formed. Vulgar can sore native. For of when dear seraphs but joyless are. Pangs long oer things. Done made third begun friends suffice go. My that kiss sorrow sing when me come from stalked him his gathered ah to",
            "Whom the horror angels grave. Of said nevermore of and bird or at all god the. Of friends whom and from token an sculptured my his. A lonely and with the december. In angels beak aptly. Grew flown heard it a the sorrowsorrow tossed thereis. From but i an leave it tempest all soul that entreating one. Bird black friends the heart sir dreams. Lonely to said lining the fancy and ebony repeating uttered your said demons theeby the quoth shadow its and. Beast a and i aptly thereat and word here press pallid a whom. Whispered this a startled said shaven chamber long i door dreaming implore. Be or of fancy straight mefilled the. Bust and flitting heart cannot the placid each said i hopes. Shorn chamber my thy tell tufted velvet yet word but into the then of said shaven from. Many placid dreaming muttered.</p><p>Dying ancient this nightly betook and a thereis ghastly a sainted nothing leave the wide. His repeating only the chamber the thy thy wide for flirt stately but my clasp above unseen. Clasp pondered from heard that the. Answer raven chamber i and the nothing name hear napping that desolate one only lord into the. Me i quaint only bust bird. Of from in was fowl all my entrance perched my the. Lenore quoth and a seeing if nodded while its that raven his wind then. Something something angels that nevermore stillness fiery from the before in upon theeby friends ungainly stood sign door and. By just scarcely more desolate made for spoken nights thrilled wind the tempest. Over within one truly wandering heart disaster. Metell this balm still. Above above borrow perfumed shall flirt flitting. I respiterespite here sorrowsorrow lost whom this a gaunt lie devil here. A desert in wished separate within i what entrance bird. And had on that minute more and flown is violet burned angels was methought flirt.</p><p>Hauntedtell soul visiter of the implore sitting terrors though what form door thy soul rapping and. Eagerly over curtain lenore from merely unmerciful gave this hath tell velvet shore. An i chamber nevermore him of sat flutter and"
        ]

        labels = [
            "0",
            "1",
            "1",
            "0",
            "0",
            "1",
            "1",
            "0",
        ]

        tokenized_messages = self.tokenizer.texts_to_sequences(messages)
        vectorized_messages = vectorize_sequences(tokenized_messages)

        text_list = vectorized_messages.tolist()

        feedback_data = []
        for i in range(0, len(text_list)):
            feedback_data.append([text_list[i], int(labels[i])])

        no_feedback_records = 3

        for i in range(0, no_feedback_records):
            self.subscription.feedback_logging.store(feedback_data=feedback_data)

        TestAIOpenScaleClient.feedback_records = (len(feedback_data) * no_feedback_records)

        wait_for_feedback_table(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_15_stats_on_feedback_logging(self):
        self.subscription.feedback_logging.show_table()
        assert_feedback_logging_unstructured_data(subscription=self.subscription, feedback_records=self.feedback_records)

    def test_16_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        assert_quality_entire_run(subscription=TestAIOpenScaleClient.subscription, run_details=run_details)
        TestAIOpenScaleClient.final_run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(
            run_uid=run_details['id'])

    def test_17_get_metrics(self):
        quality_monitoring_metrics = wait_for_quality_metrics(subscription=self.subscription)
        data_mart_quality_metrics = self.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        assert_get_quality_metrics(self.final_run_details, data_mart_quality_metrics, quality_monitoring_metrics)

        quality_monitoring_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        assert_quality_metrics_binary_model(data_mart_quality_metrics, quality_monitoring_details, subscription_uid=self.subscription_uid)

    def test_18_stats_on_quality_monitoring_table(self):
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
