from abc import ABC, abstractmethod
from watson_machine_learning_client import WatsonMachineLearningAPIClient
from utils.configuration import get_wml_credentials, is_wml_v4, is_icp


class WMLDeployment(ABC):
    scoring_url = None
    deployment_uid = None
    asset_uid = None
    deployment_details = None
    filename = None

    def __init__(self, name, asset_name):
        self.wml_v4 = is_wml_v4()
        self.name = name
        self.asset_name = asset_name
        self.wml_client = WatsonMachineLearningAPIClient(get_wml_credentials())
        self.space_id = None

        if self.wml_v4:
            if is_icp():
                self.set_space()
        
        self._get_ids()
        if self.deployment_uid is None:
            self.publish_model()
            self.deploy()
            self._get_ids()
            
    def set_space(self):
        space_name = "auto-test-space"
        spaces = self.wml_client.spaces.get_details()['resources']

        for space in spaces:
            if space['entity']['name'] == space_name:
                self.space_id = space["metadata"]["guid"]

        if self.space_id is None:
            self.space_id = self.wml_client.spaces.store(
                meta_props={self.wml_client.spaces.ConfigurationMetaNames.NAME: space_name})["metadata"]["guid"]
        self.wml_client.set.default_space(self.space_id)

    @abstractmethod
    def publish_model(self):
        pass

    def get_asset_id(self):
        return self.asset_uid

    def get_deployment_id(self):
        return self.deployment_uid

    def deploy(self):
        if self.wml_v4:
            print("Deploying model {} using V4 client.".format(self.asset_uid))
            deployment_props = {
                self.wml_client.deployments.ConfigurationMetaNames.NAME: self.name,
                self.wml_client.deployments.ConfigurationMetaNames.ONLINE: {}
            }

            deployment = self.wml_client.deployments.create(
                artifact_uid=self.asset_uid,
                meta_props=deployment_props)

            self.deployment_uid = self.wml_client.deployments.get_uid(deployment)
            self.deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)

            print("Deployment completed. Details: {}".format(self.deployment_details))
        else:
            print("Deploying model {} using V3 client.".format(self.asset_uid))
            deployment = self.wml_client.deployments.create(
                artifact_uid=self.asset_uid,
                name=self.name,
                asynchronous=False)

            self.deployment_uid = self.wml_client.deployments.get_uid(deployment)
            self.deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)

            print("Deployment completed. Details: {}".format(self.deployment_details))

    def score(self, payload):
        if self.wml_v4:
            scoring_payload = {self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [payload]}
            return self.wml_client.deployments.score(self.deployment_uid, scoring_payload)
        else:
            return self.wml_client.deployments.score(self.scoring_url, payload)

    def _get_ids(self):
        if self.wml_v4:
            for deployment in self.wml_client.deployments.get_details()['resources']:
                if deployment['entity']['name'] == self.name:
                    model_href = deployment['entity']['asset']['href']
                    splitted_href = model_href.split('/')[3]
                    self.asset_uid = splitted_href.split('?')[0] if '?' in splitted_href else splitted_href
                    self.deployment_details = deployment
                    self.deployment_uid = deployment['metadata']['guid']
                    self.scoring_url = deployment['entity']['status']['online_url']
                    self.model_details = self.get_asset_details(self.asset_uid)
                    print("Model details: {}".format(self.model_details))
                    print("Deployment details: {}".format(deployment))
        else:
            for deployment in self.wml_client.deployments.get_details()['resources']:
                if deployment['entity']['name'] == self.name:
                    self.asset_uid = deployment['entity']['deployable_asset']['guid']
                    self.deployment_uid = deployment['metadata']['guid']
                    self.scoring_url = deployment['entity']['scoring_url']
                    self.model_details = self.get_asset_details(self.asset_uid)
                    print("Model details: {}".format(self.model_details))
                    print("Deployment details: {}".format(deployment))

    def get_asset_details(self, asset_id):
        return self.wml_client.repository.get_model_details(asset_id)


def clean_up_wml_instance():
    wml_client = WatsonMachineLearningAPIClient(get_wml_credentials())

    print("Cleaning wml instance.")
    print("Removing all deployments...")

    for deployment in wml_client.deployments.get_details()['resources']:
        wml_client.deployments.delete(deployment['metadata']['guid'])

    details = wml_client.repository.get_details()

    print("Removing all models...")
    for model in details['models']['resources']:
        wml_client.repository.delete(model['metadata']['guid'])

    print("Removing all runtimes...")
    for runtime in details['runtimes']['resources']:
        wml_client.repository.delete(runtime['metadata']['guid'])

    # print("Removing definitions...")
    # for definition in details['definitions']['resources']:
    #     wml_client.repository.delete(definition['metadata']['guid'])

    print("Cleaning done.")