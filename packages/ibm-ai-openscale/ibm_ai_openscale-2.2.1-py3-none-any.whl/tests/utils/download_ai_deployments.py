from watson_machine_learning_client import WatsonMachineLearningAPIClient
import json

wml_client = WatsonMachineLearningAPIClient({
                    "instance_id": "openshift",
                    "url" : "https://namespace1-cpd-namespace1.apps.zloct36-lb-1.fyre.ibm.com",
                    "username":"admin",
                    "password": "password",
                    "version": "2.0.1"
                })
space_id = None

space_name = "auto-test-space"
spaces = wml_client.spaces.get_details()['resources']

for space in spaces:
    if space['entity']['name'] == space_name:
        space_id = space["metadata"]["guid"]

wml_client.set.default_space(space_id)

print("Resources: {}".format(wml_client.deployments.get_details()))


for deployment in wml_client.deployments.get_details()['resources']:
    if 'AutoAI' in deployment['entity']['name']:
        deployment_details = deployment
        deployment_uid = deployment['metadata']['guid']
        scoring_url = deployment['entity']['status']['online_url']

        model_href = deployment['entity']['asset']['href']
        splitted_href = model_href.split('/')[3]
        asset_uid = splitted_href.split('?')[0] if '?' in splitted_href else splitted_href
        model_details = wml_client.repository.get_model_details(asset_uid)

        wml_client.repository.download(artifact_uid=asset_uid, filename="{}.tar.gz".format(str(model_details['entity']['name'])).replace(' ', '_'))

        with open("{}.json".format(str(model_details['entity']['name']).replace(' ', '_')), 'w') as outfile:
            json.dump(model_details['entity']['schemas']['input'][0], outfile)





    # if deployment['entity']['name'] == 'AutoAI Iris deployment WMLv4':
    #     deployment_details = deployment
    #     deployment_uid = deployment['metadata']['guid']
    #     scoring_url = deployment['entity']['status']['online_url']
    #
    #     model_href = deployment['entity']['asset']['href']
    #     splitted_href = model_href.split('/')[3]
    #     asset_uid = splitted_href.split('?')[0] if '?' in splitted_href else splitted_href
    #     model_details = wml_client.repository.get_model_details(asset_uid)
    #     print("Model details: {}".format(model_details))
    #     print("Deployment details: {}".format(deployment))


# {
#          'metadata':{
#             'parent':{
#                'href':''
#             },
#             'guid':'0b26f820-522e-4bb1-ac55-65f1b86a9eec',
#             'modified_at':'',
#             'created_at':'2019-11-08T08:19:17.599Z',
#             'href':'/v4/deployments/0b26f820-522e-4bb1-ac55-65f1b86a9eec'
#          },
#          'entity':{
#             'name':'AutoAI Iris deployment WMLv4',
#             'custom':{
#
#             },
#             'online':{
#
#             },
#             'description':'',
#             'space':{
#                'href':'/v4/spaces/d42294f6-f114-4b10-a67b-e4c6ec04c21c'
#             },
#             'status':{
#                'state':'ready',
#                'online_url':{
#                   'url':'https://namespace1-cpd-namespace1.apps.zloct36-lb-1.fyre.ibm.com/v4/deployments/0b26f820-522e-4bb1-ac55-65f1b86a9eec/predictions'
#                }
#             },
#             'asset':{
#                'href':'/v4/models/406471d2-ae70-4435-8d99-fc84154fa46e?space_id=d42294f6-f114-4b10-a67b-e4c6ec04c21c'
#             },
#             'auto_redeploy':False
#          }
#       }