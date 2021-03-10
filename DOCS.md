## Menu 
- File : Nothing much reserved for future use
- View : Refresh, Update Speed, Graph Direction
  * Refresh : For accomodating a new hardware related change such as network change.
  * Update Speed : Speed control for performance tab.
  * Graph Direction : Newer on Right(default) / Newer on Left
- Help : About

## Process Tab
- Processes are shown in Parent and Child relation with filtering algorithm to filter out the background processes that are not as useful as the process that the user creates. Processes which have their origin from "/libexec" or has "deamon" or "dbus" are considered as background processes. Each row consists of tree like structure that can be sorted from any column.
- The top of column (headers) shows the overall system performance metrics.
![Screenshot from 2021-02-14 18-39-10](https://user-images.githubusercontent.com/48773008/108234592-f4a72980-716a-11eb-9a56-44ee60cba604.png)

#### Each column
- Pid : Unique Process Id for the process
- Name  : Name of the process
- ***rCPU :** The overall CPU utilisation of the parent + CPU utilisation of all of its children and children of child being a recursive value, for the leaf process the CPU and rCPU would be same. 

  Example: Process FireFox
  
  The rCPU for the FireFox will be the sum of all the CPU utilisations of all its children (web contents) and their rCPU and CPU column are same as they don't have children.
  
  FireFox_rCPU = FireFox_CPU + All_child_CPU : 1.4 + 0.6 + 0.1 + 0.1 + 0.4 + 0.1 + 0.6 +0.1 = 3.4
  
  ![image](https://user-images.githubusercontent.com/48773008/108231171-7f862500-7167-11eb-8616-01d662342d14.png)
  
- CPU : CPU utilisation for that process
- ***rMemory :** Recursive Memory utilisation calculated similarily as rCPU. This gives a better idea as to how much a process is using the memory.

  In the above example the "FireFox" uses 547.4 MiB as only one process while as a whole with child it uses 3039 MiB which is the real truth. 
- Memory : The Memory Utilisation of the process which solely belongs to the process. Calculated as **Resident_Memory - Shared_Memory = Memory util of the process**.
- DiskRead : The disk read speed at which the process is doing IO operations.
- DiskWrite : The disk write speed at which the process is doing IO operations.
- ***rDiskRead:** Recursive Disk Read calculated similar to rMemory and rCPU. 
- ***rDiskWrite:** Recursive Disk Write similar to rDiskRead.
- Resident Memory: It is the actual memory that is in the physical memory associated to the given process (not only this process also includes the shared memory with other processes).
- Shared : Shared memory with other processes.
- Owner : User to whom the process belongs.
- Command : The command corresponding to the process.

#### Killer
- It is a process kill button. Pressing it would cause the process to get terminated after asking for a confirmation.
![image](https://user-images.githubusercontent.com/48773008/108235398-cbd36400-716b-11eb-8b78-36a883a98a8e.png)
![image](https://user-images.githubusercontent.com/48773008/108235101-86169b80-716b-11eb-94f3-0fa203fd0c2a.png)

## Performance Tab
- Shows the graphs for the major computer devices.
- Contains graph for : CPU, Memory, Disks, Network Adapters, Nvidia GPU



