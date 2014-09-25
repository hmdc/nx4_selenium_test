from distutils.core import setup

setup(name='nx4_selenium_test',
      version='0.2',
      description='Provides a Python class and apps which monitor\
      and/or stress-test the NoMachine NX4 web interface',
      url='https://github.com/hmdc/nx4_selenium_test',
      author='Evan Sarmiento',
      author_email='esarmien@g.harvard.edu',
      license='MIT',
      packages=['nx4_selenium_test'],
      requires=['selenium'],
      scripts=['scripts/nx4_stress.py']
)
