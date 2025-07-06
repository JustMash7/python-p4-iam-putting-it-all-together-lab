import sys
import os
import pytest

# Add server directory to Python path
server_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, server_dir)

# Run pytest
if __name__ == '__main__':
    pytest.main(['testing'])