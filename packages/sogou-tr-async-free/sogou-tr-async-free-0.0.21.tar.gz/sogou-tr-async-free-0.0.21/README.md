# sogou-tr-async-free ![Python3.6|3.7 package](https://github.com/ffreemt/sogou-tr-async-free/workflows/Python3.6%7C3.7%20package/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/sogou-tr-async-free/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/sogou-tr-async)
sogou translate for free with async and proxy support

### Installation
Not available yet
```pip install sogou-tr-async-free```

Validate installation
```
python -c "import sogou_tr_async; print(sogou_tr_async.__version__)"
0.0.1
```

### Usage

```
import asyncio
from sogou_tr_async import sogou_tr_async

asyncio.get_event_loop().run_until_complete(sogou_tr_async('test this and that'))
# '测试这个和那个'
```

### Acknowledgments

* Thanks to everyone whose code was used
