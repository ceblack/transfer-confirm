#!/usr/bin/env python3
import logging
import sys

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
