#/usr/bin/python3

import time
from Dyspochat_Webservice import app

if __name__ == '__main__':
    time.sleep(0.5)
    print("--- Starting Server ---")
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("/etc/letsencrypt/live/dyspochat.com/cert.pem", "/etc/letsencrypt/live/dyspochat.com/privkey.pem"))
