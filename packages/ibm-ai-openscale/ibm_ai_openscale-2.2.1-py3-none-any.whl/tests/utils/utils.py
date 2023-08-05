def check_if_binding_exists(ai_client, credentials, type):
    bindings = ai_client.data_mart.bindings.get_details()

    for binding in bindings['service_bindings']:
        if binding['entity']['service_type'] == type:
            if binding['entity']['credentials'] == credentials:
                print("Binding already exists: {}".format(binding))
                return binding['metadata']['guid']


def get_application_details(hrefs_v2, application_uid, headers):
    import requests
    
    response = requests.get(
        url=hrefs_v2.get_application_details_href(application_uid),
        headers=headers,
        verify=False)
    if(response.status_code == 200):
        business_app_details = response.json()
    return business_app_details