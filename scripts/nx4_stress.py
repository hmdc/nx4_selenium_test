#!/usr/local/bin/python
from nx4_selenium_test import NX4WebClient
from time import sleep
import multiprocessing

_GLOBAL_TIMEOUT = 30

def test_new_session_loop(uri, user, passwd):
  client = NX4WebClient(uri, user, passwd)
  # We want this to go on forever, we know it's gonna mess up sometimes.
  while 1:
    try:
      client.test_new_session()
    except:
      pass

def test_resume_session_loop(uri, user, passwd):
  client = NX4WebClient(uri, user, passwd)
  while 1:
    try:
      client.test_resume_session()
    except:
      pass

def test_new_resume_delay_loop(uri, user, passwd):
  client = NX4WebClient(uri, user, passwd)
  while 1:
    try:
      client.test_new_session()
      sleep(20)
      client.test_resume_session()
      sleep(20)
    except:
      pass

def nx4_worker(info):
  # q is user,passwd
  test = info['test']
  uri = info['uri']
  user = info['user']
  passwd = info['passwd']

  test(uri, user, passwd)

# number of iterations
# processes, and username list must be equal
# username list

if __name__ == '__main__':
  lp = []
  for i in range(1, 6):
    user = "rcetest" + str(i)
    lp_obj = {
        'test': test_new_session_loop,
        'uri': 'http://dev-rce.hmdc.harvard.edu',
        'user': user,
        'passwd': 'XYZ',
    }
    lp.append(lp_obj)

  pool = multiprocessing.Pool(processes=5)
  pool_outputs = pool.map(nx4_worker, lp)
  pool.close()
  pool.join()

