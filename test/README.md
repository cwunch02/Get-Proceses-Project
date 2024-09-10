# CPSC/ECE3220 Project1 Testcases

This folder contains all the testing code for TaskA and TaskB. All the test code should run from the project1 root directory.

# 1. Installing python dependencies

The test cases uses python for testing the code. So, Python3 and pip is required for this.  To install all the required dependencies:
```
 pip install -r ./test/requirement.txt
```
As pytest is not available in your `$PATH`, you have to edit the bashrc file and add pytest to it. To do this:
```
nano ~/.bashrc 
```
Add the below line to the end of the file:
```
export PATH="$HOME/.local/bin:$PATH"
```
save the file and load the new `$PATH` into the current shell session using the source command:
```
source ~/.bashrc
``` 
# 2. Testing code

For part1A the test setup always recompile the code and test using the files present in the testfiles folder.
To test part1A, run from project1 folder, the command:
```
pytest ./test/test_p1a_git.py
```
To test part1B, run from project1 folder, the command:
```
pytest ./test/test_p1b_git.py
```

For Part1A,the testcases test the main functionality, Error cases and Edge cases as mentioned in the Part1A documentation.\
For Part1B, a simple `testgetprocs.c` file is added to the user functions. The file create various process and calls `getprocs()` method to get all the processes.\
Pytest command shows a passed test case with `.` a Failed one with `F`. If the test cases fails, pytest will show the test function as well as the output it received after running the test command.
