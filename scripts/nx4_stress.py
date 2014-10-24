#!/usr/bin/env python
from nx4_selenium_test import NX4WebClient
from time import sleep
import signal
import multiprocessing
import argparse

def test_new_session_loop(client, uri, user, passwd, iterations=10):
  # We want this to go on forever, we know it's gonna mess up sometimes.
  
  for i in range(0, iterations):
    try:
      print "[" + str(i) + "]" + " Starting test_new_session_loop()"
      client.test_new_session()
    except:
      pass



def test_resume_session_loop(client, uri, user, passwd, iterations=10):

  for i in range (0, iterations):
    try:
      print "[" + str(i) + "]" + " Starting test_resume_session_loop()"
      client.test_resume_session()
    except:
      pass



def test_new_resume_delay_loop(client, uri, user, passwd, iterations=10):

  for i in range (0, iterations):
    try:
      print "[" + str(i) + "]" + " Starting test_new_resume_delay_loop()"
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
  client = NX4WebClient(uri, user, passwd)

  try:
    _iterations = info['iterations']
  except:
    _iterations = None

  if _iterations:
    test(client, uri, user, passwd, iterations=_iterations)
  else:
    test(client, uri, user, passwd)

  client.done()


# number of iterations
# processes, and username list must be equal
# username list

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Stress test NX4 web\
      interface")

  parser.add_argument('-d', '--debug', action='store_true',
                      help="Enables verbose output.")
  parser.add_argument('-l', '--location', required=True,
                      help="URI of NoMachine NX4 web server")
  parser.add_argument('-u', '--user', required=True,
                      help="Usernames separated by a space")
  parser.add_argument('-p', '--passwd', required=True,
                      help="Username password")
  parser.add_argument('-i', '--iterations', required=True, type=int,
                      help="Number of iterations")

  args = parser.parse_args()

  _users = args.user.split(" ")
  _passwd = args.passwd
  _uri = args.location
  _num_processes = len(_users)
  _iterations = args.iterations

  lp = []

  for usr in _users:
    lp_obj = {
        'test': test_new_resume_delay_loop,
        'uri': _uri,
        'user': usr,
        'passwd': _passwd,
        'iterations': _iterations
        }
    lp.append(lp_obj)


  pool = multiprocessing.Pool(processes=_num_processes)
  
  try:
    pool.map_async(nx4_worker, lp)
    pool.close()
    pool.join()
  except KeyboardInterrupt:
    print "Caught Ctrl+C, terminating workers."
    pool.terminate()
    pool.join()
