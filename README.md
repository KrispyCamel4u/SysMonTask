# SysMonTask
Linux system monitor with the compactness and usefulness of windows task manager to allow higher control and moniterisation.

### v1.0.0 
- Performance moniterisation graphs
- Devices supported:
  * CPU
  * Memory
  * Disks
  * Network adapters
  * only single Nvidia GPU

To use:
  1. Download latest Release
  2. Install SysMonTask[version].deb
  3. Hurray, You're goot to go in understanding capabilities of your system:)
 
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
*SysMonTask will work without zenity also but some information dependent of root privilege might be incorrect.*

Running directly from terminal requires you to setup PATH to 
```
/opt/SysMonTask/
```
which is default installation directory.
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


[old]
### Prelease Beta Version-0.5
*yay the prerelease version with the performance tab is released. Download it from releases.*

To use it:
  1. Download .deb package
  2. Install on your system
  3. Run "sudo taskmanager" on terminal
