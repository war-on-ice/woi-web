USER_NAME = "username"
PASSWORD =  "password"
db_Server = "serveraddress"
db_Name = "dbname"

connStr = "mysql://" + USER_NAME +  ":" + PASSWORD + "@" + db_Server + "/" + db_Name

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = frozenset(['some@email.com'])
SECRET_KEY = 'This string will be replaced with a proper key in production.'

SQLALCHEMY_DATABASE_URI = connStr
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "secretkey"