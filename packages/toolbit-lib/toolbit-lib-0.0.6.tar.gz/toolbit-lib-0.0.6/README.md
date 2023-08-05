# Toolbit library for Python

The target device of this library is **Toolbit DMM**, Digital Multi Meter, that is used with PC to measure DC voltage or current.


# Installation

The toolbit-lib package is published to the PyPI repository. Please install it as follows as:

### Ubuntu linux
```shell
  sudo apt install libudev-dev
  pip3 install toolbit-lib
```

### macOS
```shell
  pip3 install toolbit-lib
```

### Windows
```shell
  pip3 install toolbit-lib
```

### Raspberry Pi
```shell
  sudo apt install libudev-dev
  pip3 install toolbit-lib
```


# Usage

### Example

```python
from toolbit import Dmm

dmm = Dmm()
dmm.open()
print(str('%03.3f' % dmm.getVoltage()) + " [V]")
print(str('%03.3f' % (1000.0 * dmm.getCurrent())) + " [mA]")
```


# Build

The following software is required to build toolbit-lib from source code:
  * swig: http://www.swig.org/

### Ubuntu linux, macOS, Rasberry Pi
```shell
  cd bindings/python/toolbit-lib
  make
  sudo make install
```

### Windows
```shell
  cd bindings/python/toolbit-lib
  build.bat
  python setup.py install
```


# License

[GPLv2] Please refer to the LICENSE file in this repository
