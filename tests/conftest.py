import os
import sys

# Configuration file to add the parent directory to the Python path for the tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
