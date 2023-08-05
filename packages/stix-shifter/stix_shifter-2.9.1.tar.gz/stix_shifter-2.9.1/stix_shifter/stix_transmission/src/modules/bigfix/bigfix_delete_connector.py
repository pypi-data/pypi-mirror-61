from ..base.base_delete_connector import BaseDeleteConnector
from .....utils.error_response import ErrorResponder


class BigFixDeleteConnector(BaseDeleteConnector):

    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        return_obj = dict()
        return_obj['success'] = True
        return return_obj
