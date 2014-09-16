from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NX4WebClient:
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
      print("** Unable to login. Timeout exceeded.")
      return

    # Login
    login_element.send_keys(user)
    password_element.send_keys(passwd)
    login_element.send_keys(Keys.RETURN)
    print("** Logging in to " + uri + "\n")

    # Wait until we see the 'CONNECT' button, somewhere.
    try:
      operation_button = WebDriverWait(driver, _GLOBAL_TIMEOUT).until(
          EC.presence_of_element_located((By.ID, 'group_button_session_owner'))
      )
    except:
      print("** Unable to display session list. Timeout hit.")
      return

  def _nx4_existing_session(self):
    """
    _nx4_existing_session() checks to see whether a session already
    exists in the session list. This can only be run after _nx4_login().
    If a session exists, returns that session element, otherwise returns
    None.
    """
    try:
      existing_session = self.driver.find_element_by_name("Research Cloud Environment (RCE)")
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
      _msg_start = "** Resuming session"
      _msg_fail = "** Session unable to be resumed. Timeout hit."
      _msg_success = "** Session resumed successfully."

      _session = session
    else:
      _msg_start = "** Starting new session"
      _msg_fail = "** Session unable to be started. Timeout hit."
      _msg_success = "** Session started successfully."

      _session = WebDriverWait(driver, _GLOBAL_TIMEOUT).until(
          EC.presence_of_element_located((By.ID, 'unix-xsession-default'))
      )

    _session.click()

    opButton = driver.find_element_by_id("opButton")
    opButton.click()

    print(_msg_start)

    try:
      WebDriverWait(driver, _GLOBAL_TIMEOUT + 15).until(
          EC.presence_of_element_located((By.ID, "image_1"))
      )
    except:
      print(_msg_fail)
      return

    print(_msg_success)

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

