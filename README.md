# SysMonTask  <img align="right" width="100" height="100" src="https://user-images.githubusercontent.com/48773008/108200308-4d170080-7144-11eb-8354-0c528c7b1ac2.png">
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<p align="left">
<a href="https://github.com/KrispyCamel4u/SysMonTask/commit-activity">
    <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
</a>

<a href="https://github.com/KrispyCamel4u/SysMonTask/tags/">
    <img src="https://img.shields.io/github/v/tag/KrispyCamel4u/SysMonTask.svg">
</a>
<a href="https://github.com/KrispyCamel4u/SysMonTask/master/LICENSE">
    <img src="https://img.shields.io/github/license/KrispyCamel4u/SysMonTask.svg">
</a>

<a href="https://github.com/KrispyCamel4u">
    <img src="https://img.shields.io/badge/Need%20help%3F-Ask-27B89C">
</a>
</p>

Linux system monitor with the compactness and usefulness of Windows Task Manager to allow higher control and monitoring.

## Installation
### Ubuntu and its family members **(only for: 18.04, 20.04 and 20.10 and equivalent)**, run: 

***[Need help for packaging for other distros]***

*Note: The process tab works well only for the systems using the Gnome,cinnamon and xfce desktop environment as of now (support for Mate,KDE will be added soon)*
```
$ sudo add-apt-repository ppa:camel-neeraj/sysmontask
  ....
$ sudo apt install sysmontask
  ....
// Install psutil if Ubuntu<=20.04, other-wise skip this step(more info given below) : 
$ sudo pip3 install -U psutil
  ....
$ sysmontask   // optional to run via terminal but recommended for the first time 
```
Alternatively, if you don't want to add the PPA (Personal Package Archives) then download the binaries from releases, and install by double clicking on it.

***Note: Some information such as Memory static details(slots, Frequency) and Disk IO(disk usage per process) for the other user's processes(including root) requires root access, hence to run with root access:***
```
$ sudo sysmontask
  ....
```
**For Ubuntu<=20.04(for others it will be installed automatically), psutil will not be install automatically with sysmontask(python3-psutil doesn't meet the version requirements), hence install with:**

```
$ pip3 install psutil          // if you're not planning to use it with root access
  ....
  OR
$ sudo pip3 install -U psutil  // needed to run sysmontask with root access, hence recommended
  ....
```
---

### Arch based destros:
```
$ git clone https://aur.archlinux.org/sysmontask.git
  ....
$ cd sysmontask
$ makepkg -si
  ....
$ sysmontask
  ....
```
OR

Install using pamac(gui for software add/remove), first enable the AUR(arch user repository) in preferences, then search sysmontask, install and enjoy.

---

### Installing from source(for other destros whose package is yet to be made)
Install the dependencies required, mentioned in the [requirments.md](https://github.com/KrispyCamel4u/SysMonTask/blob/master/requirements.md). In case of issue related to PyGoject or pycairo OR to get the command for the specific package manager, follow the link given in requirements.md . 

While installing from source, pip automatically installs some of the packages(which can be installed using pip) required others need to be installed using package manager.

After installing dependencies:
```
$ git clone https://github.com/KrispyCamel4u/SysMonTask.git
  ....
$ cd SysMonTask
$ sudo python3 setup.py install
  ....
$ sysmontask
  ....
```
It will install it in "/usr/local/lib/python<version>/dist-packages/".
To uninstall it run the uninstall.sh script in the SysMonTask cloned directory, with:
```
$ ./uninstall.sh
  Done
```

---

**Note: For Nvidia GPUs, nvidia-smi needs to be installed. Check if nvidia-smi is installed by running:**
```
$ nvidia-smi
  ...
```
If not then install it for your system (generally it is automatically installed with Nvidia proprietary drivers).

Then start application from the menu or by the command "sysmontask" (recommended only in case of error/crashed) on terminal.

Hurray, you're good to go in understanding capabilities of your system:)


## What's New: [![Generic badge](https://img.shields.io/badge/What's_New-History-red.svg)](https://github.com/KrispyCamel4u/SysMonTask/blob/master/HISTORY.md) [![Generic badge](https://img.shields.io/badge/Read_More-Docs-blueviolet.svg)](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md)

### v1.1.1-beta-b
#### [Bug Fix + Enhancements]
- [[#6](https://github.com/KrispyCamel4u/SysMonTask/issues/6)] Possibility to run as non-root
- [[#12](https://github.com/KrispyCamel4u/SysMonTask/issues/12)] gi.repository.Gtk' object has no attribute 'Container'
- [[#13](https://github.com/KrispyCamel4u/SysMonTask/issues/13) [#23](https://github.com/KrispyCamel4u/SysMonTask/issues/23)] ValueError: invalid literal for int() with base 10: 'N/', Does not work en PopOs 20.10
- [[#14](https://github.com/KrispyCamel4u/SysMonTask/pull/14)] Python <=3.7 compaitiable for process UI 
- [[#15]()] Processes missing from process tab( added filtered processes support for cinnamon, xfce)
- [[#16](https://github.com/KrispyCamel4u/SysMonTask/issues/16)] psutils version fallbac (removed psutil dependency for ubuntu<=20.04, install seperately)
- [[#20](https://github.com/KrispyCamel4u/SysMonTask/issues/20)] Missing temperature unit in the performance tab
- [[#22](https://github.com/KrispyCamel4u/SysMonTask/issues/22)] Temperature of AMD CPU displays as NA
- [[#26](https://github.com/KrispyCamel4u/SysMonTask/issues/26)] Wrong arrows direction on Processes tabs(sorting column header)
- [[#31](https://github.com/KrispyCamel4u/SysMonTask/issues/31)] Not working on Linux Lite (Ubuntu 20.04.2) (gir1.2-wnck-3.0 dependancy added)
- Use of zenity removed
 
**Previous highlight:**
- Processes filtering for user for fast look-ups. ([Read More](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md))
- **rCPU, rMemory** (recursive-CPU,recursive-Memery) columns. ([Read More](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md)).


**To set theme, Run:**

By Default sysmontask will use the system-wide setting for themes. If you use any of dark theme(dark mode), that dark theme(dark mode) will be applied to sysmontask. If you use any of light theme(default/light mode), that light theme(default/light mode) will be used by sysmontask. 

To Force apply a particular available theme(light or dark) regardless of system-wide theme, use the below commands:
```
$ sudo sysmontask.set_light
  0 : Raleigh
  1 : HighContrast
  2 : Pop
  3 : Default
  4 : Adwaita
  5 : Emacs
  Index for Corresponding Theme that you want to apply?:2
  Setting of Light Theme Done:)
$ sudo sysmontask.set_dark
  0 : Pop-dark
  1 : Adwaita-dark
  Index for Corresponding Theme that you want to apply?:0
  Setting of Dark Theme Done:)
  ```
This setting will be permanent. If you want to revert back to system-wide theme settings for sysmontask, run:
```
$ sudo sysmontask.set_default
  Setting done:)
```

#### Highlights
![Screenshot from 2021-02-17 17-54-27](https://user-images.githubusercontent.com/48773008/108204170-79814b80-7149-11eb-8b1f-843a1efa8d42.png)

![Screenshot from 2021-02-21 22-06-32](https://user-images.githubusercontent.com/48773008/108631693-1bc66980-7491-11eb-8b1e-59df9622bd32.png)

![Screenshot from 2021-01-24 11-00-18](https://user-images.githubusercontent.com/48773008/105622210-7ab6a580-5e35-11eb-9a43-8f09c0efbdb2.png)

![Screenshot from 2021-02-17 18-09-43](https://user-images.githubusercontent.com/48773008/108212228-a33f7000-7153-11eb-9d3d-2c56d411efc7.png)



