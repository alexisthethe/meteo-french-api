import os
from meteofrenchapi import create_app


PORT = os.getenv('PORT')
HOST = os.getenv('HOST')

app = create_app()


if __name__ == '__main__':
    app.run(host= HOST, port=PORT)
