# google-sign
![Python 3637 package](https://github.com/ffreemt/google-sign/workflows/Python3.6|3.7%20package/badge.svg) [![codecov](https://codecov.io/gh/ffreemt/google-sign/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/google-sign) [![PyPI version](https://badge.fury.io/py/google-sign.svg)](https://badge.fury.io/py/google-sign)![status](https://img.shields.io/badge/status-alpha-orange.svg)

Calculate sign string for google translate and baidu translate

### Installation

```pip install google-sign```

```
python -c "from google_sign import google_sign; print(google_sign('test'))"
476257.126138
```

### Usage

```
from google_sign import google_sign, js2py_sign, GTK

sign = google_sign('test')  #
print(sign)  # '476257.126138'

# for baidu translate text upto 30
sign = google_sign('test', GTK)  #
print(sign)  # '431039.159886'

# for baidu translate text longer than 30
sign = google_sign('test ' * 10)
print(sign)  # '403909.183028'

sign = google_sign('test ' * 10, GTK)
print(sign)  # ditto

```

### Acknowledgments

* Thanks to everyone whose code was used
