#!/usr/bin/bash
files_dir=$(find /usr/local/ -name "sysmontask*")
for file in $files_dir
do
	sudo rm -rf $file
done
sudo rm -rf /usr/applicatons/SysMonTask.desktop
sudo rm -rf /usr/share/sysmontask
echo "Done"