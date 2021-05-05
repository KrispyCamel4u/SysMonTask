#!/bin/bash

files_dir=$(find /usr/local/ -name "sysmontask*")
for file in $files_dir
do
	sudo rm -rf "$file"
done
sudo rm -rf /usr/share/applications/SysMonTask.desktop
sudo rm -rf /usr/share/sysmontask
sudo rm -rf /usr/share/doc/sysmontask
sudo rm /usr/share/glib-2.0/schemas/com.github.camelneeraj.sysmontask.gschema.xml
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
echo "Done"