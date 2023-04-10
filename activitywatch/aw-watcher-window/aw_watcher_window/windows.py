from typing import Optional
import logging

import wmi  # windows media interface
import win32gui
import win32process
import win32api

import uiautomation as auto
from pywinauto import Application

c = wmi.WMI()
"""
Much of this derived from: http://stackoverflow.com/a/14973422/965332
"""


def get_app_path(hwnd) -> Optional[str]:
    """Get application path given hwnd."""
    path = None
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    for p in c.query('SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
        path = p.ExecutablePath
        break
    return path


def get_app_name(hwnd) -> Optional[str]:
    """Get application filename given hwnd."""
    name = None
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
        name = p.Name
        break
    # logging.info("App Name : {}".format(name))
    return name


def get_window_title(hwnd):
    return win32gui.GetWindowText(hwnd)


def get_active_window_handle():
    hwnd = win32gui.GetForegroundWindow()
    return hwnd


def getUrl(wnd):
    '''Gets complete url address if the hwnd is browser'''
    # window = win32gui.GetForegroundWindow()
    win_name = win32gui.GetWindowText(wnd)
    if 'Google Chrome' in win_name or 'Edge' in win_name or 'Firefox' in win_name or 'Opera' in win_name or 'AVGSecure' in win_name:
        chromeControl = auto.ControlFromHandle(wnd)
        edit = chromeControl.EditControl()
        url = edit.GetValuePattern().Value
        if url is not None:
            return url


if __name__ == "__main__":
    hwnd = get_active_window_handle()
    print("Title:", get_window_title(hwnd))
    print("App:", get_app_name(hwnd))
    print("URL:", getUrl(hwnd))
