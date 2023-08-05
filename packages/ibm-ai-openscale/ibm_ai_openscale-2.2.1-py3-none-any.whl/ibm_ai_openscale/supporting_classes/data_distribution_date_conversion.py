# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


class DateConversion:
    @staticmethod
    def hour(field):
        return '{}:hour'.format(field)

    @staticmethod
    def day(field):
        return '{}:day'.format(field)

    @staticmethod
    def week(field):
        return '{}:week'.format(field)

    @staticmethod
    def month(field):
        return '{}:month'.format(field)

    @staticmethod
    def year(field):
        return '{}:year'.format(field)