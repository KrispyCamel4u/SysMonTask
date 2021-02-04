# SysMonTask
Linux system monitor with the compactness and usefulness of windows task manager to allow higher control and monitoring.

### v1.0.0 
- Performance monitoring graphs
- Devices supported:
  * CPU
  * Memory
  * Disks
  * Network adapters
  * only single Nvidia GPU

## Installation
To install the binary for ubuntu and its family members
```
$ sudo add-apt-repository ppa:camel-neeraj/sysmontask
  ....
$ sudo apt install sysmontask
  ....
$ pip3 install pygi-composite-templates
```
Hurray, You're goot to go in understanding capabilities of your system:)

Then start application from menu.

#### Highlights
![Screenshot from 2021-01-24 11-00-18](https://user-images.githubusercontent.com/48773008/105622210-7ab6a580-5e35-11eb-9a43-8f09c0efbdb2.png)


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

It is recommended to have zenity installed(for privilege uplifting prompt), to check run:
```
$ zenity --version
3.32.0
```
If installed, version will be shown, otherwise install with:
```
$ sudo apt install zenity
```
*SysMonTask will work without zenity also but some information dependent on root privilege might be incorrect.*

Running directly from terminal requires you to setup PATH to 
```
/opt/SysMonTask/
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


