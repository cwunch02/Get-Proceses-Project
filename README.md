# Get Processes System Call Project
The first real project for my Operating Systems class was to add a system call to the xv6 UNIX operating system. xv6 is a remake of UNIX version 6 (v6) that was created by Dennis Ritchie and Ken Thompson. It's used as a teaching and testing tool as the kernel is simple and small allowing for easier modifications.

This project involved adding a system call that would count the number of open processes. This was achieved through looking at the mkfs, user, and kernel files to get a basic design for a system call and to find out what calls and sees running processes. After this, it simply counts the processes and outputs it.

Feel free to try it out with the testing files in the test directory!
