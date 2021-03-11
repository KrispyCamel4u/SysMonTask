#!/bin/bash

files_dir=$(find /usr/local/ -name "sysmontask*")
for file in $files_dir
do
	sudo rm -rf $file
done
sudo rm -rf /usr/share/applications/SysMonTask.desktop
sudo rm -rf /usr/share/sysmontask
sudo rm -rf /usr/share/doc/sysmontask
echo "Done"