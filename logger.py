# -*- coding:utf8 -*-
"""
supper log function
"""
import os


def filer(filename='', filedir='./'):
    """
    filer(filename='', filedir='./')
    return fullpath
    auto create filedir
    if filename is null, only filedir be created
    """
    filedir = os.path.abspath(filedir)
    os.makedirs(filedir) if not os.path.isdir(filedir) else None
    return (os.path.join(filedir, filename) if filename else filedir)


def logger(name, logname, logdir='./'):
    """
    logger(name, logname, logdir='./')
    high level logging

    how to use:
    alog = logger('default', 'log13.txt')
    alog.debug('debug message!')
    alog.info('info message!')
    alog.error('error message')
    alog.critical('critical message')
    alog.warning('warning message')
    """
    import logging
    import logging.config
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {'format': '%(asctime)s %(levelname)s %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S',
                        },
            'verbose': {'format': '%(asctime)s %(levelname)s %(module)s \
                %(process)d %(thread)d %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S',
                        },
            'simple': {'format': '%(levelname)s %(message)s',
                       'datefmt': '%Y-%m-%d %H:%M:%S'
                       },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': filer(logname, logdir),
                'maxBytes': 1024000,
                'backupCount': 3,
                'encoding': 'utf8',
            },
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
            },
            'file': {
                'level': 'INFO',
                'handlers': ['file'],
            }
        },
        # 'disable_existing_loggers': False,
    })
    return logging.getLogger(name)
