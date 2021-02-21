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
