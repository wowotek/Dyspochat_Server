#/bin/python3

import os
from server import app

if __name__ == '__main__':
    os.system("sleep 0.5")
    print()
    print("--- Starting Server ---")
    print()
    app.run(host="0.0.0.0")