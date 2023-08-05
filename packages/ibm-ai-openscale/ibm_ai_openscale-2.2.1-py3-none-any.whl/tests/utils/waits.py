# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


from .configuration import *
from .request_handler import request_session


def _check_for_payload_logging_error_table(database, subscription_uid):
    if database is None:
        return False

    tables = database.list_tables_in_schema(schema=get_schema_name())
    payload_error_table_name = "{}_{}".format("PayloadError", subscription_uid)

    if payload_error_table_name in tables:
        return True
    else:
        return False


def _print_payload_logging_error_table_content(database, subscription_uid):
    payload_error_table_name = "{}_{}".format("PayloadError", subscription_uid)

    if _check_for_payload_logging_error_table(database, subscription_uid):
        print("{} content:".format(payload_error_table_name))
        print(database.get_table_data(schema=get_schema_name(), table=payload_error_table_name))


def _print_measurement_facts_table_content(database,):
    measurement_facts_table_name = "MeasurementFacts"

    print("{} content:".format(measurement_facts_table_name))
    print(database.get_table_data(schema=get_schema_name(), table=measurement_facts_table_name))


def wait_for_payload_table(subscription, payload_records):
    print("Waiting {} seconds for payload records on {} env".format(get_payload_timeout(), get_env()))
    rows = subscription.payload_logging.get_records_count()

    try:
        database = get_database()
    except Exception:
        print("--> Unable to set up database. Skipping check for payload error table.")
        database = None

    start_time = time.time()
    elapsed_time = 0

    while rows < payload_records and elapsed_time < get_payload_timeout():
        time.sleep(10)
        rows = subscription.payload_logging.get_records_count()

        if _check_for_payload_logging_error_table(database, subscription.uid):
            _print_payload_logging_error_table_content(database, subscription.uid)
            import unittest
            tc = unittest.TestCase()
            tc.fail("PayloadError table found for subscription: {}".format(subscription.uid))

        elapsed_time = time.time() - start_time

    if rows != payload_records:
        print("--> After {} seconds only {} of {} records stored in payload - timout !!!".format(
            get_payload_timeout(),
            rows,
            payload_records))
    else:
        print("--> All payload rows stored.")


def wait_for_performance_table(subscription):
    print("Waiting {} seconds for performance records...".format(get_performance_timeout()))
    rows = subscription.performance_monitoring._get_data_from_rest_api()

    start_time = time.time()
    elapsed_time = 0

    while len(rows) == 0 and elapsed_time < get_performance_timeout():
        time.sleep(10)
        rows = subscription.performance_monitoring._get_data_from_rest_api()
        elapsed_time = time.time() - start_time

    if len(rows) == 0:
        print("--> After {} seconds only performance table is still empty - timout !!!".format(get_performance_timeout()))
        _print_measurement_facts_table_content(database=get_database())


def wait_for_feedback_table(subscription, feedback_records):
    print("Waiting {} seconds for feedback records...".format(get_feedback_payload_timeout()))
    rows = subscription.feedback_logging._get_data_from_rest_api()

    start_time = time.time()
    elapsed_time = 0

    if isinstance(feedback_records, list):
        number_of_records = len(feedback_records)
    else:
        number_of_records = feedback_records

    while len(rows) < number_of_records and elapsed_time < get_feedback_payload_timeout():
        time.sleep(10)
        rows = subscription.feedback_logging._get_data_from_rest_api()
        elapsed_time = time.time() - start_time

    if len(rows) != number_of_records:
        print("--> After {} seconds only {} of {} feedback records stored in payload - timout !!!".format(
            get_feedback_payload_timeout(),
            len(rows),
            number_of_records))


def wait_for_payload_data_distribution(subscription, distribution_run_id):
    timeout = get_distribution_timeout()
    print("Waiting {} seconds for payload distribution {} to finish...".format(timeout, distribution_run_id))

    start_time = time.time()
    elapsed_time = 0

    run_details = None
    status = 'initializing'
    while (status == 'initializing' or status == 'running') and elapsed_time < timeout:
        run_details = subscription.payload_logging.data_distribution.get_run_details(run_id=distribution_run_id)
        status = run_details['status']
        time.sleep(5)
        elapsed_time = time.time() - start_time

    if elapsed_time >= timeout:
        print("Payload data distribution wait not finished after: {} secs".format(timeout))

    if status != 'completed':
        print("Payload data distribution failed with status: {}\nDetails:{}".format(status, run_details))


def wait_for_feedback_data_distribution(subscription, distribution_run_id):
    timeout = get_distribution_timeout()
    print("Waiting {} seconds for feedback distribution {} to finish...".format(timeout, distribution_run_id))

    start_time = time.time()
    elapsed_time = 0

    run_details = None
    status = 'initializing'
    while (status == 'initializing' or status == 'running') and elapsed_time < timeout:
        run_details = subscription.feedback_logging.data_distribution.get_run_details(run_id=distribution_run_id)
        status = run_details['status']
        time.sleep(5)
        elapsed_time = time.time() - start_time

    if elapsed_time >= timeout:
        print("Feedback data distribution wait not finished after: {} secs".format(timeout))

    if status != 'completed':
        print("Feedback data distribution failed with status: {}\nDetails:{}".format(status, run_details))


def wait_until_deleted(ai_client, binding_uid=None, subscription_uid=None, data_mart=None):
    uids_sum = sum([1 if b else 0 for b in [binding_uid, subscription_uid, data_mart]])

    if uids_sum > 1:
        raise Exception('More than one uid passed.')
    elif uids_sum == 0:
        raise Exception('No uids passed.')

    def can_be_found():
        if binding_uid is not None:
            try:
                print(ai_client.data_mart.bindings.get_details(binding_uid))
                return True
            except:
                return False
        elif subscription_uid is not None:
            try:
                print(ai_client.data_mart.subscriptions.get_details(subscription_uid))
                return True
            except:
                return False
        elif data_mart is not None:
            try:
                print(ai_client.data_mart.get_details())
                return True
            except Exception as e:
                print(e)
                return False

    import time

    print('Waiting for {} to delete...'.format(
        'binding with uid=\'{}\''.format(binding_uid) if binding_uid is not None
        else 'subscription with uid=\'{}\''.format(subscription_uid) if subscription_uid is not None
        else 'data_mart'
    ), end='')

    iterator = 0

    while can_be_found() and iterator < 20:
        time.sleep(3)
        print('.', end='')
        iterator += 1

    print(' DELETED')


def wait_for_business_app(url_get_details, headers, busines_app_timeout = 15):
    def get_details(url_get_details, headers):
        response = requests.get(url=url_get_details,
                            headers=headers, verify=False)
        if(response.status_code == 200):
            business_app_details = response.json()
        return business_app_details

    business_app_details = get_details(url_get_details, headers)
    start_time = time.time()
    elapsed_time = 0

    while business_app_details['entity']['status']['state'] != 'active' and elapsed_time < busines_app_timeout:
        time.sleep(1)
        business_app_details = get_details(url_get_details, headers)
        elapsed_time = time.time() - start_time

    if elapsed_time >= busines_app_timeout:
        print("Waiting for business application details more than {} seconds - TIMEOUT".format(elapsed_time))

    return business_app_details

def wait_for_business_app_client (ai_client, application_id,  busines_app_timeout = 15):

    business_app_details = ai_client.data_mart.applications.get_details(application_id)
    start_time = time.time()
    elapsed_time = 0

    while business_app_details['entity']['status']['state'] != 'active' and elapsed_time < busines_app_timeout:
        time.sleep(2)
        business_app_details = ai_client.data_mart.applications.get_details(application_id)
        elapsed_time = time.time() - start_time
        
    if elapsed_time >= busines_app_timeout:
        print("Waiting for business application details more than {} seconds - TIMEOUT".format(elapsed_time))

    return business_app_details


def wait_for_records_in_data_set(url_get_data_set_records, headers, data_set_records, waiting_timeout = 75):

    def get_data_set_records(url_get_data_set_records, headers):
        if 'include_total_count' not in url_get_data_set_records:
            additional_sign = '?' if '?' not in url_get_data_set_records else '&'
            url = url_get_data_set_records+additional_sign+'include_total_count=true'
        else:
            url = url_get_data_set_records
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()['total_count']
        else:
            print(response.status_code)
            print(response.json())
            return response.json()

    data_set_records_count = get_data_set_records(url_get_data_set_records, headers)
    start_time = time.time()
    elapsed_time = 0

    while data_set_records_count < data_set_records and elapsed_time < waiting_timeout:
        time.sleep(10)
        data_set_records_count = get_data_set_records(url_get_data_set_records, headers)
        elapsed_time = time.time() - start_time

    if data_set_records_count < data_set_records:
        print("Loaded only {} records in {} sec - TIMEOUT".format(data_set_records_count, elapsed_time))

    return data_set_records_count


def wait_for_dataset(dataset_url, headers, waiting_timeout=120):
    start_time = time.time()
    elapsed_time = 0
    status = ""
    dataset_details = ""

    while status != 'active' and elapsed_time < waiting_timeout:
        time.sleep(5)
        response = requests.get(
            dataset_url,
            headers=headers,
            verify=False
        )
        dataset_details = response.json()
        status = dataset_details['entity']['status']['state']

        elapsed_time = time.time() - start_time

    if status != 'active':
        print("Dataset status {} is different than active after {} sec - TIMEOUT".format(status, waiting_timeout))

    return dataset_details


def wait_for_monitor_instance(run_url, headers, run_id=None,  waiting_timeout=430):
    if run_id is not None:
        run_url = run_url + "/" + run_id

    def get_run_details(url, headers):
        response = request_session.get(
            url=url,
            headers=headers
        )
        return response.json()

    run_monitor_details = get_run_details(run_url, headers)
    status = run_monitor_details['entity']['status']['state']

    start_time = time.time()
    elapsed_time = 0

    while status != 'finished' and elapsed_time < waiting_timeout and status != 'error':
        time.sleep(5)
        run_monitor_details = get_run_details(run_url, headers)
        status = run_monitor_details['entity']['status']['state']
        elapsed_time = time.time() - start_time

    if elapsed_time >= waiting_timeout:
        print("Metrics calculation timeout, waiting more than: {} \n RUN MONITOR DETAILS: {}".format(
            elapsed_time, run_monitor_details))
    return run_monitor_details


def wait_for_measurements(measurements_url, no_measurements, headers):
    waiting_timeout = 60
    start_time = time.time()
    elapsed_time = 0
    measurements_records = 0
    while measurements_records < no_measurements and elapsed_time < waiting_timeout:
        response = request_session.get(url=measurements_url, headers=headers)
        if response.status_code == 200:
            measurements_records = len(response.json()['measurements'])
        else:
            print("Get measurements failed with error: {}".format(response.text))
        time.sleep(5)
        elapsed_time = time.time() - start_time

    if elapsed_time >= waiting_timeout:
        print("Measurement wait timeout")

    return response.json()


def wait_for_v2_performance_measurements(measurements_url, no_request, headers):
    waiting_timeout = 60
    start_time = time.time()
    elapsed_time = 0
    records_count = 0
    while records_count < no_request and elapsed_time < waiting_timeout:
        response = request_session.get(url=measurements_url, headers=headers)
        if response.status_code != 200:
            continue

        records_count = 0
        result = response.json()
        for measurement in result['measurements']:
            for value in measurement["entity"]["values"]:
                for metric in value["metrics"]:
                    if metric["id"] == "record_count":
                        records_count += metric["value"]
        time.sleep(5)
        elapsed_time = time.time() - start_time

    if elapsed_time >= waiting_timeout:
        print("Measurement wait timeout")

    return records_count


def wait_for_quality_metrics(subscription, no_metrics=1):
    waiting_timeout = 60
    start_time = time.time()
    elapsed_time = 0
    records_count = 0
    metrics = None
    while records_count < no_metrics and elapsed_time < waiting_timeout:
        time.sleep(10)
        metrics = subscription.quality_monitoring.get_metrics()
        records_count = len(metrics)
        elapsed_time = time.time() - start_time

    if elapsed_time >= waiting_timeout:
        print("wait_for_metrics_method timeouted")

    return metrics
