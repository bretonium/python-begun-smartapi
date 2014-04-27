from __future__ import absolute_import

import requests
import json

from .exceptions import RequestException, CallError

class BasicBegun(object):
    url = 'https://smart.begun.ru/api/'
    query_timeout = 10

    def lock(self, name, timeout, sleep):
        '''
        Return a new Lock object using key ``name`` that mimics
        the behavior of threading.Lock.

        If specified, ``timeout`` indicates a maximum life for the lock.
        By default, it will remain locked until release() is called.

        ``sleep`` indicates the amount of time to sleep per loop iteration
        when the lock is in blocking mode and another client is currently
        holding the lock.

        The Lock is required to be a context manager (for ``with`` statement).
        '''
        raise NotImplementedError

    def __init__(self, token, require_success=True):
        self.session_id = ''
        self.token = token
        self.require_success = require_success

    def login(self, login, password, captcha_key=None, captcha_text=None):
        '''Logs user in with login and password, submitting captcha values'''
        params = {'login': login, 'password': password}
        if captcha_key and captcha_text:
            params['captcha_key'] = captcha_key
            params['captcha_text'] = captcha_text
        result = self.call('Login', **params)
        self.session_id = result['session_id']
        return result

    def call(self, method, **params):
        data = {'token': self.token,
                'session_id': self.session_id,
                'method': method,
                'params': params
                }
        send_data = json.dumps(data)
        try:
            with self.lock('begun_call', self.query_timeout):
                response = request.post(self.url, send_data)
        except requests.exceptions.RequestException as e:
            raise RequestException(e)
        try:
            result = response.json()
        except ValueError as e:
            raise BadResponse(e)
        if self.require_success and 'error' in result:
            raise CallError(result['error'])
        return result

