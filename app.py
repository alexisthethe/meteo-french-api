"""entrypoint to initiate and run Flask app"""

import os
from meteofrenchapi import create_app

PORT = os.getenv("PORT")
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
