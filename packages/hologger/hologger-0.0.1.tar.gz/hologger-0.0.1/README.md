Before use this app you have to do few configuration.
In your setting.py add follow handlers and loggers.
If you want log your query, add 'dblogger_sql' to handlers and loggers. 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class' : 'logging.StreamHandler'
        },
        'dblogger': {
            'level': 'DEBUG',
            'class': 'dblogger.handlers.DbLogHandler',
        },
        'dblogger_sql':{
            'level' : 'DEBUG',
            'class' : 'dblogger.handlers.DbLogSqlHandler'
        }
    },
    'loggers': {
        'dblogger': {
            'handlers': ['dblogger'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends':{
            'handlers': ['console', 'dblogger_sql'],
            'level': 'DEBUG'
        }
    },
}