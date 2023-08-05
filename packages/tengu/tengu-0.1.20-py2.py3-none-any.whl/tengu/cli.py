import argparse
from .views import app

def main(port, init_db=False):

    if init_db:
        from .models import db
        db.create_all()

    app.run(port=port, host='0.0.0.0')


def main_entrypoint():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store', help='Port',
                        default=5000, type=int, dest='port')
    parser.add_argument('--init-db', action='store_true', help='create db',
                        dest='init_db')
    args = parser.parse_args()

    main(port=args.port, init_db=args.init_db)
