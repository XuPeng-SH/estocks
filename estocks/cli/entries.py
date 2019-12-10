from estocks.utils import colored

def __init_app(args):
    from estocks import create_app
    app = create_app(args)
    return app

def server(args):
    app = __init_app(args)
    app.run(host=args.host, port=args.port, debug=args.debug)

def create_table(args):
    app = __init_app(args)
    from estocks import db
    with app.app_context():
        db.create_all()

def drop_table(args):
    app = __init_app(args)
    from estocks import db
    with app.app_context():
        db.drop_all()
