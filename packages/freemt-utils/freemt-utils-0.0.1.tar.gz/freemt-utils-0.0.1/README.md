# freemt-utils ![Python3.6|3.7 package](https://github.com/ffreemt/freemt-utils/workflows/Python3.6%7C3.7%20package/badge.svg)![Codecov](https://github.com/ffreemt/freemt-utils/workflows/Codecov/badge.svg)

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
import asyncio
from freemt_utils import save_tempfile, switch_to, httpx_get, make_url, arun, fetch_proxies

res = asyncio.get_event_loop().run_until_complete(httpx_get('http://www.baidu.com'))
print(res.headers)
# ...
```