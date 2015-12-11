import cred

connStr = "mysql://" + cred.mysql_username +  ":" + cred.mysql_password + "@" + cred.mysql_server + "/" + cred.mysql_dbname
contractConnStr = "mysql://" + cred.mysql_username +  ":" + cred.mysql_password + "@" + cred.mysql_server + "/" + cred.mysql_contract_dbname

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = frozenset(['some@email.com'])
SECRET_KEY = 'This string will be replaced with a proper key in production.'

SQLALCHEMY_DATABASE_URI = connStr
SQLALCHEMY_BINDS = {
    "waronice": connStr,
    "contracts": contractConnStr
}
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "secretkey"