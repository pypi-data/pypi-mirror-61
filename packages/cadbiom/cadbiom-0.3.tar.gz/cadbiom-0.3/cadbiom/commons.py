# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017  IRISA
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA/IRSET
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE

# Standard imports
from logging.handlers import RotatingFileHandler
import logging
import datetime as dt
import tempfile

# Paths
DIR_LOGS = tempfile.gettempdir() + '/'

# Logging
LOGGER_NAME             = "cadbiom"
LOG_LEVEL               = 'INFO'
LOG_LEVELS              = {'debug': logging.DEBUG,
                           'info': logging.INFO,
                           'error': logging.ERROR}

# Miscellaneous
TOOLTIPS_DELAY = 200  # (ms)
# Website
CADBIOM_WEBSITE_URL = "http://cadbiom.genouest.org/"
MAIN_DOC_URL = CADBIOM_WEBSITE_URL + "documentation.html"
GUI_DOC_URL = CADBIOM_WEBSITE_URL + "doc/cadbiom/gui_package.html"
COMMAND_LINE_DOC_URL = CADBIOM_WEBSITE_URL + "doc/cadbiom/command_line_usage.html"
WORKFLOW_DOC_URL = CADBIOM_WEBSITE_URL + "doc/cadbiom/examples.html"

################################################################################

def logger(name=LOGGER_NAME, logfilename=None):
    """Return logger of given name, without initialize it.

    Equivalent of logging.getLogger() call.

    :Example::

        cm.logger(name=__name__)

    :param name: Name of the logger, only displayed if "%(name)s" is present in
        the logging.Formatter.
    """
    return logging.getLogger(name)

_logger = logging.getLogger(LOGGER_NAME)
_logger.setLevel(LOG_LEVEL)

# log file
formatter    = logging.Formatter(
    '%(asctime)s :: %(levelname)s :: %(message)s'
)
file_handler = RotatingFileHandler(
    DIR_LOGS + LOGGER_NAME + '_' + \
    dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.log',
    'a', 100000000, 1
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)
_logger.addHandler(file_handler)

# terminal log
stream_handler = logging.StreamHandler()
formatter      = logging.Formatter('%(levelname)s: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(LOG_LEVEL)
_logger.addHandler(stream_handler)

def log_level(level):
    """Set terminal/file log level to given one.

    .. note:: Don't forget the propagation system of messages:
        From logger to handlers. Handlers receive log messages only if
        the main logger doesn't filter them.
    """
    # Main logger
    _logger.setLevel(level.upper())
    # Handlers
    [handler.setLevel(level.upper()) for handler in _logger.handlers
        if handler.__class__ in (logging.StreamHandler,
                                 logging.handlers.RotatingFileHandler)
    ]
