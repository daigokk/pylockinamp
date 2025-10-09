import platform
import sys
from .pyliamp import pyliamp

if platform.system() != 'Windows':
    sys.exit("This package is for Windows only.")

def __call__():
    return pylia()

# モジュールを呼び出し可能にするためのマジック
sys.modules[__name__] = __call__
