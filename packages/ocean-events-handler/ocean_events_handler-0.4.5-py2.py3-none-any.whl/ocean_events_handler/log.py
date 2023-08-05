#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging
import logging.config
import os

import yaml


DEFAULT_CONFIG_YAML = '''
version: 1
disable_existing_loggers: {1}
formatters:
  simple:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: {0}
    formatter: simple
    stream: ext://sys.stdout

  info_file_handler:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: simple
    filename: info.log
    maxBytes: 10485760 # 10MB
    backupCount: 20
    encoding: utf8

  error_file_handler:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: simple
    filename: errors.log
    maxBytes: 10485760 # 10MB
    backupCount: 20
    encoding: utf8

loggers:
  ocean_events_handler:
    level: {0}
    handlers: [console]
    propagate: no
  ocean_keeper:
    level: {0}
    handlers: [console]
    propagate: no
  ocean_utils:
    level: {0}
    handlers: [console]
    propagate: no

root:
  level: {0}
  handlers: [console, info_file_handler, error_file_handler]

'''


def setup_logging(default_path='', default_level=None, env_key='LOG_CFG', disable_existing_loggers='True'):
    """Logging Setup"""
    path = default_path
    log_config_path = os.getenv(env_key, None)
    if log_config_path:
        path = log_config_path

    if not default_level:
        level_map = {
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        default_level = level_map.get(os.getenv('LOG_LEVEL', 'INFO'), logging.INFO)

    if os.path.exists(path):
        with open(path, 'rt') as f:
            yaml_config = f.read()
    else:
        _disable_existing_loggers = os.getenv('DISABLE_EXISTING_LOGGERS', disable_existing_loggers)
        log_level_str = os.getenv('LOG_LEVEL', 'INFO')
        yaml_config = DEFAULT_CONFIG_YAML.format(log_level_str, _disable_existing_loggers)

    try:
        config = yaml.safe_load(yaml_config)
        logging.config.dictConfig(config)
    except Exception as e:
        print(e)
        print('Error in Logging Configuration. Using default configs')
        logging.basicConfig(level=default_level)
