#!/bin/bash
echo $1/../../usr
if [ "$#" -ne 0 ]; then
	cp $1/applications/SysMonTask.desktop /usr/share/applications/
	cp -r $1/doc/sysmontask /usr/share/doc
	cp -r $1/sysmontask /usr/share
fi

