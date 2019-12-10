import argparse
from estocks.utils import colored
from estocks import __version__


def print_args(args):
    param_str = '\n'.join(
            [ '{:>20s} = {}'.format(colored.CSTR_YELLOW(k), v) for k, v in sorted(vars(args).items())]
    )
    print(param_str)

def resolve_yaml_path(path, to_stream=False):
    import os
    import io
    if hasattr(path, 'read'):
        return path
    elif os.path.exists(path):
        if to_stream:
            return open(path, encoding='utf8')
        else:
            return path
    elif path.isidentifier():
        return io.StringIO('!%s {}' % path)
    elif path.startswith('!'):
        return io.StringIO(path)
    else:
        raise argparse.ArgumentTypeError('''{} can not be resolved, it should be a readable stream,
                                            or a valid file path, or a supported class name.'''.format(path))

def set_service_parser(parser):
    parser.add_argument('--debug',
                        action='store_true',
                        default=False,
                        help='specify in debug mode')
    parser.add_argument('--port',
                        type=int,
                        default=8111,
                        help='specify port of service')
    parser.add_argument('--host',
                        type=str,
                        default='0.0.0.0',
                        help='specify addr of service')
    parser.add_argument('--yaml_path',
                        type=resolve_yaml_path,
                        required=True,
                        help='yaml config of the service, it should be a readable stream,'
                        ' or a valid file path, or a supported class name.')

    return parser


def get_parser():
    parser = argparse.ArgumentParser(
            description='''{}, My Own Stock Search Engine'''.format(colored.CSTR_GREEN('estocks {}'.format(__version__)))
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s' + ': %s' % (__version__))
    parser.add_argument('--verbose', action='store_true', default=False, help='specify verbose mode')

    sp = parser.add_subparsers(dest='cli', title='estocks sub-commands',
            description='use "estocks [sub-command] --help" '
                        'to get detailed information about each sub-command')

    ssp = set_service_parser(sp.add_parser('server', help='start a estocks service'))
    ctp = set_service_parser(sp.add_parser('create_table', help='create all tables'))
    dtp = set_service_parser(sp.add_parser('drop_table', help='drop all tables'))
    return parser
