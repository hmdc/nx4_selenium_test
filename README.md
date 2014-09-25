nx4_selenium_test
=================

Provides a Python class and apps which monitor and/or stress-test the NoMachine NX4 web interface

Setup
-----
* Clone this repo
* python setup.py install

Run
----
```python
from nx4_selenium_test import NX4WebClient
x=NX4WebClient('http://dev-rce.hmdc.harvard.edu', 'USER', 'PASSWORD')
x.test_resume_session()
x.test_new_session()
```

Stress Test
-----------
```shell
/usr/local/bin/nx4_stress.py -h
usage: nx4_stress.py [-h] [-d] -l LOCATION -u USER -p PASSWD -i
ITERATIONS

Stress test NX4 web interface

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enables verbose output.
  -l LOCATION, --location LOCATION
                        URI of NoMachine NX4 web server
  -u USER, --user USER  Usernames separated by a space
  -p PASSWD, --passwd PASSWD
                        Username password
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations

/usr/local/bin/nx4_stress.py -l http://my.nx4.location.com -u `echo test_user{1..10}` -p testuserpasswd -i 15
```
