# -*- coding: utf-8 -*-

"""run.py

The main entry-point for the web application. Loads environment variables and
launches the server.
"""

from dotenv import load_dotenv
from gello.app import GelloServer

load_dotenv()
GelloServer()
