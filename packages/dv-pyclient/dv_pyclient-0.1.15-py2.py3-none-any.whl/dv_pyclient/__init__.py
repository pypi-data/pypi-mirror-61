"""Top-level package for Datavore Python Client."""

__author__ = """Datavore Labs"""
__email__ = 'info@datavorelabs.com'
__version__ = '0.1.15'

from .dv_pyclient import _login, _get_data, _load_df


def login(user_name, env_conf):
    return _login(user_name, env_conf)


def get_data(session, data_conf):
    return _get_data(session, data_conf)


def load_df(lines_in):
    return _load_df(lines_in)
