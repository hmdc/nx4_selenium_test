nx4_selenium_test
=================

Provides a Python class and apps which monitor and/or stress-test the NoMachine NX4 web interface

Setup
-----
* Clone this repo
* pip install selenium --user

```python
from nx4_selenium_test import NX4WebClient
x=NX4WebClient('http://dev-rce.hmdc.harvard.edu', 'USER', 'PASSWORD')
x.test_resume_session()
x.test_new_session()
```
