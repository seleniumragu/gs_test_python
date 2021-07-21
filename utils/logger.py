# -*- coding: utf-8 -*-
import logging
import sys


def _logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                '%Y-%m-%d %H:%M:%S'
            )
        )

        logger.addHandler(handler)

    return logger


logger = _logger(__name__)
