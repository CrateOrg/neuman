neuman(1) -- Bot framework to emulate and automate a computer user
=============================================

## SYNOPSIS

`neuman` _bot_name_ [ **state** ]

## DESCRIPTION

This is a BETA version. Things that don't work are marked as BETA.

Neuman is a bot program and framework based on SikuliX and additional Python
libraries. Automate repetitive tasks on a computer, in a similar way to a
human.

Unlike pure SikuliX, it does not need to be run on the same machine. It can be
run on a remote machine and interact with the target application over a remote
desktop connection like rdesktop, VNC or virt-viewer.

It provides debugging information, error handling, and process state
monitoring.

## OPTIONS

- `-h, --help`
  Display this manual page.

- `state`  
  Show the current state of the bot, including logs, running status, and system
  information.

## ENVIRONMENT

- `NEUMAN_DEBUG` ( default: false | true )  
  If set to 'true', enables more debug messages in the log and shell output.

- `NEUMAN_INSTANCE` ( default: default | <NAME> )  
  Defines the bot instance. Each bot, no matter the bot name, can be given a
  unique instance name. This is used to separate multiple bots running on the
  same machine and to make a bot 'remember' it's state after a restart, crash
  or error of the bot itself. Can be used to make a bot continue where it left
  off. See the `nm_memory_get` and `nm_memory_set` functions in the neuman
  library.

- `NEUMAN_THOUGHT` ( default: silent | verbal | verbal_wait )  
  Controls the thought mode of the bot. Can be set to 'silent', 'verbal', or
  'verbal_wait'. 'silent' will not speak any thoughts, 'verbal' will speak
  thoughts in background, and 'verbal_wait' will speak thoughts and wait until
  the speech is finished before continuing.

- `NEUMAN_HOST` ( default: local | remote )  
  BETA: Only 'local' is supported at the moment.  
  Defines the host type. Can be set to 'local' or 'remote'. 'local' will run
  the bot on the local machine for the local machine, 'remote' will run the bot
  localy for a remote machine, and interact with the target application over a
  remote desktop connection. The difference is in the way the bot interacts
  with the target application. 'local' uses SikuliX to interact with the
  applications, such as windows title recognition. 'remote' uses advanced image
  recognition and keyboard emulation to interact with the applications.

## FILES

**Logs: ~/.local/share/neuman/logs/**  
Filename format is: <bot_name>_$NEUMAN_INSTANCE.log  
Will be overwritten after same bot restart.

**Storage for instances: /dev/shm/neuman/**  
The INSTANCE_DIR folder Will be reset after reboot!

**Keyboard layout: /etc/default/keyboard**  
Determine source hosts keyboard layout.  
BETA: Some layouts are not supported. See autotype(1) for more information.

## EXAMPLES

Monitor the state of a running bot:

    $ neuman mybot state

Open another terminal and start the bot:

    $ neuman mybot

Now switch over to a fullscreen remote desktop viewer and watch the bot work.

Another example, set another instance name and thought mode:

    $ NEUMAN_INSTANCE=another NEUMAN_THOUGHT=verbal_wait neuman mybot

## KNOWN BUGS

A bug appears under virt-manager or virt-viewer while using the neuman
function `nm_type` or `nm_keycombo`.  
These functions use the package `autotype`, which uses ydotool or xdotool to
emulate keyboard input.  
While using virt-manager or virt-viewer 'xdotool key' fails when using ALT_R
modifier. It seems virt-viewer ignores, or intercepst ALT_R, and then ignores
it. Use ydotool to get around this problem. This is automatically solved by the
package `autotype`.

## DEPENDENCIES

- `autovoice` (for speech output)
- `autotype` (will also install ydotool and/or xdotool)
- `SikuliX` (install to /opt/SikuliX*.jar , tested with SikuliX-2.0.5
- `java runtime` (at least jre-headless, tested with JRE 17)
- `notify-send` (optional, for start and stop popup-notifications)

## LIBRARIES OVERVIEW AND USAGE

neuman uses SikuilX and additional Python libraries. SikiuliX is a Java and
Jython based automation library that uses image recognition to interact with
the screen. The additional libraries are written in Python and provide
additional functionality to the bot.

System libraries should be installed to:  
**/usr/lib/sikulix/dist-packages/**

User libraries should be installed to:  
**~/.Sikulix/Lib/site-packages/**

On neuman startup, all system libraries will automatically be symlinked to the
current users library directory. This is required for SikuliX to find the
libraries.

The library structure for each library and bot script is as follows:

- Create a base directory for the bot, e.g. 'mybot' that ends in .sikuli
- Example for a bot: ~/My_Bots/mybot.sikuli/
- Example for a library: ~/.Sikulix/Lib/site-packages/mybot.sikuli/
- In each directory, create a file with the same name but ending in .py
- Example for a bot: ~/My_Bots/mybot.sikuli/mybot.py
- As a minimum, the file should contain the following lines:

      import org.sikuli.script.SikulixForJython
      from sikuli import *

To import additional libraries, the following lines should be added.  
Here is an example for the import of the base 'neuman' library:

    import org.sikuli.script.SikulixForJython
    from sikuli import *
    from neuman import *

## INCLUDED LIBRARIES OVERVIEW

- `neuman` : Neuman Bot Library.  
  Basic bot automation library.  
  It does not include any images or specific file dependencies, ensuring
  it can run without additional files.  
  The library provides logging and error handling, environment variable
  management, automation features such as screen detection, typing, speech and
  more.

- `neuman_extend` : Extended Neuman Bot Library.  
  Additional functions related to visual detection and GUI interaction.

- `neuman_extend_images` : Extended Neuman Bot Library Images.  
  Part of the Extended Neuman Library. Contains static image data.

## INCLUDED LIBRARY REFERENCE: neuman

### Global Variables:

**env_debug**: Environment variable value for debugging  
**env_host**: Environment variable value for host type  
**env_instance**: Environment variable value for instance name  
**env_thought**: Environment variable value for thought mode  
**nmv_path_instance**: Path to instance memory storage  
**nmv_file_memory**: Path to memory file storage

For 'env_' variables see the ENVIRONMENT section.

### Functions:

**nm_error(text)**  
Logs an error message and exits the script.

**nm_log(text)**  
Logs a message as part of normal bot behavior.

**nm_debug(text)**  
Logs debug information when `env_debug` is `true`.

**nm_debug_verbose(text)**  
Logs debug information and prints it to the console if `env_debug` is `true`.

**nm_set_env(var_name, valid_values, optional=False)**  
Sets environment variables based on allowed values.

**nm_create_config()**  
Initializes bot configuration, resets memory if instance is `default`.

**nm_click(image)**  
Clicks on the specified image.

**nm_db_get(flat_file_db, var_name)**  
Retrieves a stored variable from a flat file database.

**nm_db_set(flat_file_db, var_name, var_value)**  
Stores or updates a variable in a flat file database.

**nm_detect(img_list_indicators, list_of_names, certain=True)**  
Detects images from a list and returns a matched name.  
If `certain`, the bot claims to 'know'. Opposite is 'believe'.

**nm_fatique_add(integer)**  
Increases fatigue value in memory. Use to simulate human fatigue/tiredness.

**nm_fatique_get()**  
Retrieves the current fatigue value.

**nm_fatique_remove(integer)**  
Decreases fatigue value in memory.

**nm_fatique_set(integer)**  
Sets the fatigue value in memory.

**nm_host_cmd(cmd)**  
Executes a command on the host and returns the output.

**nm_host_cmd_bg(cmd)**  
Executes a command in the background without waiting.

**nm_keycombo(combo, delay=120)**  
Simulates key combinations with an optional delay.  
Can also be a single key press.  
See autotype(1) for more information.

**nm_match_exact(image_path)**  
Returns an exact pattern match for an image.

**nm_match_similar(image_path)**  
Returns a pattern match with 50% similarity.

**nm_match_very_similar(image_path)**  
Returns a pattern match with 80% similarity.

**nm_memory_get(var_name)**  
Retrieves a stored variable from memory.

**nm_memory_set(var_name, var_value)**  
Stores a variable in memory.

**nm_sleep(time)**  
Pauses execution for a specified duration in seconds. Can be an integer or
float.

**nm_speak(text)**  
Logs and speaks the provided text.  
Waits for the speech to finish before continuing.  
See autovoice(1) for more information.

**nm_speak_bg(text)**  
Logs and speaks the provided text in the background.

**nm_think(text)**  
Logs and optionally speaks thoughts based on `env_thought`.  
Use this to make the bot 'think' about what it is doing. Good for logging and
to be analyzed later.

**nm_type(text=None, delay=120, file=None)**  
Simulates typing with an optional delay or from a file.  
Choose between a text string or a file path. Not both.

## INCLUDED LIBRARY REFERENCE: neuman extend

This also includes the 'neuman extend images' library.

To fully understand the functions in this library, it is recommended to read
the source code. The functions and image variables are documented in the code.

### Functions:

**nm_detect_os()**  
Detects the current operating system and stores it in memory.  
Returns the detected OS as a string.

**nm_os_to_image(os_name, list_of_images)**  
Converts an OS name to its corresponding image from a list.  
Returns the matched image.

**nm_gui_simple_run(command)**  
Opens a terminal or run dialog and runs a command as the current user.  
Closes the terminal immediately after execution.  
Requires nm_detect_os() to be run first.

**nm_gui_run(command="", preserve=False, become=False, password="")**  
Opens a terminal or run dialog.  
Runs a command with optional superuser privileges.  
Can keep the terminal open if preserve is True.  
If become is True, requires a password for superuser access.

**nm_gui_run_done(close=False, timeout=120)**  
Waits for a terminal to finish executing a command.  
timeout prevents infinite waiting (default 120 seconds).  
Can close the terminal automatically if close=True.

## COPYRIGHT

See license file

## SEE ALSO

autotype(1), autovoice(1), java(1)

http://www.sikulix.com/
