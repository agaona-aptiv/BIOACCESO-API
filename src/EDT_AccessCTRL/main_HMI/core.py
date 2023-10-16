'''
Created on October, 2020
@author: Ernesto Ulises Beltran
'''
#########################################################################################
#  COPYRIGHT 2020
#  \verbatim
#                 This software is copyright protected and proprietary to Condumex.
#                 All other rights remain with Condumex
#
#  \endverbatim
#  LICENSE
#          Module: HMI
#          Description: This script provides control of HMI.
#          Enterprise: Condumex
#          SW Developer: Ernesto Ulises Beltran
#
#          File: core.py
#          Feature: HMI
#          Design: TBD
#          Deviations: None (At the time this code was writen there was no python standard
#          defined yet.)
#
#########################################################################################

import logging
import os
import subprocess
import sys
import yaml

class Core:
    version = '1.0'

    def __init__(self):
        sys.path.append(self.path())
        self.debug = False
        self.boot()

    def boot(self):
        self.config = self.load_config()
        self.logger = self.setup_logging()

    def set_debug(self, debug):
        self.debug = debug
        self.boot()

    def load_config(self):
        default = {
            'log_level': 'INFO',
            'log_formatter': '%(asctime)s - %(levelname)s - %(message)s',
            'target': False,
            'splash': False,
            'width': 600,
            'height': 1024,
        }
        config_fname = self.path('.', 'config.yml')
        if not os.path.exists(config_fname):
            with open('config.yml', 'w') as f:
                f.write(yaml.safe_dump(default, default_flow_style=False))
        with open(config_fname) as f:
            config = yaml.safe_load(f.read()) or {}
        default.update(config)
        if self.debug:
            default['log_level'] = 'DEBUG'
        default['serial_file'] = None
        return default

    def setup_logging(self):
        logger = logging.getLogger()
        log_level = (
            logging.DEBUG
            if self.config['log_level'].lower() == 'debug'
            else logging.INFO
        )
        logger.setLevel(log_level)
        formatter = logging.Formatter(self.config['log_formatter'])
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def path(self, *args):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))

    def popen(self, cmd, verbose=False):
        logging.debug('Execute shell command %s' % ' '.join(cmd))
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

#########################################################################################
#  File Revision History (top to bottom: first revision to last revision)
#
# Date userid (Description on following lines: task_name #, etc.)
# Oct-08-2020 Ernesto Ulises Beltran
#   + DBL_66:
#      -Created initial file.
#
# Oct-15-2020 Ernesto Ulises Beltran
#   + DBL_93:
#      -Updated data flow for hmi.
#
#########################################################################################