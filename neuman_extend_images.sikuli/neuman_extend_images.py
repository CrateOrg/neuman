# info: Extended Neuman Bot Image Library
# Part of the Extended Neuman Library.
# Contains static image data for the Neuman Bot.

import org.sikuli.script.SikulixForJython
from sikuli import *
from neuman import *

# Each line in each list represents a Desktop Environment.
# Append new ones.

# All global image variables start with 'nmvi_'

nmv_os_names = [
    'Windows XP',
    'Windows 7',
    'Kali Linux',
    'Debian 12 with XFCE and Servermonkeys Theme'
]

nmvi_os_indicators = [
    nm_match_exact("start_winxp.png"),
    nm_match_exact("start_win7.png"),
    nm_match_exact("start_kali-linux.png"),
    nm_match_exact("start_debian12_xfce_servermonkey.png")
]

nmvi_os_indicators_b = [
    nm_match_exact("desktop_icon_mycomputer_winxp.png"),
    nm_match_exact("button_show_desktop_win7.png"),
    nm_match_exact("wallpaper_cutout_kali-linux.png"),
    nm_match_exact("wallpaper_cutout_debian12_default.png")
]

nmvi_os_indicators_c = [
    0,
    nm_match_similar("icon_recycle_bin_win7.png"),
    0,
    0
]

nmvi_buttons_close = [
    nm_match_exact("buttons_close_winxp.png"),
    nm_match_exact("buttons_close_win7.png"),
    nm_match_exact("buttons_close_kali-linux.png"),
    nm_match_exact("buttons_close_debian12_xfce_servermonkey.png")
]

nmvi_runas_indicators = [
    nm_match_exact("run_indicator_winxp.png"),
    nm_match_exact("run_indicator_win7.png"),
    nm_match_exact("run_indicator_kali-linux.png"),
    nm_match_exact("run_indicator_debian12_xfce_servermonkey.png")
]

# alternative close buttons, not app specific,
# mostly found in Linux when mixing GNOME, KDE and other environments
nmvi_buttons_close_b = [
    0,
    0,
    nm_match_exact("buttons_close_b_kali-linux.png"),
    0
]

nmvi_menu_bar = [
    nm_match_exact("menu_bar_winxp.png"),
    nm_match_exact("menu_bar_win7.png"),
    nm_match_exact("menu_bar_kali-linux.png"),
    nm_match_exact("menu_bar_debian12_xfce_servermonkey.png")
]

nmvi_menu_bar_firefox = [
    0,
    0,
    nm_match_exact("menu_bar_firefox_kali-linux.png"),
    nm_match_exact("menu_bar_firefox_debian12_xfce_servermonkey.png")
]

nmvi_term_done = [
    0,
    0,
    0,
    nm_match_exact("term_done_debian12_xfce_servermonkey.png")
]

nmvi_term_done_sudo = [
    0,
    0,
    0,
    nm_match_exact("term_done_sudo_debian12_xfce_servermonkey.png")
]

nmvi_icon_iexplorer = [
    "icon_iexplorer_winxp.png",
    "icon_iexplorer_win7.png",
    0,
    0
]

nmvi_icon_taskbar_iexplorer = [
    "icon_taskbar_iexplorer_winxp.png",
    "icon_taskbar_iexplorer_win7.png",
    0,
    0
]

nmvi_icon_firefox = [
    0,
    0,
    0,
    0
]

nmvi_icon_edge = [
    0,
    0,
    0,
    0
]

nmvi_icon_chromium = [
    0,
    0,
    0,
    0
]

nmvi_icon_chrome = [
    0,
    0,
    0,
    0
]

nmvi_app_mspaint_indicators = [
    nm_match_exact("app_mspaint_indicator_winxp.png"),
    nm_match_exact("app_mspaint_indicator_win7.png"),
    0,
    0
]
