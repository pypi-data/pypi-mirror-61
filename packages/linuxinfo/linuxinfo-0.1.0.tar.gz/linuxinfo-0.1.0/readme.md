# Linux Information

**work in progress**

Answers:

- is this a raspberry pi?
    - functions return `None` on error
- is this a raspbian or ubuntu distro?
- is this distro based on debian?
- reads `/proc/cpuinfo` for revision code
- reads `/etc/os-release` for linux OS info

## Info

Reads the [revision code](https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md)
which encodes a bunch of information as `uuuuuuuuFMMMCCCCPPPPTTTTTTTTRRRR`. This library
decodes that number.

```python
RPiInfo = namedtuple("RPiInfo", "type processor memory revision manufacturer flag")
LinuxInfo = namedtuple("LinuxInfo", "distro distro_pretty debian_based version version_codename")
```

## Example

```python
from linuxinfo import linux_info()
from linuxinfo import pi_info
from linuxinfo import RPiInfo, LinuxInfo  # not sure you need these
from linuxinfo.rpi import decode          # normally you don't use this!

# given a revision code, it decodes it (see below). Normally you
# wouldn't do this ... this is just a test
print(decode(0xa020a0))  # compute module 3
print(decode(0xa22042))  # Pi2B
print(decode(0xc03111))  # Pi4B

print(pi_info())  # reads /proc/cpuinfo and get revision code
```

```
RPiInfo(type='CM3', processor='BCM2837', memory='1GB', revision=0, manufacturer='Sony UK', flag='new-style revision')
RPiInfo(type='2B', processor='BCM2837', memory='1GB', revision=2, manufacturer='Embest', flag='new-style revision')
RPiInfo(type='4B', processor='BCM2711', memory='4GB', revision=1, manufacturer='Sony UK', flag='new-style revision')
```

# Change Log

| Date        | Version | Notes      |
|-------------|---------|------------|
| 2020 Dec 4  | 0.1.0   | changed name because it does more |
| 2019 Oct 27 | 0.0.3   | simple clean up |
| 2019 Oct 27 | 0.0.1   | init            |


# MIT License

**Copyright (c) 2019 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
