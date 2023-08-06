# Pybar

[![image](https://img.shields.io/badge/Pypi-0.1.0.1-green.svg)](https://pypi.org/project/guang)
[![image](https://img.shields.io/badge/python-3.X-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/MIT-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-K.y-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)




Easy to use progress bar display for python.





## Installation

```bash
pip install pyprobar
```



## Examples

* Use `probar` or `bar` to display current progress

  ```python
  from pyprobar import bar, probar
  import time
  for idx, x in probar(range(10)):
      time.sleep(0.8)
  
  >> 100.00% |█████████████████████████████| 0'7.2"|0'7.2" ETC: 12-2 23:59:8
  
  import numpy as np
  N = 1024
  a = np.linspace(2, 5, N)
  for idx, i in enumerate(a):
      time.sleep(0.01)
      bar(idx, N)
  >> 100.00% |█████████████████████████████| 0:00:00|0:00:10  ETC: 02-19 20:33:34 
  ```