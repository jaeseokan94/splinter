# -*- coding: utf-8 -*-
import warnings

from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.exceptions import DriverNotFoundError

def deprecate(cls, message):
    def new_init(self, *args, **kwargs):
        cls.__init__(self, *args, **kwargs)
        warnings.warn(message, DeprecationWarning)

    cls_dict = dict(cls.__dict__)
    cls_dict['__init__'] = new_init
    return type("Deprecated%s" % cls.__name__, (cls,), cls_dict)

_DRIVERS = {
    'firefox': FirefoxWebDriver,
    'chrome': ChromeWebDriver,
}

try:
    from splinter.driver.zopetestbrowser import ZopeTestBrowser
    _DRIVERS['zope.testbrowser'] = ZopeTestBrowser
except ImportError:
    pass


def Browser(driver_name='firefox', profile=None, extensions=[]):
    """
    Returns a driver instance for the given name.

    When working with ``firefox``, it's possible to provide a profile name and a
    list of extensions.

    If you don't provide any driver_name, then ``firefox`` will be used.

    If there is no driver registered with the provided ``driver_name``, this function
    will raise a :class:`splinter.exceptions.DriverNotFoundError` exception.
    """

    try:
        driver = _DRIVERS[driver_name]
        if driver_name == 'firefox':
            return driver(profile, extensions)
        else:
            return driver()
    except KeyError:
        raise DriverNotFoundError("No driver for %s" % driver_name)
