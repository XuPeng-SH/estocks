import sys
import os
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)


if __name__ == '__main__':
    from estocks.cli import main
    main()
