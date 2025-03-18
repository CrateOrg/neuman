# info: Extended Neuman Bot Library
# Additional functions related to OS detection and GUI interaction.

import org.sikuli.script.SikulixForJython
from sikuli import *
from neuman import *
from neuman_extend_images import *


def nm_detect_os():
    result_os = nm_detect(nmvi_os_indicators, nmv_os_names)

    if not result_os:
        result_os = nm_detect(nmvi_os_indicators_b, nmv_os_names, False)

    if not result_os:
        result_os = nm_detect(nmvi_os_indicators_c, nmv_os_names, False)

    if not result_os:
        nm_error("Could not detect the OS")

    nm_memory_set("current_os", result_os)

    nm_debug("Detected OS: " + result_os)
    return result_os


def nm_os_to_image(os_name, list_of_images):
    for i in nmv_os_names:
        if i == os_name:
            return list_of_images[nmv_os_names.index(i)]


def nm_gui_simple_run(command):
    # open terminal or run dialog,
    # run the command as current user,
    # then close the terminal immediately
    nm_think("I will start the program: " + command)

    # detect OS
    current_os = nm_memory_get("current_os")
    if not current_os:
        nm_error("must run nm_detect_os() before nm_gui_simple_run()")

    current_run_indicator = nm_os_to_image(current_os, nmvi_runas_indicators)
    current_delay = nm_memory_get("delay")

    # open terminal or run dialog
    if "Windows" in current_os:
        nm_keycombo('leftmeta r', current_delay)
    elif "Servermonkeys" in current_os and "XFCE" in current_os:
        nm_keycombo('leftmeta t', current_delay)
    elif "Debian" in current_os or "Linux" in current_os:
        nm_keycombo('leftctrl leftalt t', current_delay)
    else:
        nm_error("OS not supported: " + current_os)

    # verify that the terminal or run dialog is open
    try:
        wait(current_run_indicator, 3)
    except FindFailed:
        if "Windows" in current_os:
            nm_error("Could not open the run dialog")
        else:
            nm_error("Could not open a terminal")

    # run the command
    if "Windows" in current_os:
        nm_type(command, current_delay)
        nm_keycombo('enter', current_delay)
    else:
        # start the command in background
        nm_type(' nohup ' + command + " & exit", current_delay)
        nm_keycombo('enter', current_delay)
        # close the terminal
        nm_keycombo('leftctrl d', current_delay)


# open terminal or run dialog,
# become superuser if required,
# run the command as superuser or current user,
# then close the terminal if not preserved
# if "command" is empty then just open the terminal
# if "command" is not empty then run the command
# if "preserve" is True then keep the terminal open
# if "become" is True then become superuser via the password
def nm_gui_run(command="", preserve=False, become=False, password=""):
    # info
    if become:
        if password == "":
            nm_error("Password required to become super user")
        admin_term = "superuser "
    else:
        admin_term = ""
    if command != "":
        nm_think("I will open a " + admin_term + "terminal and a program")
    else:
        nm_think("I will open a " + admin_term + "terminal")

    # detect OS
    current_os = nm_memory_get("current_os")
    if not current_os:
        nm_error("must run nm_detect_os() before nm_gui_run()")
    current_run_indicator = nm_os_to_image(current_os, nmvi_runas_indicators)
    current_delay = nm_memory_get("delay")

    # early fail if superuser on Windows
    if "Windows" in current_os:
        if become:
            nm_error("Become superuser is not supported on Windows")
        if preserve:
            nm_think("Preserve is not supported in Windows Run dialog")

    # already running a terminal
    if exists(current_run_indicator, 0):
        if "Windows" in current_os:
            nm_think("A Run dialog is already open, restarting it")
            nm_keycombo('esc', current_delay)
            sleep(1)
            nm_keycombo('leftmeta r', current_delay)
            sleep(1)
            nm_keycombo('backspace', current_delay)
        elif "Debian" in current_os or "Linux" in current_os:
            nm_think("A terminal is already open")
            return False
        else:
            nm_error("OS not supported: " + current_os)
    # open new terminal or run dialog
    else:
        if "Windows" in current_os:
            nm_keycombo('leftmeta r', current_delay)
        elif "Servermonkeys" in current_os and "XFCE" in current_os:
            nm_keycombo('leftmeta t', current_delay)
        elif "Debian" in current_os or "Linux" in current_os:
            nm_keycombo('leftctrl leftalt t', current_delay)
        else:
            nm_error("OS not supported: " + current_os)

        # verify that the terminal or run dialog is open
        try:
            wait(current_run_indicator, 2)
        except FindFailed:
            if "Windows" in current_os:
                nm_error("Could not open the run dialog")
            else:
                nm_error("Could not open a terminal")

    # become the superuser
    if become:
        if "Debian" in current_os or "Linux" in current_os:
            nm_type('sudo -i', current_delay)
            nm_keycombo('enter', current_delay)
            nm_sleep(1)
            nm_debug("Typing the password")
            nm_type(password, current_delay)
            nm_keycombo('enter', current_delay)
            nm_sleep(1)
            nm_think("I am root now")

    # run the command
    if command != "":
        nm_think("And run the following command")
        if "Windows" in current_os:
            nm_type(command, current_delay)
        else:
            if preserve:
                nm_type(command, current_delay)
            else:
                nm_type(' nohup ' + command + " & exit", current_delay)
        # confirm the command
        nm_keycombo('enter', current_delay)

    # close the terminal
    if not preserve:
        if "Windows" in current_os:
            nm_keycombo('esc', current_delay)
        else:
            nm_keycombo('leftctrl d', current_delay)
            nm_keycombo('leftctrl d', current_delay)

    return True


# wait for a terminal to finish running a command
# set a timeout in seconds to prevent infinite waiting
# set timeout to what you assume is the maximum time the command will take
# default is 2 minutes
def nm_gui_run_done(close=False, timeout=120):
    # convert timeout to minutes
    if timeout > 60:
        timeout_min = timeout / 60
        timeout_msg = str(timeout_min) + " minutes"
    else:
        timeout_msg = str(timeout) + " seconds"
    nm_think("Waiting max " + timeout_msg + " for terminal to finish")
    # detect OS
    current_os = nm_memory_get("current_os")
    if not current_os:
        nm_error("must run nm_detect_os() before nm_gui_run_done()")

    if "Windows" not in current_os:
        # wait for command to finish
        current_term = nm_os_to_image(current_os, nmvi_term_done)
        current_term_sudo = nm_os_to_image(current_os, nmvi_term_done_sudo)

        timeout_count = 0
        term_is_sudo = False
        while timeout_count < timeout:
            if exists(current_term, 0):
                break
            elif exists(current_term_sudo, 0):
                term_is_sudo = True
                break
            timeout_count = timeout_count + 1
            nm_sleep(1)

        if close:
            # if timeout_count is more than 60 seconds convert to minutes
            if timeout_count > 60:
                timeout_count = timeout_count / 60
                time_msg = str(timeout_count) + " minutes"
            else:
                time_msg = str(timeout_count) + " seconds"
            nm_think("Program took " + time_msg)
            nm_debug("Closing the terminal")
            nm_keycombo('leftctrl d')
            if term_is_sudo:
                nm_keycombo('leftctrl d')
    else:
        nm_debug("Windows does not need to wait for terminal to finish")


# DEMO MAIN ##################################################################

if __name__ == '__main__':
    nm_think("Current OS is: " + nm_detect_os())
