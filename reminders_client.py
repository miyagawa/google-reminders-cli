import json

import reminders_client_utils as client_utils
from reminder import Reminder

URIs = {
    'create': 'https://reminders-pa.clients6.google.com/v1internalOP/reminders/create',
    'delete': 'https://reminders-pa.clients6.google.com/v1internalOP/reminders/delete',
    'get': 'https://reminders-pa.clients6.google.com/v1internalOP/reminders/get',
}

HEADERS = {
    'content-type': 'application/json+protobuf',
}

HTTP_OK = 200


class RemindersClient:
    def __init__(self):
        self.auth_http = client_utils.authenticate()
    
    @staticmethod
    def _report_error(response, content, func_name: str):
        print(f'Error in {func_name}:')
        print(f'    status code: {response.status}')
        print(f'    content: {content}')
    
    def create_reminder(self, reminder: Reminder) -> bool:
        """
        send a 'create reminder' request.
        returns True upon a successful creation of a reminder
        """
        response, content = self.auth_http.request(
            uri=URIs['create'],
            method='POST',
            body=client_utils.create_req_body(reminder),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            return True
        else:
            self._report_error(response, content, 'create_reminder')
            return False
    
    def get_reminder(self, reminder_id: str) -> Reminder:
        """
        retrieve information about the reminder with the given id. None if an
        error occurred
        """
        response, content = self.auth_http.request(
            uri=URIs['get'],
            method='POST',
            body=client_utils.get_req_body(reminder_id),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            reminder_dict = json.loads(content.decode("utf-8"))['1'][0]
            return client_utils.build_reminder(reminder_dict=reminder_dict)
        else:
            self._report_error(response, content, 'get_reminder')
    
    def delete_reminder(self, reminder_id: str):
        """
        delete the reminder with the given id.
        Returns True upon a successful deletion
        """
        response, content = self.auth_http.request(
            uri=URIs['delete'],
            method='POST',
            body=client_utils.delete_req_body(reminder_id),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            return True
        else:
            self._report_error(response, content, 'delete_reminder')
            return False