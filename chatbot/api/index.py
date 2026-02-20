"""Vercel Python Serverless Function entry point."""
import sys
import os

# Ensure chatbot package is on the path when running as Vercel function
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="off")
