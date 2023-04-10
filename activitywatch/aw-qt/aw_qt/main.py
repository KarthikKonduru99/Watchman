import os
import sys
import logging
import click
from typing import Optional

import psutil
from aw_core.log import setup_logging
from .manager import Manager
from . import trayicon
from .config import AwQtSettings
from datetime import date, datetime

import threading
import time

logger = logging.getLogger(__name__)

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def check_for_service():
    ''' Method runs for every 10 minutes to check services running if any services are not running make attempt to
    restart '''
    try:
        srvc = ['aw-server','aw-watcher-afk', 'aw-watcher-window']
        to_start = []
        for proc in srvc:
            if checkIfProcessRunning(proc):
                continue
            else:
                to_start.append(proc)
                logger.warning(f'Process {proc} is not running')
                logger.info(f"Restarting {proc}")
                _manager = Manager()
                _manager.start(proc,)
    except Exception as e:
        logger.error("Exception : {}".format(e))

@click.command("aw-qt", help="A trayicon and service manager for ActivityWatch")
@click.option(
    "--testing", is_flag=True, help="Run the trayicon and services in testing mode"
)
@click.option(
    "--autostart-modules",
    help="A comma-separated list of modules to autostart, or just `none` to not autostart anything.",
)

def main(testing: bool, autostart_modules: Optional[str]) -> None:
    try:
        logger.info('-' * 50)
        logger.info("Checking for instance and initiating instance object..")
        from .singlinstance import SingleInstance,SingleInstanceException
        instance = SingleInstance()
        logger.info("Object Initialised. No Instance is running continuing...")
        logger.info('-' * 50)
    except SingleInstanceException:
        logger.warning("Tried to initiate new ActivityWatch")
        from .trayicon import show_module_already_running
        show_module_already_running()
        sys.exit(-1)

    config = AwQtSettings(testing=testing)
    _autostart_modules = (
        [m.strip() for m in autostart_modules.split(",") if m and m.lower() != "none"]
        if autostart_modules
        else config.autostart_modules
    )
    setup_logging("aw-qt", testing=testing, verbose=testing, log_file=True)

    _manager = Manager(testing=testing)
    _manager.autostart(_autostart_modules)
    logger.info('-' * 80)
    logger.info("Intiating Scheduler Thread")
    def schedule():
        while 1:
            check_for_service()
            time.sleep(10)

    # makes our logic non blocking
    thread = threading.Thread(target=schedule)
    thread.start()
    logger.info('-'*80)
    logger.info(f"JOB Thread {thread.is_alive()}")
    error_code = trayicon.run(_manager, testing=testing)
    _manager.stop_all()
    sys.exit(error_code)