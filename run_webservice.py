#/bin/python3

import time
from webservice import app

if __name__ == '__main__':
    time.sleep(0.5)
    print("--- Starting Server ---")
    app.run(host="0.0.0.0", port=5000, debug=True)
