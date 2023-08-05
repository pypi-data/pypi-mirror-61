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
from ibm_ai_openscale import APIClient, APIClient4ICP


class TestAIOpenScaleClient(unittest.TestCase):
    ai_client = None
    credentials = None

    @classmethod
    def setUpClass(cls):
        cls.aios_credentials = get_aios_credentials()
        cls.schema = get_schema_name()
        cls.database_credentials = get_database_credentials()

        if is_icp():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

    def test_00_check_if_datamart_exists(self):
        if is_icp():
            try:
                print("Checking if datamart exists on CP4D...")
                self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
                print("Datamart exists: {}".format(self.ai_client.data_mart.get_details()))
            except Exception as ex:
                print("Unable to setup datamart: {}".format(ex))
                print("Cleaning environment...")
                prepare_env(self.ai_client)
                print("Environment cleaned. Creating datamart...")
                self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
                print("Datamart created.")
        else:
            print("Cleaning up all env...")
            prepare_env(self.ai_client)
            print("Environment cleaned. Creating datamart...")
            self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)
            print("Datamart created.")


if __name__ == '__main__':
    unittest.main()
