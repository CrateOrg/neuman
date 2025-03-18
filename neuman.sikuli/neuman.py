# info: Neuman Bot Library
# This is the basic library, it shall not include any images or specific file
# dependencies. It should be able to run without any additional files.

import org.sikuli.script.SikulixForJython
from sikuli import *
import os
from subprocess import PIPE, Popen


# FUNCTIONS ##################################################################

def nm_error(text):
    Debug.error(text)
    exit(1)


# will write to log and show while using 'state' option
# use this for normal bot behavior
def nm_log(text):
    Debug.user(text)


# will write [info] debug data to log
# use this only for debugging and development
def nm_debug(text):
    if env_debug == 'true':
        Debug.info(text)


# will write [info] debug data to log and show in console
# use this only for debugging and development
def nm_debug_verbose(text):
    if env_debug == 'true':
        print(text)
        Debug.info(text)


def nm_set_env(var_name, valid_values, optional=False):
    default_value = valid_values[0]
    env_value = os.getenv(var_name)

    if not env_value or (valid_values and env_value not in valid_values):
        if not env_value:
            env_value = default_value
        elif optional:
            if var_name == '':
                nm_error(var_name + " is not set correctly.")
        else:
            nm_error(var_name + " is not set correctly.")

    msg = var_name + ": " + env_value
    print(msg)
    nm_log(msg)
    return env_value


def nm_create_config():
    # always start with a fresh memory if the instance is 'default'
    if env_instance == 'default':
        if os.path.exists(nmv_path_instance):
            os.system('rm -rf ' + nmv_path_instance)

    # create the base folder
    if not os.path.exists(nmv_path_instance):
        os.makedirs(nmv_path_instance)

    # remember the environment variables
    nm_memory_set("NEUMAN_DEBUG", env_debug)
    nm_memory_set("NEUMAN_HOST", env_host)
    nm_memory_set("NEUMAN_THOUGHT", env_thought)

    # set base fatique to 0
    if env_instance == 'default':
        nm_fatique_set(0)

    # get the name of the main python script file
    script_name = os.path.basename(getBundlePath())
    # remove ".sikuli" from the end of the name
    script_name = script_name.replace(".sikuli", "")
    log_dir = os.path.expanduser("~") + "/.local/share/neuman/logs"
    log_file = log_dir + "/" + script_name + ".log"
    # check if log file exists
    if not os.path.exists(log_file):
        nm_error("Log file not found: " + log_file)

    # bugfix:
    # remove useless error los a where you can't disable hotkey conflicts
    strip_1 = "[error] Hot key conflicts"
    strip_2 = "[error] HotkeyManager: addHotkey: failed"
    with open(log_file, "r") as f:
        log_data = f.readlines()
    with open(log_file, "w") as f:
        for line in log_data:
            # remove specific lines from the log file
            if strip_1 not in line and strip_2 not in line:
                f.write(line)


def nm_click(image):
    click(image)


def nm_db_get(flat_file_db, var_name):
    name = str(var_name)

    found_var = ""
    if os.path.exists(flat_file_db):
        with open(flat_file_db, "r") as file:
            for line in file:
                if line.startswith(name + "="):
                    found_var = line.split("=", 1)[1].strip()
                    break
    else:
        nm_error("Storage file not found: " + flat_file_db)

    return found_var


def nm_db_set(flat_file_db, var_name, var_value):
    name = str(var_name)
    value = str(var_value)

    # if the memory already exists, update it
    if os.path.exists(flat_file_db):
        with open(flat_file_db, "r") as file:
            lines = file.readlines()

        with open(flat_file_db, "w") as file:
            found = False
            for line in lines:
                if line.startswith(name + "="):
                    file.write(name + "=" + value + "\n")
                    found = True
                else:
                    file.write(line)
            if not found:
                file.write(name + "=" + value + "\n")
    else:
        with open(flat_file_db, "w") as file:
            file.write(name + "=" + value + "\n")


# detect if any part of the screen matches a list of images and return names
def nm_detect(img_list_indicators, list_of_names, certain=True):
    if certain:
        msg_certainty = "know"
    else:
        msg_certainty = "believe"

    counter = 0
    for i in img_list_indicators:
        if i != 0:
            if exists(i, 0):
                nm_debug("nm_detect found img: " + str(i))
                name_matches = list_of_names[counter]
                nm_think("I " + msg_certainty + " this is " + name_matches)
                return name_matches
        counter = counter + 1
    return False


def nm_fatique_add(integer):
    if not isinstance(integer, int):
        nm_error("nm_fatique_set: not an integer: " + str(integer))
    fatique = nm_memory_get("fatique")

    if not fatique:
        fatique = 0
    fatique_new = int(fatique) + int(integer)
    nm_log("Fatique: +" + str(integer) + " now " + str(fatique_new))
    nm_memory_set("fatique", fatique_new)


def nm_fatique_get():
    fatique = nm_memory_get("fatique")
    fatique_int = int(fatique)
    return fatique_int


def nm_fatique_remove(integer):
    fatique = nm_memory_get("fatique")
    fatique_new = int(fatique) - int(integer)
    nm_log("Fatique: -" + str(integer) + " now " + str(fatique_new))
    nm_memory_set("fatique", fatique_new)


def nm_fatique_set(integer):
    if not isinstance(integer, int):
        nm_error("nm_fatique_set: not an integer: " + str(integer))

    nm_memory_set("fatique", integer)


def nm_host_cmd(cmd):
    # sikulis native way 'run(cmd)' does not work properly

    # debug
    if env_debug == 'true':
        nm_debug("Host cmd: " + cmd)
    else:
        cmd_bin = cmd.split(" ")[0]
        if cmd_bin == "autovoice" or cmd_bin == "autotype":
            pass
        else:
            nm_debug("Host cmd: " + cmd_bin)

    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout_raw, stderr_raw = p.communicate()
    stdout_clean = str(stdout_raw) \
        .replace("b''", "").replace("b'", "").replace("b\"", "")
    stderr_clean = str(stderr_raw) \
        .replace("b''", "").replace("b'", "").replace("b\"", "")
    stdout = stdout_clean.replace(r"\n'", "").replace(r"\n", " ")
    stderr = stderr_clean.replace(r"\n'", "").replace(r"\n", " ")

    if p.returncode != 0:
        if stdout != '':
            nm_error("nm_host_cmd: " + cmd + ": " + stdout)
        else:
            nm_error("nm_host_cmd: " + cmd + ": " + stderr)
    else:
        return stdout, stderr


def nm_host_cmd_bg(cmd):
    # debug
    if env_debug == 'true':
        nm_debug("Host bg cmd: " + cmd)
    else:
        cmd_bin = cmd.split(" ")[0]
        nm_debug("Host bg cmd: " + cmd_bin)

    # run process in background, without waiting for it to finish
    os.popen(cmd)


def nm_keycombo(combo, delay=120):
    # sometimes typing is too fast for a remote machine, set a minimum delay
    if isinstance(delay, int) and delay < 5:
        delay = 5

    if delay == "":
        delay = 120

    nm_log("Keycombo: " + combo)
    if env_host == 'remote':
        cmd_pre = 'autotype --delay ' + str(delay)
        if combo.startswith("-"):
            arg_term = " --"
        else:
            arg_term = ""
        combo_formatted = combo.replace("'", "'\\''")
        cmd_suf = arg_term + ' --mod \'' + combo_formatted + '\''

        autotype_result, autotype_err = nm_host_cmd(cmd_pre + cmd_suf)
        if autotype_err:
            nm_error("nm_keycombo: autotype: " + autotype_err)


def nm_match_exact(image_path):
    return Pattern(image_path).exact()


def nm_match_similar(image_path):
    return Pattern(image_path).similar(0.5)


def nm_match_very_similar(image_path):
    return Pattern(image_path).similar(0.8)


def nm_memory_get(var_name):
    return nm_db_get(nmv_file_memory, var_name)


def nm_memory_set(var_name, var_value):
    nm_db_set(nmv_file_memory, var_name, var_value)


def nm_sleep(time):
    wait(time)


def nm_speak(text):
    nm_log("Speak: " + str(text))
    if env_host == 'remote':
        nm_host_cmd('autovoice "' + text + '."')
    else:
        nm_debug("nm_speak not implemented on 'local' machines")


def nm_speak_bg(text):
    nm_log("Speak: " + str(text))
    if env_host == 'remote':
        nm_host_cmd_bg('autovoice "' + text + '."')
    else:
        nm_debug("nm_speak_bg not implemented on 'local' machines")


def nm_think(text):
    nm_log("Think: " + text)
    if env_thought == 'verbal':
        nm_speak_bg("Thinking. " + text)
    elif env_thought == 'verbal_wait':
        nm_speak("Thinking. " + text)


def nm_type(text=None, delay=120, file=None):
    # sometimes typing is too fast for a remote machine, set a minimum delay
    if isinstance(delay, int) and delay < 5:
        delay = 5

    if delay == "":
        delay = 120

    if env_host == 'remote':
        cmd_pre = 'autotype --delay ' + str(delay)
        if file:
            nm_log("Type from file: " + file)
            bot_dir = getBundlePath()
            file_bot_dir = bot_dir + "/" + file
            file_location = ""
            if os.path.exists(file):
                file_location = file
            elif os.path.exists(file_bot_dir):
                file_location = file_bot_dir
            else:
                nm_error("nm_type: File not found: " + file)
            cmd_suf = ' <"' + file_location + '"'

        else:
            nm_log("Type: " + text)
            if text.startswith("-"):
                arg_term = " --"
            else:
                arg_term = ""
            text_formatted = text.replace("'", "'\\''")
            cmd_suf = arg_term + ' \'' + text_formatted + '\''

        autotype_result, autotype_err = nm_host_cmd(cmd_pre + cmd_suf)
        if autotype_err:
            nm_error("nm_type: autotype: " + autotype_err)

    # sikuli native
    else:
        Settings.TypeDelay = int(delay / 1000)
        type(text)


# INIT AND GLOBALS ###########################################################

nm_log("Loading neuman library")

env_debug = nm_set_env(
    'NEUMAN_DEBUG',
    ['false', 'true']
)

env_host = nm_set_env(
    'NEUMAN_HOST',
    ['remote', 'local']
)

env_instance = nm_set_env(
    'NEUMAN_INSTANCE',
    ['default'],
    True
)

env_thought = nm_set_env(
    'NEUMAN_THOUGHT',
    ['silent', 'verbal', 'verbal_wait']
)

# use the prefix 'nmv' for all variables that are global to that instance

nmv_path_instance = '/dev/shm/neuman/' + env_instance + '/'
nmv_file_memory = nmv_path_instance + "memory"

nm_create_config()

# DEMO MAIN ##################################################################

if __name__ == '__main__':
    nm_think("Hello, I am Neuman")
