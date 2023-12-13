import requests

from base64 import b64encode
from dataclasses import dataclass
from typing import Dict, Optional

from gong.base import GongHTTPObjectBase
from gong.calls import (
    GongCallBaseFilter,
    GongCallDetailsRequest,
    GongCallTranscriptFilter,
    GongCallTranscriptResponse,
    GongGetCallsResponse,
    GongGetCallDetailsResponse,
)
from gong.users import GongUserResponse


@dataclass
class GongResponse:
    response: requests.Response
    response_obj: GongHTTPObjectBase = None


class GongClient:
    def __init__(self, access_key: str, access_key_secret: str,
                 base_url: str):
        self.base_url = base_url

        self.token = self._generate_token(access_key, access_key_secret)

    @staticmethod
    def snake_to_camel_case(snake_str: str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def camel_case_to_snake(camel_str: str):
        return ''.join(
            '_' + c.lower() if c.isupper() else c for c in camel_str
        ).lstrip('_')

    def _generate_token(self, access_key: str, access_key_secret: str):
        return b64encode(f'{access_key}:{access_key_secret}'.encode('utf-8')).decode('utf-8')

    def _format_request_object(self, request_obj: Dict):
        resulting_obj = {}

        for key, value in request_obj.items():
            new_key_name = self.snake_to_camel_case(key)

            if not value:
                continue

            if isinstance(value, dict):
                resulting_obj[new_key_name] = self._format_request_object(value)

            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    resulting_obj[new_key_name] = [self._format_request_object(item) for item in value]
                else:
                    resulting_obj[new_key_name] = value
            
            else:
                resulting_obj[new_key_name] = value

        return resulting_obj

    def _format_response_object(self, response_obj: Dict):
        resulting_obj = {}

        for key, value in response_obj.items():
            new_key_name = self.camel_case_to_snake(key)

            if isinstance(value, dict):
                resulting_obj[new_key_name] = self._format_response_object(value)

            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    resulting_obj[new_key_name] = [self._format_response_object(item) for item in value]

            else:
                resulting_obj[new_key_name] = value

        return resulting_obj

    def _request(self, method: str, path: str, body: Optional[Dict] = None,
                 params: Optional[Dict] = None, response_obj: GongHTTPObjectBase = None):
        req_args = {
            'method': method,
            'url': f'{self.base_url}/{path}',
            'headers': {
                'Authorization': f'Basic {self.token}'
            }
        }

        if params:
            req_args['params'] = self._format_request_object(params)
        elif body:
            req_args['json'] = self._format_request_object(body)

        response = requests.request(**req_args)

        gong_response = GongResponse(response=response)

        if response.status_code >= 200 and response.status_code < 300:
            if response_obj:
                normalized_response = self._format_response_object(response.json())

                gong_response.response_obj = response_obj(**normalized_response)

        return gong_response

    def post(self, path: str, body: Optional[Dict] = None,
             response_obj: Optional[GongHTTPObjectBase] = None) -> GongResponse:
        return self._request('POST', path, body=body, response_obj=response_obj)

    def get(self, path: str, params: Optional[Dict] = None,
            response_obj: Optional[GongHTTPObjectBase] = None) -> GongResponse:
        return self._request('GET', path, params=params, response_obj=response_obj)

    def calls(self, filter: GongCallBaseFilter) -> GongResponse:
        '''Returns a list of calls matching the filter criteria'''
        params = None
        if filter:
            params = filter.to_dict()

        return self.get(
            path='/v2/calls',
            params=params,
            response_obj=GongGetCallsResponse,
        )

    def call_details(self, request: GongCallDetailsRequest) -> GongResponse:
        '''Returns call details'''
        return self.post(
            body=request.to_dict(),
            path='/v2/calls/extensive',
            response_obj=GongGetCallDetailsResponse,
        )

    def call_transcripts(self, filter: GongCallTranscriptFilter) -> GongResponse:
        '''Returns a list of call transcripts'''
        return self.post(
            body=filter.to_dict(),
            path='/v2/calls/transcript',
            response_obj=GongCallTranscriptResponse,
        )

    def user(self, user_id: str) -> GongResponse:
        '''Returns a user'''
        return self.get(
            path=f'/v2/users/{user_id}',
            response_obj=GongUserResponse,
        )