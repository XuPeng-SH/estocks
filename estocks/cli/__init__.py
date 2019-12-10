import sys
from estocks.cli import entries

__all__ = ['main']

def no_cli_error(parser):
    def inner():
        parser.print_help()
        sys.exit(1)
    return inner

def main():
    from estocks.cli.parser import get_parser, print_args
    parser = get_parser()
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    print_args(args)
    getattr(entries, args.cli, no_cli_error(parser))(args)
