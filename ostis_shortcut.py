#!/usr/bin/env python3
import subprocess
import sys

title = 'run_ostis'

script_name = title +'.sh'
desktop_entry_name = title + '.desktop'
keyboard_shortcut = '<Control><Alt>O'

def allow_execution(file):
	subprocess.call(['chmod', '+x', file])


def create_script(ostis_folder):
	script_path = ostis_folder + '/scripts/'

	file = open(script_path + script_name, "wt")

	file.write('#!/bin/bash' + '\n')
	file.write('cd ' + script_path + '\n')
	file.write('gnome-terminal --tab -e "./restart_sctp.sh" --tab -e "./run_scweb.sh"')

	file.close()

	allow_execution(script_path + script_name)

	print("Bash script created...")


def create_shortcut():
	dconf_schema = "org.gnome.settings-daemon.plugins.media-keys"
	dconf_key = "custom-keybindings"
	dconf_subkey = dconf_schema + "." + dconf_key[:-1] + ":"
	dconf_item = "/" + dconf_subkey.replace(".", "/").replace(":", "/")

	# get the current list of custom shortcuts
	shortcuts = subprocess.check_output(["gsettings", "get", dconf_schema, dconf_key]).decode("utf-8")
	shortcut_list = eval(shortcuts)

	# find first shortuct number, that doesn't exist in current list
	n = 0
	while True:
		new_shortcut = dconf_item + "custom" + str(n) + "/"
		if new_shortcut in shortcut_list:
			n += 1
		else:
			break

	shortcut_list.append(new_shortcut)

	subprocess.call(["gsettings", "set", dconf_schema, dconf_key, str(shortcut_list)])
	subprocess.call(["gsettings", "set", dconf_subkey + new_shortcut, "name", "ostis"])
	subprocess.call(["gsettings", "set", dconf_subkey + new_shortcut, "command", "gtk-launch " + title])
	subprocess.call(["gsettings", "set", dconf_subkey + new_shortcut, "binding", keyboard_shortcut])
	
	print("Keyboard shortcut created...")


def create_desktop_entry(ostis_folder):
	username = subprocess.check_output(["whoami"]).decode('utf-8').rstrip()
	
	desktop_entry_path = '/home/' + username + '/.local/share/applications/'
	script_full_path = ostis_folder + '/scripts/' + script_name
	
	file = open(desktop_entry_path + desktop_entry_name, 'wt')

	file.write('[Desktop Entry]' + '\n')
	file.write('Type=Application' + '\n')
	file.write('Terminal=true' + '\n')
	file.write('Name=ostis' + '\n')
	file.write('Exec=' + script_full_path + '\n')
	
	file.close()
	
	allow_execution(script_full_path)
	
	print("Desktop entry created...")


if len(sys.argv) < 2:
	print('Usage: python3 ' + sys.argv[0] + ' path_to_ostis_directory\n')
	sys.exit()

create_script(sys.argv[1])
create_desktop_entry(sys.argv[1])
create_shortcut()
