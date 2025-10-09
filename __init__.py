import platform
import sys

if platform.system() != 'Windows':
    sys.exit("This package is for Windows only.")
