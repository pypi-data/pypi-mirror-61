# Copyright 2018 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configure logging for the Joulescope user interfaace application"""


import logging
from logging import FileHandler
import time
import datetime
import faulthandler
import json
import os
import sys
import platform
from joulescope_ui.paths import paths_current
from . import __version__ as UI_VERSION
from joulescope import VERSION as DRIVER_VERSION


paths = paths_current()
LOG_PATH = paths['dirs']['log']
EXPIRATION_SECONDS = 7 * 24 * 60 * 60
STREAM_SIMPLE_FMT = "%(levelname)s:%(name)s:%(message)s"
STREAM_VERBOSE_FMT = "%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d:%(name)s:%(message)s"
FILE_FMT = "%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d:%(name)s:%(message)s"

LEVELS = {
    'OFF': 100,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'ALL': 0,
}
for name, value in list(LEVELS.items()):
    LEVELS[value] = value
assert(logging.CRITICAL == 50)
assert(logging.DEBUG == 10)


_BANNER = """\
Joulescope User Interface
UI Version = {ui_version}
Driver Version = {driver_version}"""


def _make_banner():
    banner = _BANNER.format(ui_version=UI_VERSION, driver_version=DRIVER_VERSION)
    lines = banner.split('\n')
    line_length = max([len(x) for x in lines]) + 4
    lines = ['* ' + line + (' ' * (line_length - len(line) - 3)) + '*' for line in lines]
    k = '*' * line_length
    lines = [k] + lines + [k, '']
    return '\n'.join(lines)


def _make_info():
    frozen = getattr(sys, 'frozen', False)
    if frozen:
        frozen = getattr(sys, '_MEIPASS', frozen)
    info = {
        'joulescope': {
            'ui_version': UI_VERSION,
            'driver_version': DRIVER_VERSION,
        },
        'platform': {
            'name': sys.platform,
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor(),
            'executable': sys.executable,
            'frozen': frozen,
            'paths': paths,
        }
    }
    return json.dumps(info, indent=2)


def _cleanup_logfiles():
    """Delete old log files"""
    now = time.time()
    for f in os.listdir(LOG_PATH):
        fname = os.path.join(LOG_PATH, f)
        if not os.path.isfile(fname):
            continue
        if os.stat(fname).st_mtime + EXPIRATION_SECONDS < now:
            try:
                os.unlink(fname)
            except Exception:
                logging.getLogger(__name__).warning('Could not unlink %s', fname)


def logging_config(stream_log_level=None, file_log_level=None):
    """Configure logging.

    :param stream_log_level: The logging level for stderr which
        can be the integer value or name.  None (default) is 'WARNING'.
    :param file_log_level: The logging level for the log file which
        can be the integer value or name.  None (default) is 'INFO'.
    """
    banner = _make_banner()
    banner = banner + '\ninfo = ' + _make_info() + '\n\n=====\n'
    os.makedirs(LOG_PATH, exist_ok=True)
    d = datetime.datetime.utcnow()
    time_str = d.strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(LOG_PATH, 'joulescope_%s_%s.log' % (time_str, os.getpid(), ))

    root_log = logging.getLogger()
    root_log.handlers = []

    stream_lvl = logging.WARNING if stream_log_level is None else LEVELS[stream_log_level]
    stream_fmt = logging.Formatter(STREAM_VERBOSE_FMT)
    stream_hnd = logging.StreamHandler()
    stream_hnd.stream.write(banner)
    stream_hnd.setFormatter(stream_fmt)
    stream_hnd.setLevel(stream_lvl)
    root_log.addHandler(stream_hnd)

    file_lvl = logging.INFO if file_log_level is None else LEVELS[file_log_level]
    if file_lvl < LEVELS['OFF']:
        file_fmt = logging.Formatter(FILE_FMT)
        file_hnd = FileHandler(filename=filename)
        file_hnd.stream.write(banner)
        file_hnd.setFormatter(file_fmt)
        file_hnd.setLevel(file_lvl)
        faulthandler.enable(file=file_hnd.stream)
        root_log.addHandler(file_hnd)
    else:
        faulthandler.enable()

    root_log.setLevel(min([stream_lvl, file_lvl]))
    _cleanup_logfiles()
    root_log.info('logging configuration: stream_level=%s, file_level=%s', stream_lvl, file_lvl)
