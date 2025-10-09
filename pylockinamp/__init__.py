import platform
import sys
from .pylockinamp import pylockinamp

if platform.system() != 'Windows':
    sys.exit("This package is for Windows only.")

def __call__():
    return pylockinamp()

# モジュールを呼び出し可能にするためのマジック
sys.modules[__name__] = __call__
