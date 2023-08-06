# freemt-utils ![Python3.6|3.7 package](https://github.com/ffreemt/freemt-utils/workflows/Python3.6%7C3.7%20package/badge.svg)![Codecov](https://github.com/ffreemt/freemt-utils/workflows/Codecov/badge.svg)[![PyPI version](https://badge.fury.io/py/freemt-utils.svg)](https://badge.fury.io/py/freemt-utils)

various utils for freemt

### Installation

```pip install freemt-utils```

Validate installation
```
python -c "import freemt_utils; print(freemt_utils.__version__)"
0.0.1
```

### Usage

```
from pathlib import Path
import asyncio
from freemt_utils import save_tempfile, switch_to, httpx_get, make_url, arun, fetch_proxies, logger_level

with switch_to():
  print(Path.cwd())  # home dir
print(Path.cwd())  # back to the current work directory

try:
  arun(httpx_get('www.baidu.com'))
except Exception as exc:
  print(exc)  # InvalidURL: No scheme included in URL.

res = arun(httpx_get(make_url('www.baidu.com')))
print(res.headers)
# Headers([('bdpagetype', '1'), ('bdqid',...

logger_level('info')

res.encoding = 'UTF-8'
save_tempfile(res.text)  # display res.text in the default browser

```