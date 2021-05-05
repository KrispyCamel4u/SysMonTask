### v1.3.9
#### [Bug Fix]
- [[#22](https://github.com/KrispyCamel4u/SysMonTask/issues/22)] Temperature of AMD CPU displays as NA ["zenpower" name added]
- [[#47](https://github.com/KrispyCamel4u/SysMonTask/issues/47)] unknown signal name: clicked (GPU error)

### V1.3.7
#### [Enhancements]
- Filter Dialog [Read More](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md)
- Process Log Record and Log Plot [Read More](https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md)
#### [Bug Fix]
- [[#15]((https://github.com/KrispyCamel4u/SysMonTask/issues/15))] Processes missing from process tab [or all desktop environments, fixed]
- [[#22](https://github.com/KrispyCamel4u/SysMonTask/issues/22)] Temperature of AMD CPU displays as NA [fixed]
- [[#27](https://github.com/KrispyCamel4u/SysMonTask/issues/27)] How to search or filter for processes
- [[#28](https://github.com/KrispyCamel4u/SysMonTask/issues/28)] [[#45](https://github.com/KrispyCamel4u/SysMonTask/issues/45)] [[#46](https://github.com/KrispyCamel4u/SysMonTask/issues/46)] Doesnt Seem To Work With Gruvbox-dark-gtk, Not Working on Arch Linux, Sudo Error! (AttributeError: 'NoneType' object has no attribute 'lower')
- [[#34](https://github.com/KrispyCamel4u/SysMonTask/issues/34)] Invalid version (double separator '-'): 1.1.1-beta-b: python3dist(sysmontask) = 1.1.1-beta-b (Follow Semantic Versioning)
- [[#36](https://github.com/KrispyCamel4u/SysMonTask/issues/36)] Please exclude zram slots from disks
- [[#38](https://github.com/KrispyCamel4u/SysMonTask/issues/38)] Can't click on the tabs in the performance tabs.


### v1.1.1-beta-b
#### [Bug Fix + Enhancements]
- [[#6](https://github.com/KrispyCamel4u/SysMonTask/issues/6)] Possibility to run as non-root( removed need for package zenity)
- [[#12](https://github.com/KrispyCamel4u/SysMonTask/issues/12)] gi.repository.Gtk' object has no attribute 'Container'
- [[#13](https://github.com/KrispyCamel4u/SysMonTask/issues/13) [#23](https://github.com/KrispyCamel4u/SysMonTask/issues/23)] ValueError: invalid literal for int() with base 10: 'N/', Does not work en PopOs 20.10
- [[#14](https://github.com/KrispyCamel4u/SysMonTask/pull/14)] Python <=3.7 compaitiable for process UI
- [[#15]()] Processes missing from process tab [added filtered processes support for cinnamon, xfce]
- [[#16](https://github.com/KrispyCamel4u/SysMonTask/issues/16)] psutils version fallbac (removed psutil dependency for ubuntu<=20.04, install seperately)
- [[#20](https://github.com/KrispyCamel4u/SysMonTask/issues/20)] Missing temperature unit in the performance tab
- [[#22](https://github.com/KrispyCamel4u/SysMonTask/issues/22)] Temperature of AMD CPU displays as NA [didn't get fixed]
- [[#26](https://github.com/KrispyCamel4u/SysMonTask/issues/26)] Wrong arrows direction on Processes tabs(sorting column header)
- [[#31](https://github.com/KrispyCamel4u/SysMonTask/issues/31)] Not working on Linux Lite (Ubuntu 20.04.2) (gir1.2-wnck-3.0 dependancy added)
- Removed zenity.

### v1.1.1-beta-a
#### [Bug Fix]
  * Added support for multiple users processes.
  * About logo icon fixed.
  * Back to zenity for privilege uplifting.
  * Removed auto installing of psutil.
  * [[#4](https://github.com/KrispyCamel4u/SysMonTask/pull/4)] hardcode path removed when running from source

### v1.1.1-beta
#### Enhancements
- Logical and Overall CPU Utilisation.
- Option to change graph movement(Newer on Left/Newer on Right).
- Icons on Menu.
- Mac Address on Network tab.
- Resident and Shared Memory Columns on performance tab.
- Show/Hide process tab columns(click on column headers).

**[Bug Fix]**
- optimised code.
- Refresh not working after Adding a process tab.
- Update speed not working after Adding a process tab.
- Graph resizing on full screen.
- [[Bug #2](https://github.com/KrispyCamel4u/SysMonTask/issues/2)] Application crashes start after adding process tab.

### v1.1.0
#### Enhancements
- user-specific process tab
  * Process filtering like Windows Task Manager(parent and child)
  * Icon support for processes
  * Aggregate readings on process tab column headers
  * killer for killing process
- Mounted Disk statistics (on disk performance tab)
- use of pkexec for priviledge uplifting
- Can start with different system themes

#### Bug fixes
- no net adapter stops execution (added error handling)
- use of GiB, MiB and KiB for all tabs( for explicitly mentioning of power of 2s)
- [[Bug #1](https://github.com/KrispyCamel4u/SysMonTask/issues/1)] No need for pip3 install pygi-composite-templates

### v1.0.0
- Performance monitoring graphs
- Devices supported:
  * CPU
  * Memory
  * Disks
  * Network adapters
  * only single Nvidia GPU
