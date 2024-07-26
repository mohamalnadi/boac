"""
Copyright ©2024. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""

import calendar
from datetime import datetime as dt
import json
import os
import shutil

from bea.models.term import Term
from dateutil import tz
from flask import current_app as app


# Driver config

def get_browser():
    return app.config['BROWSER']


def get_browser_chrome_binary_path():
    return app.config['BROWSER_BINARY_PATH']


def browser_is_headless():
    return app.config['BROWSER_HEADLESS']


# Timeouts

def get_click_sleep():
    return app.config['CLICK_SLEEP']


def get_short_timeout():
    return app.config['TIMEOUT_SHORT']


def get_medium_timeout():
    return app.config['TIMEOUT_MEDIUM']


def get_long_timeout():
    return app.config['TIMEOUT_LONG']


# Users

def get_admin_uid():
    return app.config['ADMIN_UID']


def get_admin_username():
    return os.getenv('USERNAME')


def get_admin_password():
    return os.getenv('PASSWORD')


# Test configs and utils

def get_test_identifier():
    return f'QA TEST {calendar.timegm(dt.now().timetuple())}'


def parse_test_data():
    with open(app.config['TEST_DATA']) as f:
        return json.load(f)


def attachments_dir():
    return f'{app.config["BASE_DIR"]}/bea/assets'


def default_download_dir():
    return f'{app.config["BASE_DIR"]}/bea/downloads'


def prepare_download_dir():
    # Make sure a clean download directory exists
    if os.path.isdir(default_download_dir()):
        shutil.rmtree(default_download_dir())
    os.mkdir(default_download_dir())


def is_download_dir_empty():
    return False if os.listdir(default_download_dir()) else True


def assert_equivalence(actual, expected):
    app.logger.info(f'Expecting {expected}, got {actual}')
    assert actual == expected


def date_to_local_tz(date):
    return date.astimezone(tz.gettz('Los Angeles'))


def in_op(arr):
    arr = list(map(lambda i: f"'{i}'", arr))
    return ', '.join(arr)


# Terms

def get_current_term():
    return Term({
        'code': app.config['TERM_CODE'],
        'name': app.config['TERM_NAME'],
        'sis_id': app.config['TERM_SIS_ID'],
    })


def get_previous_term(term=None):
    term = term or get_current_term()
    sis_id = get_prev_term_sis_id(term.sis_id)
    return Term({
        'code': get_previous_term_code(sis_id),
        'name': term_sis_id_to_term_name(sis_id),
        'sis_id': sis_id,
    })


def get_prev_term_sis_id(sis_id=None):
    current_sis_id = int(sis_id) if sis_id else int(app.config['TERM_SIS_ID'])
    previous_sis_id = current_sis_id - (4 if (current_sis_id % 10 == 2) else 3)
    return f'{previous_sis_id}'


def get_previous_term_code(term_sis_id):
    d1 = '2'
    d2_3 = str(int(term_sis_id[1:3]) - 1) if (term_sis_id[-1] == '2') else term_sis_id[1:3]
    if term_sis_id[3] == '8':
        d4 = '5'
    elif term_sis_id[3] == '5':
        d4 = '2'
    else:
        d4 = '8'
    return d1 + d2_3 + d4


def term_sis_id_to_term_name(term_sis_id):
    year = f'{term_sis_id[0]}0{term_sis_id[1]}{term_sis_id[2]}'
    if term_sis_id[3] == 2:
        return f'Spring {year}'
    elif term_sis_id[3] == 5:
        return f'Summer {year}'
    else:
        return f'Fall {year}'
