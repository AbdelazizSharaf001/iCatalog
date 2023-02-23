#!python3
import os
import sys

from dotenv import load_dotenv, find_dotenv

# fix local imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from app import create_app

# .env loader
load_dotenv(find_dotenv())

# server properity
app = create_app()
application = create_app()
