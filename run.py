import os
from app import create_app

PROD = True if os.environ.get('PROD', False) == 'True' else False

app = create_app()


if __name__ == '__main__':
    app.run(debug=not PROD)
