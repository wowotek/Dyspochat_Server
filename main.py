#/bin/python3

import os
from server import app

if __name__ == '__main__':
    os.system("sleep 0.5")
    print("--- Starting Server ---")
    app.run(host="0.0.0.0", port=5555)
