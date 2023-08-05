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

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

        prepare_env(cls.ai_client)

    def test_00_setup_data_mart(self):
        pass


if __name__ == '__main__':
    unittest.main()
