# SysMonTask  <img align="right" width="100" height="100" src="https://user-images.githubusercontent.com/48773008/108200308-4d170080-7144-11eb-8354-0c528c7b1ac2.png">
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<p align="left">
<a href="https://github.com/KrispyCamel4u/SysMonTask/commit-activity">
    <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
</a>
 <a href="https://github.com/KrispyCamel4u/SysMonTask/tags/">
    <img src="https://img.shields.io/github/v/tag/KrispyCamel4u/SysMonTask.svg?sort=semver">
</a>
<a href="https://github.com/KrispyCamel4u/SysMonTask/master/LICENSE">
    <img src="https://img.shields.io/github/license/KrispyCamel4u/SysMonTask.svg">
</a>

<a href="https://github.com/KrispyCamel4u">
    <img src="https://img.shields.io/badge/Need%20help%3F-Ask-27B89C">
</a>
</p>

Linux system monitor with the compactness and usefulness of windows task manager to allow higher control and monitoring.

## Installation
To install the binary for ubuntu and its family members
```
$ sudo add-apt-repository ppa:camel-neeraj/sysmontask
  ....
$ sudo apt install sysmontask
  ....
```
Then start application from menu.

Hurray, You're goot to go in understanding capabilities of your system:)

## What's New: [![Generic badge](https://img.shields.io/badge/What's_New-History-red.svg)](https://github.com/KrispyCamel4u/SysMonTask/blob/master/HISTORY.md) [![Generic badge](https://img.shields.io/badge/Read_More-Docs-blueviolet.svg)](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md)

### v1.1.0
- User Processess Tab
    * Processes filtering for user for fast look-ups. ([Read More](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md))
    * rCPU, rMemory (recursive-CPU,recursive-Memery) columns. ([Read More](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md)).
    * Support for aggregate values on coloumn headers.
    * Icon support, Available Killer. 
- Mounted Disk List  


#### Highlights
![Screenshot from 2021-02-17 17-54-27](https://user-images.githubusercontent.com/48773008/108204170-79814b80-7149-11eb-8b1f-843a1efa8d42.png)

![Screenshot from 2021-01-24 11-00-18](https://user-images.githubusercontent.com/48773008/105622210-7ab6a580-5e35-11eb-9a43-8f09c0efbdb2.png)

![Screenshot from 2021-02-17 18-09-43](https://user-images.githubusercontent.com/48773008/108212228-a33f7000-7153-11eb-9d3d-2c56d411efc7.png)

### v1.0.0 
- Performance monitoring graphs
- Devices supported:
  * CPU
  * Memory
  * Disks
  * Network adapters
  * only single Nvidia GPU

### If you are using dark mode and didn't like the look then follow below specified steps for dark mode disabled package:
*Note: Below mentioned facts and information is only applicable to this method of installation only*
  1. Uninstall if you've installed via terminal
  ```
  $ sudo apt remove sysmontask
  ```
  2. Download latest package from Releases
  3. Install SysMonTask[version].deb
 
- *Require Ubuntu 20.04 or higher or equivalent*
- Tested on Ubuntu 20.04 LTS, popOS 20.10 

Running directly from terminal requires you to setup PATH to 
```
/opt/sysmontask
```
which is the default installation directory.
After setting PATH, run:
```
$ sysmontask
```
from any location.

#### Bug Reporting and Debugging information
In case of bugs/crashes/incompatibilities please drop a mail to
[neerajkumar.nitt@gmail.com](url) or report in GitHub Issues.

For getting the details of error, run SysMonTask from terminal.
```
$ /opt/SysMonTask/sysmontask
```


