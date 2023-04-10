import logging
import traceback
import sys
import os
from time import sleep
from datetime import datetime, timezone
from aw_core.models import Event
from aw_core.log import setup_logging
from aw_client import ActivityWatchClient

from .lib import get_current_window
from .config import parse_args
from .macos_permissions import background_ensure_permissions

# from .chrome_watcher import chrome_watcher # Uncomment if you are using chrome watcher

logger = logging.getLogger(__name__)

# run with LOG_LEVEL=DEBUG
log_level = os.environ.get("LOG_LEVEL")
if log_level:
    logger.setLevel(logging.__getattribute__(log_level.upper()))

# Get windows signals in loop

import ctypes
from ctypes import c_long, c_int, c_wchar_p
from pathlib import WindowsPath
import time
import win32api
import win32con
import win32gui
import win32process

oldWndProc = None


def wndproc(hWnd, msg, wParam, lParam):
    logger.info(f"hwnd:{hWnd}, msg:{msg}, wParam: {wParam}, lparam : {lParam}")

    print("wndproc received message: %s" % msg)
    logger.info("wndproc received message: %s" % msg)

    if (msg == win32con.WM_QUERYENDSESSION):
        logger.info("wndproc received WM_QUERYENDSESSION")
        logger.info("RCVED WM_QUERYENDSESSION")
        logger.info('-' * 50)
        time.sleep(2)
        return 0

    elif (msg == win32con.WM_ENDSESSION):
        logger.info("wnproc received WM_ENDSESSION")
        logger.info("RCVED WM_ENDSESSION")
        logger.info('-' * 50)
        time.sleep(2)
        return 0

    elif msg == win32con.WM_POWERBROADCAST:
        logger.info("RCVED POWER BROADCAST")
        logger.info('-' * 50)
        time.sleep(2)
        return 0

    elif msg == win32con.PBT_APMSUSPEND:
        logger.info("RCVED POWER BROADCAST : PBT_APMSUSPEND")
        logger.info('-' * 50)
        time.sleep(2)
        return 0

    elif msg == win32con.PBT_APMSTANDBY:
        logger.info("RCVED POWER BROADCAST : PBT_APMSTANDBY")
        logger.info('-' * 50)
        time.sleep(2)
        return 0

    elif msg == win32con.PWR_SUSPENDREQUEST:
        logger.info("RCVED POWER BROADCAST : PWR_SUSPENDREQUEST")
        logger.info('-' * 50)
        return 0

    elif msg == win32con.PBT_APMQUERYSUSPEND:
        logger.info("RCVED POWER BROADCAST : PBT_APMQUERYSUSPEND")
        logger.info('-' * 50)
        time.sleep(2)
        return 0

    # Pass all messages to the original WndProc
    return win32gui.CallWindowProc(oldWndProc, hWnd, msg, wParam, lParam)


try:
    # Create a window just to be able to receive WM_QUERYENDSESSION messages
    win32api.SetLastError(0)
    hinst = win32api.GetModuleHandle(None)
    messageMap = {win32con.WM_QUERYENDSESSION: wndproc,
                  win32con.WM_ENDSESSION: wndproc,
                  win32con.WM_QUIT: wndproc,
                  win32con.WM_DESTROY: wndproc,
                  win32con.WM_CLOSE: wndproc,
                  win32con.WM_POWERBROADCAST: wndproc,
                  win32con.PBT_APMSUSPEND: wndproc,
                  win32con.PBT_APMSTANDBY: wndproc,
                  win32con.PWR_SUSPENDREQUEST: wndproc,
                  win32con.PBT_APMQUERYSUSPEND: wndproc}

    # print(messageMap)

    wndclass = win32gui.WNDCLASS()

    wndclass.hInstance = hinst
    wndclass.lpszClassName = "PreventShutdownWindowClass"

    wndclass.lpfnWndProc = messageMap

    myWindowClass = win32gui.RegisterClass(wndclass)

    hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,
                                   myWindowClass,
                                   "PreventShutdownWindow",
                                   0,
                                   0,
                                   0,
                                   win32con.CW_USEDEFAULT,
                                   win32con.CW_USEDEFAULT,
                                   0,
                                   0,
                                   hinst,
                                   None)

    logger.info('CreateWindowEx: ' + str(hwnd))
    logger.info('CreateWindowEx last error: ' + str(win32api.GetLastError()))
    print()

    # Set WndProc
    win32api.SetLastError(0)
    WndProcType = ctypes.WINFUNCTYPE(c_int, c_long, c_int, c_int, c_int)
    newWndProc = WndProcType(wndproc)
    oldWndProc = ctypes.windll.user32.SetWindowLongW(hwnd, win32con.GWL_WNDPROC, newWndProc)
    logger.info('SetWindowLong: ' + str(oldWndProc))
    logger.info('SetWindowLong last error: ' + str(win32api.GetLastError()))
    print()

except Exception as e:
    print("Exception: %s" % str(e))


def main():
    args = parse_args()
    if sys.platform.startswith("linux") and (
            "DISPLAY" not in os.environ or not os.environ["DISPLAY"]
    ):
        raise Exception("DISPLAY environment variable not set")

    setup_logging(
        name="aw-watcher-window",
        testing=args.testing,
        verbose=args.verbose,
        log_stderr=True,
        log_file=True,
    )

    if sys.platform == "darwin":
        background_ensure_permissions()

    client = ActivityWatchClient("aw-watcher-window", testing=args.testing)

    bucket_id = "{}_{}".format(client.client_name, client.client_hostname)
    event_type = "currentwindow"
    client.create_bucket(bucket_id, event_type, queued=True)

    logger.info("aw-watcher-window started")

    sleep(1)  # wait for server to start
    with client:
        heartbeat_loop(
            client,
            bucket_id,
            poll_time=args.poll_time,
            strategy=args.strategy,
            exclude_title=args.exclude_title,
        )


def heartbeat_loop(client, bucket_id, poll_time, strategy, exclude_title=False):
    while True:
        try:
            win32gui.PumpWaitingMessages()
            # logger.info("Checked for windows signals")

            if os.getppid() == 1:
                logger.info("window-watcher stopped because parent process died")
                break
            try:
                current_window = get_current_window(strategy)
                logger.debug(current_window)
            except Exception as e:
                logger.error(
                    "Exception thrown while trying to get active window: {}".format(e)
                )
                traceback.print_exc()
                current_window = {"app": "unknown", "title": "unknown", "url": "unknown"}

            now = datetime.now(timezone.utc)
            if current_window is None:
                logger.debug("Unable to fetch window, trying again on next poll")
            else:
                if exclude_title:
                    current_window["title"] = "excluded"

                current_window_event = Event(timestamp=now, data=current_window)
                client.heartbeat(
                    bucket_id, current_window_event, pulsetime=poll_time + 1.0, queued=True
                )
            # logger.info("Sleeping for 5 seconds")
            sleep(poll_time)
        except KeyboardInterrupt:
            logger.info("Stopped by keyboard Interrupt")
            break
