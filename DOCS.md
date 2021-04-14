## Menu 
- File : Nothing much, reserved for future use
- View : Refresh, Update Speed, Graph Direction
  * Refresh : For accomodating a new hardware related change such as network change.
  * Update Speed : Speed control for performance tab.
  * Graph Direction : Newer on Right(default) / Newer on Left
  * **Filter**: To Filter out the unwanted processes.
- Help : About, What's New

## Filter Dialog (View->Filter)
Filter filters out the unwanted system/user processes by using custom filtering words which can be defined in FILTER dialog.

Column description:
- Status: Shows the On/Off status of the filter word of the row.
- Filter String: Word/String to be used for filtering. String is matched in Name, Owner and command column.
- Depth: Since the process are shown in Parent Child fashion, depth depicts the level of this hierarchy.
   * -1: All child with parent(first matched with Filter String) process are filtered out.
   * 0: Effectively no filtering is done for the matched process.
   * 1: Only the process with a match is filtered all it's child are not effected.
   * 2: With the matched process all immediate child are also filtered out.
   * and so on.
- Regex: Whether the Matching is done using regular expressions(the Filter String will be treated as regular expression) or not.

*Certain syntex and sementic rules need to be followed to use Filter:*

![Screenshot from 2021-04-14 22-42-58](https://user-images.githubusercontent.com/48773008/114751481-d298e480-9d72-11eb-8fc2-13b370b557f2.png)

#### Syntex and Sementics for New Entry:
**Type I:**
```
<String> : <Depth>     OR      <String>
```
Where String will be matched in process **Name, Owner and Command**. A match in any of the field will considered as a Filter match and that process will be filtered out with its child defined by the depth. The ***Depth*** field is **optional** and default value is ***-1***. Matching mechanism if regex is **OFF**
would ***"String1 in String2"*** and if regex is **ON** regex match would be performed.

*Multiple Entries Can be added at one time by using ";" between entries.
``` root:-1 ; libexec ;gpg:4```*

---

**Type II:**
*Use of segregating two ",(commas)" are must.*
```
<Name>,<Owner>,<Command> :<Depth>   OR   <Name>,,  OR ,<Owner>,<Command>:<Depth>  OR  ,,<Command>   OR   <Name>,<Owner>,   
OR any Combination with same pattern. 
```
Where the String at **Name, Owner and Command** fields will be matched against respective columns in the process table. A successful Filter match will only occur
if each is String field is matched successfully in their respective process column fields. When any of String field is empty that will be not be considered for matching and others are tried with their respective columns.
The ***Depth*** field is **optional** and default value is ***-1***. Matching mechanism if regex is **OFF**
would ***"String1 in String2"*** and if regex is **ON** regex match would be performed.

*Duplicate Entries are ignored*

#### Add, Save and Delete
- A Enter and click on "Add" button will put the filled entry to the list.
- To make the change appear in the Process Tab immediately after adding entries then Save them with ***Save*** Button. Otherwise the changes will only appear on the next time of spawing the sysmontask.
- Entries can be deleted by "delete" button but **the entry ",root,:-1" can not be deleted.**

#### Keywords For Various Desktop Environments:


---

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



