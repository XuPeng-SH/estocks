import logging
from functools import wraps
from werkzeug.wrappers import BaseResponse
from flask_restplus.utils import unpack

logger = logging.getLogger(__name__)

def code_message_data_formatter(**kwargs):
    response = None
    result = kwargs.get('result')
    code = kwargs.get('code')
    message = kwargs.get('message')
    evelope = kwargs.get('evelope')

    if not evelope:
      response = {
          'result': result if result else {},
          'code': code if code else 0,
          'message': message if message else '',
      }
    else:
      response = {
          'result': {
              evelope: result
          } if result else {},
          'code': code if code else 0,
          'message': message if message else '',
      }
    return response

def code_message_response_format(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        response = method(*args, **kwargs)
        logger.error(response)
        if isinstance(response, BaseResponse):
            data, code, headers = unpack(response)
        else:
            data, code, headers = response
        logger.error(data)
        data = code_message_data_formatter(**data)

        return data, code, headers

    return wrapper
