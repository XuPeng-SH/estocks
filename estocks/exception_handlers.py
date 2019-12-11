from elasticsearch.exceptions import NotFoundError as ESNotFoundError
from flask_restplus.model import HTTPStatus
from estocks.namespaces import default_api as api
from estocks.exceptions import *
from restplus_enhancement.schema_model import SchemaResponse
from estocks import exception_codes as codes


@api.errorhandler(ESNotFoundError)
def ESNotFoundErrorHandler(error):
    return SchemaResponse(code=codes.ESNotFoundError,
            message=str(error),
            ), HTTPStatus.BAD_REQUEST
