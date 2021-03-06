from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class client:
  _GLOBAL_TIMEOUT = 30

  """This class can run a number of tests on an NX4 web client"""
  def __init__(self, uri, user, passwd):
    """
    Starts Firefox.
    Sets the URI, user, and password.
    """
    self.driver = webdriver.Firefox()
    self.uri = uri
    self.user = user
    self.passwd = passwd
    self.pid = os.getpid()

  def done(self):
    self.driver.quit()

  def _nx4_login(self):
    """
    _nx4_login() attempts to load self.uri, login with the specified
    username and password and also checks whether or not the session
    list becomes visible after login.
    """

    # Have we displayed the login window?
    driver = self.driver
    uri = self.uri
    user = self.user
    passwd = self.passwd
    _GLOBAL_TIMEOUT = self._GLOBAL_TIMEOUT

    driver.get(uri)

    try:
      login_element = WebDriverWait(driver, _GLOBAL_TIMEOUT).until(
          EC.presence_of_element_located((By.ID, 'nxserverlogin'))
      )
      password_element = WebDriverWait(driver, _GLOBAL_TIMEOUT).until(
          EC.presence_of_element_located((By.ID, 'nxserverpass'))
      )
    except:
      print("[%d]:result:nx4_login=-1,NO_LOGIN_ELEMENTS_TIMEOUT_EXCEEDED." %(self.pid))
      return

    # Clear both L/P
    login_element.clear()
    password_element.clear()

    login_element.send_keys(user)
    password_element.send_keys(passwd)
    login_element.send_keys(Keys.RETURN)

    print("[%d]:info:Logging in to %s" %(self.pid, self.uri))

    # Wait until we see the 'CONNECT' button, somewhere.
    try:
      operation_button = WebDriverWait(driver, _GLOBAL_TIMEOUT).until(
          EC.presence_of_element_located((By.ID, 'group_button_session_owner'))
      )
    except:
      print("[%d]:result:nx4_login=-1,NO_SESSION_LIST_TIMEOUT_EXCEEDED" %(self.pid))
      return

  def _nx4_existing_session(self):
    """
    _nx4_existing_session() checks to see whether a session already
    exists in the session list. This can only be run after _nx4_login().
    If a session exists, returns that session element, otherwise returns
    None.
    """
    try:
      existing_session = self.driver.find_element_by_name("Research Computing Environment (RCE)")
    except:
      existing_session = None

    return existing_session

  def _nx4_terminate_session(self, session):
    """
    _nx4_terminat_session() takes a sesion object as an element an
    termimnates it. This can only be done after _nx4_login() and
    _nx4_existing_session()
    """

    driver = self.driver

    session.click()
    actions = ActionChains(driver)
    actions.move_to_element(session).context_click().perform()
    driver.find_element_by_link_text('Terminate session').click()

  def _nx4_start_session(self, session=None):
    """
    _nx4_start_session() either starts or resumes a session, if session
    is defined as an argument.
    """

    driver = self.driver
    _GLOBAL_TIMEOUT = self._GLOBAL_TIMEOUT

    if session:
      _function = "nx4_resume_session"
      _msg_start = "Resuming session"
      _msg_fail = "Session unable to be resumed. Timeout hit."
      _msg_success = "Session resumed successfully."

      _session = session
    else:
      _function = "nx4_start_session"
      _msg_start = "Starting new session"
      _msg_fail = "Session unable to be started. Timeout hit."
      _msg_success = "Session started successfully."

      #print("Waiting for the new desktop button..")

      #_new_desktop_click = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[2]/span')

      #_new_desktop_click = WebDriverWait(driver, _GLBOAL_TIMEOUT).until(
      #    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[2]/span'))
      #    )

      print ("[%d]:info:clicking new desktop button" %(self.pid))

      #_new_desktop_click.click()

      _session = WebDriverWait(driver, _GLOBAL_TIMEOUT).until(
          EC.presence_of_element_located((By.ID, 'unix-xsession-default'))
      )

    _session.click()

    opButton = driver.find_element_by_id("opButton")
    opButton.click()

    print ("[%d]:info:%s" %(self.pid, _msg_start))

    try:
      WebDriverWait(driver, _GLOBAL_TIMEOUT + 15).until(
          EC.presence_of_element_located((By.ID, "image_1"))
      )
    except:
      try:
        # <img src="/nxplayer/images/shared/equalizer.png"
        # style="float:left;margin-top:9px;margin-left:2px;width:104px;">
        driver.find_element_by_css_selector("img[src='/nxplayer/images/shared/equalizer.png']")
      except:
        print("[%d]:result:%s=-1,%s" %(self.pid,_function,_msg_fail))
        return

    print("[%d]:result:%s=1,%s" %(self.pid,_function,_msg_success))

  def test_resume_session(self):
    """test_resume_session() resumes an NX4 session. If no session is
    present, starts a new session and then resumes"""

    self._nx4_login()
    existing_session = self._nx4_existing_session()
    if existing_session:
      self._nx4_start_session(existing_session)
    else:
      self._nx4_start_session()
      # Now we should runt his test again..
      self.test_resume_session()

  def test_new_session(self):
    """test_new_session() starts a new session and terminates a session
    if already present."""

    # Try to login
    self._nx4_login()
    
    # Do we have an existing session? If so, terminate
    existing_session = self._nx4_existing_session()
    if existing_session:
      self._nx4_terminate_session(existing_session)

    self._nx4_start_session()

