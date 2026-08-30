"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Ensures the SourceCode directory is importable as the 'api' package during tests.
"""

import sys
from pathlib import Path

SOURCE_CODE_DIR = Path(__file__).resolve().parents[2]
if str(SOURCE_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_CODE_DIR))
