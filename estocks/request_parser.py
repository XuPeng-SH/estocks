import logging
from flask_restplus import reqparse

logger = logging.getLogger(__name__)


def pagination_parser(parser=None):
    parser = parser if parser else reqparse.RequestParser()
    parser.add_argument('offset', type=int, default=0, required=False, location='args', help='Default: 0')
    parser.add_argument('pagesize', type=int, default=10, required=False, location='args', help='Default: 10')
    return parser

def search_parser(parser=None):
    parser = pagination_parser(parser)
    parser.add_argument('keyword', type=str, required=True, location='args', help='Search keyword')
    return parser
