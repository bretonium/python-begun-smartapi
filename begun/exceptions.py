import requests

class BaseBegunError(Exception):
    pass

class RequestException(BaseBegunError):
    '''Is raised when requests.exceptions.RequestException happens'''
    def __init__(self, request_exception):
        self.request_exception = request_exception
        super(RequestException, self).__init__(request_exception)

class CallError(BaseBegunError):
    '''Is raised when ``error`` key is returned by Begun'''
    def __init__(self, error):
        self.error = error
        m = u'{0}: {1}'.format(error['error_code'], error['error_message'])
        super(RequestException, self).__init__(m)

class BadResponse(BaseBegunError):
    '''sometimes Begun returns not json'''
    pass
