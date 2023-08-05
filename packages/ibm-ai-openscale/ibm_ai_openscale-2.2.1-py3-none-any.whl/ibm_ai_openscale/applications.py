# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from ibm_ai_openscale.base_classes import Table
from ibm_ai_openscale.supporting_classes import *
from ibm_ai_openscale.utils.client_errors import *
from ibm_ai_openscale.supporting_classes.enums import EventDataFormat
from io import BufferedReader
from requests.utils import quote




@logging_class

class Applications:
    """
    Manages applications used to analyze subscribed deployments.
    """
    def __init__(self, ai_client):
        from ibm_ai_openscale.base_classes.client.client import APIClientBase
        validate_type(ai_client, "ai_client", APIClientBase, True)
        self._ai_client = ai_client
        self._hrefs_v2 = AIHrefDefinitionsV2(ai_client._service_credentials)

        # self._list_header =  ['uid', 'name', 'description','subscription ids' 'metrics']
        self._applications_table_fields = ['uid', 'name', 'description','subscription ids' 'metrics']

    def _validate_application_id(self, application_id):
        validate_type(application_id, u'application_id', str, True)
        if application_id not in self.get_uids():
            raise ValueError("Invalid application id")

    def _get_records(self):

        records = [
            [
                application['metadata']['id'],
                application['entity']['name'],
                application['entity']['description'] if 'description' in application else None,
                application['entity']['subscription_ids'],
                [metric['id'] for metric in application['entity']['business_metrics']],

            ] for application in self.get_details()['business_applications']
        ]

        return records

    def _get_run_details(self, business_metrics_monitor_instance_id, run_id):

        validate_type(run_id, 'run_id', str, False)

        url = self._hrefs_v2.get_monitor_instance_run_details_href(business_metrics_monitor_instance_id, run_id)
        response = self._ai_client.requests_session.get(
            url=url,
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, u'getting business monitor run details', response)

    def get_details(self, application_id=None):
        """
        Gets details of registered application(s).

        :param application_id: uid of defined application (optional)
        :type application_id: str

        :return: registered applications details
        :rtype: dict

        A way you might use me is:

        >>> client.data_mart.applications.get_details(application_id)
        >>> client.data_mart.applications.get_details()
        """

        validate_type(application_id, 'application_id', str, False)

        if application_id is None:
            url = self._hrefs_v2.get_applications_href()
        else:
            url = self._hrefs_v2.get_application_details_href(application_id)

        headers = self._ai_client._get_headers()
        headers["Cache-Control"] = "no-cache"

        response = self._ai_client.requests_session.get(
                url=url,
                headers=headers
            )

        return handle_response(200, u'getting application details', response)

    def get_uids(self, name=None):
        """
        Gets uids of defined applications.

        :param name: name of the application (optional). If not provided uids for all defined applications are returned
        :type name: list of str

        :return: list of defined applications' uids.
        :rtype: list

        A way you might use me is:

        >>> client.data_mart.applications.get_uids()
        """

        validate_type(name, 'name', str, False)
        applications_details = self.get_details()

        if name is None:
            uids = [application['metadata']['id'] for application in applications_details['business_applications']]
        else:
            uids = [application['metadata']['id'] for application in applications_details['business_applications']
                    if application['entity']['name'] == name]

        return uids

    def get_table_content(self, application_id, format='pandas', limit=10):
        """
        Gets content of table in chosen format.
        By default the format is 'pandas'.

        :param application_id: uid of defined application
        :type application_id: str

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows, by default is set to 10 (optional)
        :type limit: int

        :return: content of table with bkpis
        :rtype: pandas DataFrame or list

        A way you might use me is:

        >>> pandas_table_content = client.data_mart.applications.get_table_content(application_id)
        >>> table_content = client.data_mart.applications.get_table_content(application_id, format='python')
        >>> pandas_table_content = client.data_mart.applications.get_table_content(application_id, format='pandas')
        """
        validate_type(format, u'format', str, True)
        validate_type(limit, u'limit', int, False)
        self._validate_application_id(application_id)

        bkpi_data = []
        measurements = self.get_measurements(application_id, limit=limit)['measurements']

        for m in measurements:
            for val in m['entity']['values']:
                for metric in val['metrics']:
                    data_rec = metric
                    data_rec['timestamp'] = m['entity']['timestamp']
                    data_rec['measuremet_id'] = m['metadata']['id']
                    for tag in val['tags']:
                        data_rec[tag['id']] = tag['value']
                    bkpi_data.append(data_rec)

        if format == 'python':
            return bkpi_data
        elif format == 'pandas':
            import pandas as pd
            columns = ['timestamp', 'id', 'value', 'lower_limit', 'measuremet_id', 'transaction_batch_id']
            return pd.DataFrame(data=bkpi_data, columns=columns)
        else:
            raise ClientError('Unsupported format chosen: {}'.format(format))

    def list(self, **kwargs):
        """
        Lists defined business applications.

        :param kwargs: filtering parameters corresponding to column names (optional)
        :type kwargs: dict

        A way you might use me is:

        >>> client.data_mart.applications.list()
        """
        Table(self._applications_table_fields, self._get_records()).list(filter_setup=kwargs, title="Applications",
                                                                        column_list=self._applications_table_fields)

    def add(self, name, business_metrics, payload_schema, subscription_ids=None, description=None):
        """
         Adds application instance.

         :param name: name of the monitor
         :type name: str

         :param business_metrics: list of BusinessMetric class objects defining business metrics for the application
         :type business_metrics: list

         :param payload_schema: list of business payload fields which are part of business application. Every field should be described by dictionary with three values: "name", "type" (allowed values: 'string' or 'number') and optionally "description".
         :type payload_schema: list

         :param subscription_ids: list of subscription ids which application is targeted to  (optional)
         :type subscription_ids: list

         :param description: description of the monitor (optional)
         :type description: str

         :return: registered application details
         :rtype: dict

         A way you might use me is:

         >>> from ibm_ai_openscale.supporting_classes import BusinessMetric
         >>> from ibm_ai_openscale.supporting_classes.enums import AggregationMethods as AppAggregation

         >>> business_metrics = [BusinessMetric(metric_name='Sum of Values',field_name='Values',aggregation=AppAggregation.SUM, lower_limit=10),
         >>>                     BusinessMetric(metric_name='Average of Values', field_name='Values',aggregation=AppAggregation.AVG, lower_limit=5)]
         >>> business_payload_fields = [{"name": "Values", "type": "number", "description": "Column with values"}]
         >>> application_details = client.data_mart.application.add(name='Model Application', business_metrics=business_metrics, payload_schema=business_payload_fields)
        """
        validate_type(name, 'name', str, True)
        validate_type(business_metrics, 'business_metrics', list, True)
        validate_type(payload_schema, 'payload_schema', list, True)
        validate_type(subscription_ids, 'subscription_ids', list, False)
        validate_type(description, 'description', str, False)
        # validate_type(business_metrics_monitor_definition_id, 'business_metrics_monitor_definition_id', str, False)
        # validate_type(business_metrics_monitor_instance_id, 'business_metrics_monitor_instance_id', str, False)
        # validate_type(correlation_monitor_instance_id, 'correlation_monitor_instance_id', str, False)
        # validate_type(business_payload_data_set_id, 'business_payload_data_set_id', str, False)
        # validate_type(transaction_batches_data_set_id, 'transaction_batches_data_set_id', str, False)


        payload = {
                    "name": name,
                    "description": description if not None else '',
                    "payload_fields": payload_schema,
                    "business_metrics": [m._to_json() for m in business_metrics],
        }

        if subscription_ids is not None:
            payload["subscription_ids"] = subscription_ids

        # if business_metrics_monitor_definition_id is not None:
        #     payload["business_metrics_monitor_definition_id"] = business_metrics_monitor_definition_id
        #
        # if business_metrics_monitor_instance_id is not None:
        #     payload["business_metrics_monitor_instance_id"] = business_metrics_monitor_instance_id
        #
        # if correlation_monitor_instance_id is not None:
        #     payload["correlation_monitor_instance_id"] = correlation_monitor_instance_id
        #
        # if business_payload_data_set_id is not None:
        #     payload["business_payload_data_set_id"] = business_payload_data_set_id
        #
        # if transaction_batches_data_set_id is not None:
        #     payload["transaction_batches_data_set_id"] = transaction_batches_data_set_id

        response = self._ai_client.requests_session.post(
            url=self._hrefs_v2.get_applications_href(),
            json=payload,
            headers=self._ai_client._get_headers()
        )

        try:
            application_details = handle_response(202, 'post application', response, True)
            return application_details
        except ApiRequestWarning:
            ApiRequestWarning.print_msg(u'Warning during {}.'.format('application registration'), response)
            application_details = self.get_details(applicatin_id=self.get_uids(name=name)[0])
            return application_details

    def run(self, application_id, background_mode=True, max_nb_days_for_correlation_monitor=100):
        """
        Runs application instance.

        :param application_id: uid of defined application
        :type application_id: str

        :param background_mode: if set to True, run will be in asynchronous mode, if set to False it will wait for result (optional)
        :type background_mode: bool

        :param max_nb_days_for_correlation_monitor: max number of days calculated for correlation monitor(optional)
        :type max_nb_days_for_correlation_monitor: int

        :return: application run details
        :rtype: dict

        A way you might use me is:

        >>> client.data_mart.applications.run(application_id)
        """

        self._validate_application_id(application_id)
        validate_type(background_mode, 'background_mode', bool, False)
        validate_type(max_nb_days_for_correlation_monitor, 'max_nb_days_for_correlation_monitor', int, False)

        business_metrics_monitor_instance_id = self.get_details(application_id)['entity']['business_metrics_monitor_instance_id']

        payload = {
            "triggered_by": "user",
            "parameters": {
                "correlation_monitor": {
                    "trigger_on_completion": True,
                    "parameters": {
                        "max_number_of_days": max_nb_days_for_correlation_monitor}}}}

        response = self._ai_client.requests_session.post(
            url=self._hrefs_v2.get_monitor_instance_run_href(business_metrics_monitor_instance_id),
            headers=self._ai_client._get_headers(),
            json=payload)

        business_app_run_details = handle_response(201, 'run application monitor', response)

        if background_mode:
            return business_app_run_details

        request_id = business_app_run_details['metadata']['id']

        def check_state():
            details = self._get_run_details(business_metrics_monitor_instance_id, request_id)
            return details['entity']['status']['state']

        def get_result():
            details = self._get_run_details(business_metrics_monitor_instance_id, request_id)
            state = details['entity']['status']['state']

            if state in ['finished']:
                return "Successfully finished run", None, details
            else:
                return "Run failed with status: {}".format(state), 'Reason: {}'.format(details['entity']['status']['failure']), details

        return print_synchronous_run(
            'Waiting for end of business metrics calculation run {}'.format(request_id),
            check_state,
            get_result=get_result
        )

    def store_event_data(self, application_id, event_data, event_data_format, data_header=False, data_delimiter=',',
                         _csv_max_line_length=10 * 1024 * 1024):

        """
        Stores business payload records in business application data set.

        :param application_id: uid of defined application
        :type application_id: str

        :param event_data: business payload data. Each record should have fields  "transaction_id" and "timestamp".
        :type event_data: list of dict, str or io BufferedReader

        :param event_data_format: content type (optional). One of [‘text’, ‘dict’]. Default value: ‘dict’.
        :type event_data_format: str

        :param data_header: does the csv/text data contain header [True, False]? (optional). Default value is False.
        :type data_header: bool

        :param data_delimiter: delimiter character used to separate fields in CSV/TEXT format (optional). By default comma is used.
        :type data_delimiter: str


        A way you might use me is:

        >>> from ibm_ai_openscale.supporting_classes.enums import EventDataFormat
        >>>
        >>> client.data_mart.applications.store_event_data(application_id = application_id,event_data=io_buffer_reader, event_data_format=EventDataFormat.CSV)
        >>> client.data_mart.applications.store_event_data(application_id = application_id,event_data = "car_new,1,250,0-0-2,2019-12-31T01:00:00.00000", event_data_format=EventDataFormat.CSV)
        >>> client.data_mart.applications.store_event_data(application_id = application_id,event_data = [{"field_1": 16, "field_2": "2000", "transaction_id": "0-0-2", "timestamp": "2019-12-31T01:00:00.00000"}], event_data_format=EventDataFormat.DICT)

       """
        validate_type(application_id, "application_id", str, True)
        self._validate_application_id(application_id)

        if event_data_format == EventDataFormat.CSV:
            validate_type(event_data, "feedback_data", [str, BufferedReader], True)
            validate_type(data_header, "data_header", bool, True)
            validate_type(data_delimiter, "data_delimiter", str, True)
            validate_type(_csv_max_line_length, "_csv_max_line_length", int, True)
        else:
            validate_type(event_data, "feedback_data", [list], True)

        business_payload_data_set_id = self.get_details(application_id)['entity']['business_payload_data_set_id']

        if event_data_format == EventDataFormat.DICT:

            response = self._ai_client.requests_session.post(
                self._hrefs_v2.get_data_set_records_href(business_payload_data_set_id),
                json=event_data,
                headers=self._ai_client._get_headers()
            )

            handle_response(202, u'business event data storing', response, json_response=True)

        elif event_data_format == EventDataFormat.CSV:

            query_params = '?header=' + json.dumps(data_header) + '&delimiter=' + quote(data_delimiter, safe='') + '&on_error=continue' + "&csv_max_line_length=" + str(_csv_max_line_length)
            response = self._ai_client.requests_session.post(
                self._hrefs_v2.get_data_set_records_href(business_payload_data_set_id) + query_params,
                data=event_data,
                headers=self._ai_client._get_headers(content_type='text/csv')
            )

            handle_response(202, u'business event data storing', response, json_response=True)

        else:
            raise IncorrectValue(value_name='data_format', reason='Unsupported value.')

    def get_business_payload_records_count(self, application_id):
        """
        Returns number of records stored in business payload data set.

        :param application_id: uid of defined application
        :type application_id: str

        :return: number of records stored in data set
        :rtype: int
        """
        self._validate_application_id(application_id)
        business_data_set_id = self.get_details(application_id)['entity']['business_payload_data_set_id']

        response = self._ai_client.requests_session.get(
            url=self._hrefs_v2.get_data_set_records_href(business_data_set_id) + '?include_total_count=true',
            headers=self._ai_client._get_headers(), json={})

        handle_response(200, u'get business data set records', response, json_response=True)
        return response.json()['total_count']

    def get_measurements(self, application_id, start_time=None, limit=100):
        """
        Returns measurements of business monitor instance

        :param application_id: uid of defined application
        :type application_id: str

        :param start_time: returns measurements from start time to current time. By default last 3 months are used. Example value of start_time: "2019-05-22T00:00:00Z" (optional)
        :type start_time: str

        :param limit: limit of measurements (optional), default value is 100
        :type limit: int

        :return: measurements of business monitor instance
        :rtype: dict

        A way you might use me is:

        >>> measurements = client.data_mart.applications.get_measurements(application_id, start_time ="2019-12-22T00:00:00Z", limit=20)

        """

        validate_type(application_id, 'application_id', str, True)
        validate_type(start_time, 'start_time', str, False)
        validate_type(limit, 'limit', int, False)

        self._validate_application_id(application_id)

        application_details = self.get_details(application_id)
        weeks_number=12

        if start_time is None:
            try:
                start_time = datetime.datetime.strptime(application_details['metadata']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")\
                             - timedelta(weeks=weeks_number)
            except:
                start_time = datetime.datetime.strptime(application_details['metadata']['created_at'], "%Y-%m-%dT%H:%M:%SZ")\
                                 - timedelta(weeks=weeks_number)
            start_time = start_time.isoformat() + 'Z'

        monitor_instance_id = application_details['entity']['business_metrics_monitor_instance_id']

        query = '?start={}&end={}Z&limit'.format(start_time, datetime.datetime.utcnow().isoformat(), limit)

        response = self._ai_client.requests_session.get(
            self._hrefs_v2.get_measurements_href(monitor_instance_id)+query,
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, "getting application measurements", response, True)

    def get_correlation_measurements(self, application_id, start_time=None, limit=100):
        """
        Returns measurements of correlation monitor

        :param application_id: uid of defined application
        :type application_id: str

        :param start_time: returns measurements from start time to current time. By default last 3 months are used. Example value of start_time: "2019-05-22T00:00:00Z" (optional)
        :type start_time: str

        :param limit: limit of measurements (optional), default value is 100
        :type limit: int

        :return: measurements of business monitor instance
        :rtype: dict

        A way you might use me is:

        >>> measurements = client.data_mart.applications.get_correlation_measurements(application_id, start_time ="2019-12-22T00:00:00Z", limit=20)

        """

        validate_type(application_id, 'application_id', str, True)
        validate_type(start_time, 'start_time', str, False)
        validate_type(limit, 'limit', int, False)

        self._validate_application_id(application_id)

        application_details = self.get_details(application_id)
        weeks_number = 12

        if start_time is None:
            try:
                start_time = datetime.datetime.strptime(application_details['metadata']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")\
                             - timedelta(weeks=weeks_number)
            except:
                start_time = datetime.datetime.strptime(application_details['metadata']['created_at'], "%Y-%m-%dT%H:%M:%SZ")\
                                 - timedelta(weeks=weeks_number)
            start_time = start_time.isoformat() + 'Z'

        try:
            monitor_instance_id = application_details['entity']['correlation_monitor_instance_id']
        except KeyError:
            print("No correlation monitor connected to the application.")
            return None

        query = '?start={}&end={}Z&limit'.format(start_time, datetime.datetime.utcnow().isoformat(), limit)

        response = self._ai_client.requests_session.get(
            self._hrefs_v2.get_measurements_href(monitor_instance_id)+query,
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, "getting correlation measurements", response, True)

    def delete(self, application_id):
        """
        Deletes application instance.

        :param application_id: application id
        :type application_id: str

        A way you might use me is:

        >>> client.data_mart.applications.delete(application_id)
        """

        validate_type(application_id, 'application_id', str, True)

        response = self._ai_client.requests_session.delete(
            self._hrefs_v2.get_application_details_href(application_id),
            headers=self._ai_client._get_headers()
        )

        handle_response(202, 'deletion of application', response, False)
