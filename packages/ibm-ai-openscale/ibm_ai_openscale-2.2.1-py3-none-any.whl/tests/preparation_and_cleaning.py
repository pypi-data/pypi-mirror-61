# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import io
import json
import os
import sys
import time
import requests
import uuid
from configparser import ConfigParser
from datetime import datetime, timedelta

import ibm_boto3

import psycopg2
from db2rest_utils import cleanupdb2
from ibm_botocore.client import Config
from psycopg2.sql import Identifier, SQL
from pytz import timezone


yesterday = datetime.now(timezone('UTC')) - timedelta(days=1)


if "ENV" in os.environ:
    environment = os.environ['ENV']
else:
    environment = "YP_QA"

print('Used environment:', environment)

if "QUICKRUN" in os.environ:
    suite_config = "CONFIG_QUICKRUN"
    quick_run = True
    print('Quick run selected. All timeouts are reduced and assets ids are fiexed.')
else:
    suite_config = "CONFIG"
    quick_run = False


if "icp" in str(environment).lower() or "db2" in str(environment).lower():
    import ibm_db

if "TEST_DIR" in os.environ:
    configDir = os.environ['TEST_DIR'] + "config.ini"
else:
    configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


def get_env():
    return environment


def get_schema_name():
    return config.get(environment, 'schema_name')


def get_schema_name2():
    return config.get(environment, 'schema_name2')


def get_aios_credentials():
    return json.loads(config.get(environment, 'aios_credentials'))


def get_aios_lite_credentials():
    if config.has_option(environment, 'aios_lite_credentials'):
        return json.loads(config.get(environment, 'aios_lite_credentials'))
    else:
        return None


def is_quickrun_enabled():
    return quick_run


def get_spss_cnds_credentials():
    return json.loads(config.get('SPSS_CNDS_ENV', 'credentials'))


def get_payload_timeout():
    if "SANITY" in str(get_env()):
        json.loads(config.get(suite_config, 'payload_timeout')) * 4

    return json.loads(config.get(suite_config, 'payload_timeout'))


def get_performance_timeout():
    if "SANITY" in str(get_env()):
        json.loads(config.get(suite_config, 'performance_timeout')) * 4

    return json.loads(config.get(suite_config, 'performance_timeout'))


def get_feedback_payload_timeout():
    return json.loads(config.get(suite_config, 'feedback_payload_timeout'))


def get_wml_payload_timeout():
    if "SANITY" in str(get_env()):
        json.loads(config.get(suite_config, 'payload_timeout')) * 6

    if "CR" in get_env():
        json.loads(config.get(suite_config, 'payload_timeout')) * 3

    return json.loads(config.get(suite_config, 'payload_timeout'))


def get_quality_run_timeout():
    if "SANITY" in str(get_env()):
        return json.loads(config.get(suite_config, 'quality_run_timeout')) * 4

    if "CR" in get_env():
        return json.loads(config.get(suite_config, 'quality_run_timeout')) * 3

    return json.loads(config.get(suite_config, 'quality_run_timeout'))


def get_3rd_payload_timeout():
    return json.loads(config.get(suite_config, 'payload_timeout'))


def wait_for_payload_table(subscription, payload_records):
    print("Waiting {} seconds for payload records on {} env".format(get_payload_timeout(), get_env()))
    rows = subscription.payload_logging.get_records_count()

    start_time = time.time()
    elapsed_time = 0

    while rows < payload_records and elapsed_time < get_payload_timeout():
        time.sleep(10)
        rows = subscription.payload_logging.get_records_count()
        elapsed_time = time.time() - start_time

    if rows != payload_records:
        print("--> After {} seconds only {} of {} records stored in payload - timout !!!".format(
            get_payload_timeout(),
            rows,
            payload_records))


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


def wait_for_feedback_table(subscription, feedback_records):
    print("Waiting {} seconds for feedback records...".format(get_feedback_payload_timeout()))
    rows = subscription.feedback_logging._get_data_from_rest_api()

    start_time = time.time()
    elapsed_time = 0

    while len(rows) != feedback_records and elapsed_time < get_feedback_payload_timeout():
        time.sleep(5)
        rows = subscription.feedback_logging._get_data_from_rest_api()
        elapsed_time = time.time() - start_time

    if len(rows) != feedback_records:
        print("--> After {} seconds only {} of {} feedback records stored in payload - timout !!!".format(
            get_feedback_payload_timeout(),
            len(rows),
            feedback_records))


def wait_for_payload_propagation(is_wml_engine=True):
    if is_wml_engine:
        timeout = get_wml_payload_timeout()
    else:
        timeout = get_3rd_payload_timeout()
    print("Waiting {} seconds for payload propagation...".format(timeout))
    time.sleep(timeout)


def get_database_credentials():
    if config.has_option(environment, 'database_credentials'):
        return json.loads(config.get(environment, 'database_credentials'))
    elif config.has_option(environment, 'postgres_credentials'):
        return get_postgres_credentials()
    elif config.has_option(environment, 'db2_datamart'):
        return get_db2_datamart_credentials()
    else:
        raise Exception("There is no database in config!")


def is_postgres_database():
    db_credentials = get_database_credentials()

    if "connection" in db_credentials.keys() and "postgres" in db_credentials['connection'].keys():
        return True

    if "db_type" in db_credentials.keys() and "postgresql" == db_credentials['db_type']:
        return True

    if 'postgres' in str(db_credentials):
        return True

    if 'dashdb' in str(db_credentials):
        return False

    if 'db2' in str(db_credentials):
        return False

    return False


def get_db2_datamart_credentials():
    return json.loads(config.get(environment, 'db2_datamart'))


def get_db2_schema_name():
    return json.loads(config.get(environment, 'db2_schema'))


def get_wml_credentials(env=environment):
    return json.loads(config.get(env, 'wml_credentials'))


def get_wml_credentials_other_icp(env=environment):
    return json.loads(config.get(env, 'wml_credentials_other_icp'))


def get_wml_lite_credentials():
    return json.loads(config.get(environment, 'wml_lite_credentials'))


def get_postgres_credentials():
    return json.loads(config.get(environment, 'postgres_credentials'))


def get_cos_credentials():
    return json.loads(config.get(environment, 'cos_credentials'))


def get_feedback_data_reference():
    return json.loads(config.get(environment, 'feedback_data_reference'))


def get_db2_credentials():
    return json.loads(config.get(environment, 'db2_reference'))


def get_spark_reference():
    return json.loads(config.get(environment, 'spark_reference'))


def get_cos_auth_endpoint():
    return config.get(environment, 'cos_auth_endpoint')


def get_cos_service_endpoint():
    return config.get(environment, 'cos_service_endpoint')


def get_client():
    wml_lib = __import__('watson_machine_learning_client', globals(), locals())
    return wml_lib.WatsonMachineLearningAPIClient(get_wml_credentials())


def get_wml_instance_plan(wml_credentials):
    wml_lib = __import__('watson_machine_learning_client', globals(), locals())
    wml_client = wml_lib.WatsonMachineLearningAPIClient(wml_credentials)
    wml_instance_details = wml_client.service_instance.get_details()
    return wml_instance_details['entity']['plan']


def get_cos_resource():
    cos_credentials = get_cos_credentials()
    api_key = cos_credentials['apikey']
    service_instance_id = cos_credentials['resource_instance_id']
    auth_endpoint = get_cos_auth_endpoint()
    service_endpoint = get_cos_service_endpoint()

    cos = ibm_boto3.resource(
        's3',
        ibm_api_key_id = api_key,
        ibm_service_instance_id = service_instance_id,
        ibm_auth_endpoint = auth_endpoint,
        config = Config(signature_version='oauth'),
        endpoint_url = service_endpoint
    )

    return cos


def prepare_cos(cos_resource, bucket_prefix='wml-test'):
    import datetime

    postfix = datetime.datetime.now().isoformat().replace(":", "-").split(".")[0].replace("T", "-")

    bucket_names = {
        'data': '{}-{}-data-{}'.format(bucket_prefix, environment.lower().replace('_', '-'), postfix),
        'results': '{}-{}-results-{}'.format(bucket_prefix, environment.lower().replace('_', '-'), postfix)
    }

    cos_resource.create_bucket(Bucket=bucket_names['data'])
    cos_resource.create_bucket(Bucket=bucket_names['results'])

    return bucket_names


def get_cos_training_data_reference(bucket_names):
    cos_credentials = get_cos_credentials()
    service_endpoint = get_cos_service_endpoint()

    return {
        "connection": {
            "endpoint_url": service_endpoint,
            "access_key_id": cos_credentials['cos_hmac_keys']['access_key_id'],
            "secret_access_key": cos_credentials['cos_hmac_keys']['secret_access_key']
        },
        "source": {
            "bucket": bucket_names['data'],
        },
        "type": "s3"
    }


def get_cos_training_results_reference(bucket_names):
    cos_credentials = get_cos_credentials()
    service_endpoint = get_cos_service_endpoint()

    return {
        "connection": {
            "endpoint_url": service_endpoint,
            "access_key_id": cos_credentials['cos_hmac_keys']['access_key_id'],
            "secret_access_key": cos_credentials['cos_hmac_keys']['secret_access_key']
        },
        "target": {
            "bucket": bucket_names['results'],
        },
        "type": "s3"
    }


def clean_cos_bucket(cos_resource, bucket_name):
    bucket_obj = cos_resource.Bucket(bucket_name)
    for upload in bucket_obj.multipart_uploads.all():
        upload.abort()
    for o in bucket_obj.objects.all():
        o.delete()
    bucket_obj.delete()


def clean_cos(cos_resource, bucket_names):
    clean_cos_bucket(cos_resource, bucket_names['data'])
    clean_cos_bucket(cos_resource, bucket_names['results'])


def clean_env(cos_resource=None, threshold_date=yesterday, raise_when_not_empty=False, database="postgres"):
    rm_els_no = 0

    from ibm_ai_openscale import APIClient
    ai_client = APIClient(get_aios_credentials())
    for uid in ai_client.data_mart.subscriptions.get_uids():
        subscription = ai_client.data_mart.subscriptions.get(uid)
        if subscription.get_details()['metadata']['created_at'] < threshold_date.isoformat():
            print('Deleting \'{}\' subscription.'.format(uid))
            try:
                ai_client.data_mart.subscriptions.delete(uid)
            except Exception as e:
                print('Deleting of subscription failed:', e)

    client = get_client()

    rm_els_no += clean_experiments(client, threshold_date)
    rm_els_no += clean_training_runs(client, threshold_date)
    rm_els_no += clean_definitions(client, threshold_date)
    rm_els_no += clean_models(client, threshold_date)
    rm_els_no += clean_deployments(client, threshold_date)
    try:
        rm_els_no += clean_ai_functions(client, threshold_date)
        rm_els_no += clean_runtimes(client, threshold_date)
        rm_els_no += clean_custom_libraries(client, threshold_date)
    except:
        pass

    if cos_resource is not None:
        for bucket in cos_resource.buckets.all():
            if 'wml-test-' in bucket.name and bucket.creation_date < threshold_date:
                rm_els_no +=1
                print('Deleting \'{}\' bucket.'.format(bucket.name))
                try:
                    for upload in bucket.multipart_uploads.all():
                        upload.abort()
                    for o in bucket.objects.all():
                        o.delete()
                    bucket.delete()
                except Exception as e:
                    print("Exception during bucket deletion occured: " + str(e))

    if raise_when_not_empty and rm_els_no > 0:
        raise Exception('Non zero number of elements to clean: {}'.format(rm_els_no))

    try:
        ai_client = APIClient(get_aios_credentials())
        try:
            for uid in ai_client.data_mart.bindings.get_uids():
                ai_client.data_mart.bindings.delete(uid)
        except:
            pass

        try:
            ai_client.data_mart.delete()
        except:
            pass
    except:
        pass

    if database == "postgres":
        clean_postgress_instance()
        set_up_postgress_instance()
    elif database == "db2":
        clean_db2_schema(get_db2_datamart_credentials(), get_db2_schema_name())
    elif database == "all":
        clean_postgress_instance()
        set_up_postgress_instance()
        clean_db2_schema(get_db2_datamart_credentials(), get_db2_schema_name())
    else:
        raise Exception("Database {} not supported!".format(database))


def prepare_env(ai_client, internal=False):
    for uid in ai_client.data_mart.subscriptions.get_uids():
        print('Deleting \'{}\' subscription.'.format(uid))
        try:
            ai_client.data_mart.subscriptions.delete(uid)
        except Exception as e:
            print('Deleting of subscription failed:', e)

    for uid in ai_client.data_mart.bindings.get_uids():
        try:
            ai_client.data_mart.bindings.delete(uid)
        except:
            pass
    try:
        ai_client.data_mart.delete()
    except:
        pass

    if internal:
        return

    db_credentials = get_database_credentials()
    schema_name = get_schema_name()

    if "postgres" in str(db_credentials):
        delete_schema(db_credentials, schema_name)
        create_schema(db_credentials, schema_name)

    elif "db2" in str(db_credentials):
        clean_db2_database(db2_credentials=db_credentials, db2_schema=schema_name)

    # if "ICP" in get_env():
    #     if "bluemix.net" in str(db_credentials):
    #         clean_db2_schema(db_credentials, schema_name)
    #     else:
    #         clean_db2_icp_schema(db_credentials, schema_name)
    # else:
    #     if 'postgres' in str(db_credentials):
    #         delete_schema(db_credentials, schema_name)
    #         create_schema(db_credentials, schema_name)
    #     elif 'db2' in db_credentials['uri']:
    #         cleaned_db2 = False
    #         try:
    #             clean_db2_schema(db_credentials, schema_name)
    #             cleaned_db2 = True
    #         except Exception:
    #             pass
    #
    #         if not cleaned_db2:
    #             try:
    #                 time.sleep(30)
    #                 clean_db2_schema(db_credentials, schema_name)
    #             except Exception:
    #                 pass
    #     else:
    #         raise Exception("Database {} not supported!".format(db_credentials))


def clean_postgress_instance():
    delete_schema(get_postgres_credentials(), get_schema_name())
    delete_schema(get_postgres_credentials(), get_schema_name2())


def set_up_postgress_instance():
    create_schema(get_postgres_credentials(), get_schema_name())
    create_schema(get_postgres_credentials(), get_schema_name2())


def clean_wml_assets(details, delete, asset_name, threshold_date=yesterday):

    number_of_assets = 0

    for asset_details in details['resources']:
        if asset_details['metadata']['created_at'] < threshold_date.isoformat():
            number_of_assets += 0
            print('Deleting \'{}\' {}.'.format(asset_details['metadata']['guid'], asset_name))
            try:
                delete(asset_details['metadata']['guid'])
            except Exception as e:
                print('Deletion of {} failed:'.format(asset_name), e)

    return number_of_assets


def clean_repository_assets(client, details, asset_name, threshold_date=yesterday):
    return clean_wml_assets(details, client.repository.delete, asset_name, threshold_date)


def clean_models(client, threshold_date=yesterday):
    return clean_repository_assets(client, client.repository.get_model_details(), 'model', threshold_date)


def clean_definitions(client, threshold_date=yesterday):
    return clean_repository_assets(client, client.repository.get_definition_details(), 'definition', threshold_date)


def clean_deployments(client, threshold_date=yesterday):
    return clean_wml_assets(client.deployments.get_details(), client.deployments.delete, 'deployment', threshold_date)


def clean_experiments(client, threshold_date=yesterday):
    return clean_repository_assets(client, client.repository.get_experiment_details(), 'experiment', threshold_date)


def clean_training_runs(client, threshold_date=yesterday):
    return clean_wml_assets(client.training.get_details(), client.training.delete, 'training run', threshold_date)


def clean_runtimes(client, threshold_date=yesterday):
    return clean_repository_assets(client, client.runtimes.get_details(), 'runtimes', threshold_date)


def clean_custom_libraries(client, threshold_date=yesterday):
    return clean_wml_assets(client.runtimes.get_library_details(), client.runtimes.delete_library, 'custom library', threshold_date)


def clean_ai_functions(client, threshold_date=yesterday):
    return clean_repository_assets(client, client.repository.get_function_details(), 'python function', threshold_date)


def run_monitor(client, experiment_run_uid, queue):
    stdout_ = sys.stdout
    captured_output = io.StringIO()  # Create StringIO object
    sys.stdout = captured_output  # and redirect stdout.
    client.experiments.monitor_logs(experiment_run_uid)
    sys.stdout = stdout_  # Reset redirect.

    print(captured_output.getvalue())

    queue.put(captured_output.getvalue())


def run_monitor_metrics(client, experiment_run_uid, queue):
    stdout_ = sys.stdout
    captured_output = io.StringIO()  # Create StringIO object
    sys.stdout = captured_output  # and redirect stdout.
    client.experiments.monitor_metrics(experiment_run_uid)
    sys.stdout = stdout_  # Reset redirect.

    print(captured_output.getvalue())

    queue.put(captured_output.getvalue())


def run_monitor_training(client, training_run_uid, queue):
    stdout_ = sys.stdout
    captured_output = io.StringIO()  # Create StringIO object
    sys.stdout = captured_output  # and redirect stdout.
    client.training.monitor_logs(training_run_uid)
    sys.stdout = stdout_  # Reset redirect.

    print(captured_output.getvalue())

    queue.put(captured_output.getvalue())


def prepare_connection_postgres(postgres_credentials):

    if 'uri' in postgres_credentials.keys():
        uri = postgres_credentials['uri']

        import re
        res = re.search('^[0-9a-zA-Z]+://([0-9a-zA-Z]+):([0-9a-zA-Z]+)@([^:]+):([0-9]+)/([0-9a-zA-Z]+)$', uri)

        if res is None:
            raise Exception('Unexpected format of db uri: {}'.format(uri))

        username = res.group(1)
        password = res.group(2)
        host = res.group(3)
        port = res.group(4)
        database = res.group(5)

        return psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=host,
            port=port
        )
    elif 'connection' in postgres_credentials.keys():
        pstg_connection = postgres_credentials['connection']['postgres']
        conn_str = "host='{}' port='{}' dbname='{}' user='{}' password='{}' sslmode='require'".format(pstg_connection['hosts'][0]['hostname'], pstg_connection['hosts'][0]['port'],
                                                                                                      pstg_connection['database'], pstg_connection['authentication']['username'],
                                                                                                      pstg_connection['authentication']['password'])
        return psycopg2.connect(conn_str)

def create_schema(postgres_credentials, schema_name):
    try:
        execute_sql_query(SQL("CREATE SCHEMA {}").format(Identifier(schema_name)), postgres_credentials)
    except psycopg2.Error as ex:
        print("Unable to create schema {}. Reason:\n{}".format(schema_name, ex.pgerror))

#
def delete_schema(postgres_credentials, schema_name):
    try:
        execute_sql_query(SQL("DROP SCHEMA {} CASCADE").format(Identifier(schema_name)), postgres_credentials)
        print("Schema {} dropped.".format(schema_name))
    except psycopg2.Error:
        print("Schema {} does not exist.".format(schema_name))


def delete_db2_schema(db2_credentials, schema_name):
    execute_db2_sql_query("DROP SCHEMA {} CASCADE".format(schema_name), db2_dsn=db2_credentials['dsn'])


def clean_db2_icp_schema(db2_credentials, schema_name):
    result = execute_db2_sql_query(""" select 'DROP TABLE "'||rtrim(tabschema)||'"."'||rtrim(tabname)||'"' from syscat.tables where OWNER = 'DB2INST1' and TABSCHEMA = '{}' and type = 'T' """.format(schema_name),  db2_dsn=db2_credentials['dsn'])
    for query in result:
        execute_db2_sql_query(query,  db2_dsn=db2_credentials['dsn'])


def clean_db2_schema(db2_credentials, schema_name):
    for query in list(map(lambda table: """ DROP TABLE "{}"; """.format(table), list_db2_tables(db2_credentials=db2_credentials, schema_name=schema_name))):
       execute_db2_sql_query(query, db2_dsn=db2_credentials['dsn'])


def list_db2_tables(db2_credentials, schema_name):
    query_result = execute_db2_sql_query(""" SELECT tabname FROM syscat.tables WHERE owner='{}' AND type='T' """.format(schema_name), db2_dsn=db2_credentials['dsn'])
    db2_tables = []
    for record in query_result:
        db2_tables.append(record)

    return db2_tables


def print_schema_tables_info(postgres_credentials, schema_name):
    rows = execute_sql_query("SELECT * FROM information_schema.tables WHERE table_schema = '{}'".format(schema_name), postgres_credentials)
    query_rows = []
    for row in rows:
        query_rows.append(row)

    return query_rows


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


def execute_sql_query(query, postgres_credentials=None, db2_credentials=None):
    # delete the function
    if postgres_credentials is not None:
        conn = prepare_connection_postgres(postgres_credentials=postgres_credentials)
    else:
        raise Exception("Credentials are not supported.")

    cursor = conn.cursor()
    cursor.execute(query)

    try:
        query_result = cursor.fetchall()
    except psycopg2.ProgrammingError as ex:
        query_result = ""

    conn.commit()
    cursor.close()
    conn.close()

    return query_result


def upload_german_risk_training_data_to_postgres(postgres_credentials):
    try:
        execute_sql_query(""" SELECT * FROM {}.CreditRiskTable LIMIT 1 """.format("trainingdataschema"), postgres_credentials=postgres_credentials)
        return
    except psycopg2.ProgrammingError:
        print("Table does not exist. Creating new schema and table.")

    try:
        create_schema(postgres_credentials, "trainingdataschema")
    except psycopg2.ProgrammingError:
        print("Schema already exist.")

    try:
        execute_sql_query("""
                CREATE TABLE {}.{}(
                    CheckingStatus text,
                    LoanDuration integer,
                    CreditHistory text,
                    LoanPurpose text,
                    LoanAmount integer,
                    ExistingSavings text,
                    EmploymentDuration text,
                    InstallmentPercent integer,
                    Sex text,
                    OthersOnLoan text,
                    CurrentResidenceDuration integer,
                    OwnsProperty text,
                    Age integer,
                    InstallmentPlans text,
                    Housing text,
                    ExistingCreditsCount integer,
                    Job text,
                    Dependents integer,
                    Telephone text,
                    ForeignWorker text,
                    Risk text
                )
                """.format("trainingdataschema", "CreditRiskTable"), postgres_credentials=postgres_credentials)

    except psycopg2.ProgrammingError as ex:
        print("Unable to create new table!")
        print(ex)

    try:
        conn = prepare_connection_postgres(postgres_credentials)
        conn.autocommit = True
        cursor = conn.cursor()
        with open(os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'), 'r') as f:
            next(f)
            cursor.copy_from(file=f, table='{}.CreditRiskTable'.format("trainingdataschema"), sep=',')
        cursor.close()
        conn.close()
    except psycopg2.ProgrammingError as ex:
        print("Unable to upload content from CSV to postgres table")
        print(ex)

    try:
        result = execute_sql_query(""" SELECT * FROM {}.CreditRiskTable LIMIT 1 """.format("trainingdataschema"), postgres_credentials=postgres_credentials)
        print("Table content:\n{}".format(result))
        return
    except psycopg2.ProgrammingError as ex:
        print("Error during table creation!")
        raise ex


def upload_go_sales_training_data_to_postgres(postgres_credentials):
    try:
        execute_sql_query(""" SELECT * FROM {}.GoSalesTable LIMIT 1 """.format("trainingdataschema"), postgres_credentials=postgres_credentials)
        return
    except psycopg2.ProgrammingError:
        print("Table does not exist. Creating new schema and table.")

    try:
        create_schema(postgres_credentials, "trainingdataschema")
    except psycopg2.ProgrammingError:
        print("Schema already exist.")

    try:
        execute_sql_query("""
                CREATE TABLE {}.{}(
                    PRODUCT_LINE text,
                    GENDER text,
                    AGE integer,
                    MARITAL_STATUS text,
                    PROFESSION text
                )
                """.format("trainingdataschema", "GoSalesTable"), postgres_credentials=postgres_credentials)

    except psycopg2.ProgrammingError as ex:
        print("Unable to create new table!")
        print(ex)

    try:
        conn = prepare_connection_postgres(postgres_credentials)
        conn.autocommit = True
        cursor = conn.cursor()
        with open(os.path.join(os.curdir, 'datasets', 'GoSales', 'GoSales_Tx_NaiveBayes.csv'), 'r') as f:
            next(f)
            cursor.copy_from(file=f, table='{}.GoSalesTable'.format("trainingdataschema"), sep=',')
        cursor.close()
        conn.close()
    except psycopg2.ProgrammingError as ex:
        print("Unable to upload content from CSV to postgres table")
        print(ex)

    try:
        result = execute_sql_query(""" SELECT * FROM {}.GoSalesTable LIMIT 1 """.format("trainingdataschema"), postgres_credentials=postgres_credentials)
        print("Table content:\n{}".format(result))
        return
    except psycopg2.ProgrammingError as ex:
        print("Error during table creation!")
        raise ex


def export_datamart_config_to_json(ai_client):
    import requests
    response = requests.get(url="{}/{}".format(ai_client._href_definitions.get_data_mart_href(), 'file'), headers=ai_client._get_headers())

    return response.json()


def get_wml_model_and_deployment_id(model_name, deployment_name):
    wml_client = get_client()

    for deployment in wml_client.deployments.get_details()['resources']:
        if deployment['entity']['name'] == deployment_name:
            print("--> Deployment already exists: {}".format(deployment))
            return deployment['entity']['deployable_asset']['guid'], deployment['metadata']['guid']

    return None, None


def clean_wml_instance(model_id, deployment_id, binding_id=None):
    print("Cleaning WML instance ...")
    if binding_id is not None:
        from ibm_ai_openscale import APIClient
        ai_client = APIClient(get_aios_credentials())
        wml_client = ai_client.data_mart.bindings.get_native_engine_client(binding_id)
    else:
        wml_client = get_client()

    print("Deleting deployment: {}".format(deployment_id))
    wml_client.deployments.delete(deployment_id)

    print("Deleting model: {}".format(model_id))
    wml_client.repository.delete(model_id)

    # if "ICP" in get_env():
    #     clean_up_wml_instance()


def clean_up_wml_instance():
    wml_client = get_client()

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


def clean_up_wml_instance_spss(wml_client):
    env_clean = False
    try:
        details = wml_client.repository.get_details()

        for deployment in details['deployments']['resources']:
            if "spss" in str(deployment['entity']['runtime_environment']).lower():
                print("Removing spss deployment: {}".format(deployment))
                wml_client.deployments.delete(deployment['metadata']['guid'])

        for model in details['models']['resources']:
            if "spss" in str(model['entity']['runtime_environment']).lower():
                print("Removing spss model: {}".format(model))
                wml_client.repository.delete(model['metadata']['guid'])

        env_clean = True

    except Exception as ex:
        print("First cleanup failed. Trying the second approach\n{}".format(ex))

    if not env_clean:
        try:
            models = wml_client._models.get_details()
            deployments = wml_client.deployments.get_details()

            for deployment in deployments['resources']:
                if "spss" in str(deployment['entity']['runtime_environment']).lower():
                    print("Removing spss deployment: {}".format(deployment))
                    wml_client.deployments.delete(deployment['metadata']['guid'])

            for model in models['resources']:
                if "spss" in str(model['entity']['runtime_environment']).lower():
                    print("Removing spss model: {}".format(model))
                    wml_client.repository.delete(model['metadata']['guid'])

        except Exception as ex:
            print("Second cleanup failed.\n{}".format(ex))


def clean_db2_database(db2_credentials, db2_schema):

    if "icp" in str(get_env()).lower():
        if 'dsn' in db2_credentials.keys():
            db2_dsn = db2_credentials["dsn"]
        else:
            db2_dsn = db2_credentials['ssldsn']

        tables_drop_query = execute_db2_sql_query(query= """ select 'DROP TABLE "'||rtrim(tabschema)||'"."'||rtrim(tabname)||'"' from syscat.tables where OWNER = 'DB2INST1' and TABSCHEMA = '{}' and type = 'T' """.format(db2_schema), db2_dsn=db2_dsn)
        views_drop_query = execute_db2_sql_query(query=""" select 'DROP VIEW "'||rtrim(tabschema)||'"."'||rtrim(tabname)||'"' from syscat.tables where OWNER = 'DB2INST1' and TABSCHEMA = '{}' and type = 'V' """.format(db2_schema), db2_dsn=db2_dsn)

        for table_query in tables_drop_query:
            execute_db2_immediately_query(query=table_query, db2_dsn=db2_dsn)

        for view_query in views_drop_query:
            execute_db2_immediately_query(query=view_query, db2_dsn=db2_dsn)

    else:
        cleanupdb2(db2_credentials)
        # tables = execute_db2_sql_query(query="SELECT tabname FROM syscat.tables WHERE owner='{}' AND type='T' ".format(db2_schema), db2_dsn=db2_dsn)
        # views = execute_db2_sql_query(query="SELECT tabname FROM syscat.tables WHERE owner='{}' AND type='V' ".format(db2_schema), db2_dsn=db2_dsn)
        # for table in tables:
        #     execute_db2_immediately_query(query="""DROP TABLE "{}";""".format(table), db2_dsn=db2_dsn)
        #
        # for view in views:
        #     execute_db2_immediately_query(query="""DROP VIEW "{}";""".format(view), db2_dsn=db2_dsn)


def upload_credit_risk_training_data_to_db2(db2_credentials):
    db2_dsn = db2_credentials["dsn"]
    db2_uri = db2_credentials["uri"]
    if "icp" in str(get_env()).lower():
        schemas_list = execute_db2_sql_query(query= """ select schemaname from syscat.schemata """, db2_dsn=db2_dsn)

        if "TRAININGDATA" in schemas_list:
            print("Training data schema exists")
            return
            # execute_db2_immediately_query(query=""" drop schema TRAININGDATA restrict""", db2_dsn=db2_dsn)


        print("Creating schema")
        execute_db2_immediately_query(query=""" create schema TRAININGDATA """, db2_dsn=db2_dsn)

        import sqlalchemy
        import pandas as pd
        import ibm_db_sa

        engine = sqlalchemy.create_engine('ibm_db_sa:{}'.format(db2_uri[4:]))

        df = pd.read_csv("datasets/German_credit_risk/credit_risk_training_500.csv")
        df.to_sql(name="CREDIT_RISK_TRAINING", con=engine, schema="TRAININGDATA", index=False, if_exists="replace")

        print("Training data uploaded successfully.")


def execute_db2_sql_query(query, db2_dsn):
    results_array = []

    connection = ibm_db.connect(db2_dsn, "", "")
    statement = ibm_db.prepare(connection, query)

    try:
        res = ibm_db.execute(statement)
        result_dict = ibm_db.fetch_tuple(statement)

        while result_dict is not False:
            results_array.append(result_dict[0])
            result_dict = ibm_db.fetch_tuple(statement)
    except Exception as ex:
        print("SQL execution failed:")
        print(ex)
    finally:
        ibm_db.close(connection)

    return results_array


def execute_db2_immediately_query(query, db2_dsn):
    connection = ibm_db.connect(db2_dsn, "", "")
    try:
        ibm_db.exec_immediate(connection, query)
    except Exception as ex:
        print("SQL immediately execution failed:")
        print(ex)
    finally:
        ibm_db.close(connection)


def get_details_from_restapi(ai_client, binding_uid):
    import requests
    response = requests.get(ai_client._href_definitions.get_ml_gateway_discovery_href(binding_uid=binding_uid), headers=ai_client._get_headers())
    print("Request url: {}".format(ai_client._href_definitions.get_ml_gateway_discovery_href(binding_uid=binding_uid)))
    print("Request header: {}".format(ai_client._get_headers()))
    print("Response code: {}".format(response.status_code))
    print("Response text: {}".format(response.json()))


def get_iam_token(env, apikey):
    import requests

    apikey = apikey

    url = "https://iam.bluemix.net/oidc/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    IBM_cloud_IAM_uid = "bx"
    IBM_cloud_IAM_pwd = "bx"
    response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
    iam_token = response.json()["access_token"]

    return iam_token


def score_log_payload_auto_ai(subscription_details, wml_credentials, payload_scoring, payload_store_function, scoring_records=10):
    from ibm_ai_openscale.supporting_classes.payload_record import PayloadRecord
    iam_token = get_iam_token(env="YP", apikey=wml_credentials['apikey'])
    ml_instance_id = wml_credentials['instance_id']
    print("Scoring payload: {}".format(payload_scoring))
    records_list = []
    for i in range(0, int(scoring_records)):
        request, response, response_time = score_auto_ai(payload_scoring, subscription_details, iam_token,
                                                         ml_instance_id)
        records_list.append(PayloadRecord(request=request, response=response, response_time=response_time))
    print("Scored {} times with received response: ".format(scoring_records))
    print(response)
    # Log payload with Payload API:
    payload_store_function(records=records_list)


def score_auto_ai(payload_scoring, subscription_details, iam_token, ml_instance_id):
    scoring_endpoint = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token,
              'ML-Instance-ID': ml_instance_id}
    start_time = time.time()
    response_scoring = requests.post(
       url=scoring_endpoint,
       json=payload_scoring,
       headers=header)
    response_time = int(time.time() - start_time)

    return payload_scoring['input_data'][0], response_scoring.json()['predictions'][0], response_time


def print_wml_tags(wml_client):
    instance_details = wml_client.service_instance.get_details()
    if 'entity' in instance_details.keys() and 'tags' in instance_details['entity'].keys():
        print(instance_details['entity']['tags'])


def wait_for_business_app(url_get_details, headers, busines_app_timeout = 15):
    def get_details(url_get_details, headers):
        response = requests.get(url=url_get_details,
                            headers=headers)
        if(response.status_code == 200):
            print(response.status_code)
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


def wait_for_records_in_data_set(url_get_data_set_records, headers, data_set_records, waiting_timeout = 75):

    def get_data_set_records(url_get_data_set_records, headers):
        if 'include_total_count' not in url_get_data_set_records:
            additional_sign = '?' if '?' not in url_get_data_set_records else '&'
            url = url_get_data_set_records+additional_sign+'include_total_count=true'
        else:
            url = url_get_data_set_records
        response = requests.get(url=url, headers=headers)
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


def wait_for_monitor_instance(run_url, headers, run_id,  waiting_timeout=430):
    run_url = run_url + "/" + run_id

    def get_run_details(url, headers):
        response = requests.get(
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
