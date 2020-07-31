#!/usr/bin/python3
import sys
sys.path.insert(0, '/var/www/Dyspochat_Webservice/')
from Dyspochat_Webservice import app as application
application.secret_key = "wowotek-secret-key"
