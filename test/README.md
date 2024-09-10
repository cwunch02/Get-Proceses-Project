
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

To test , run from project/downloaded directory, the command:
```
pytest ./test/test_p1b_git.py
```
