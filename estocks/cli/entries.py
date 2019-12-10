from estocks.utils import colored

def server(args):
    from estocks import create_app
    app = create_app(args)
    app.run(host=args.host, port=args.port, debug=args.debug)

def create_table(args):
    from estocks import create_app, db
    app = create_app(args)
    with app.app_context():
        db.create_all()

def drop_table(args):
    from estocks import create_app, db
    app = create_app(args)
    with app.app_context():
        db.drop_all()
