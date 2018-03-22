# -*- coding: utf-8 -*-

""""""

from .. import celery


@celery.task
def send_async_test(msg):
    logger = send_async_test.get_logger()
    logger.info(msg)
    print(msg)
