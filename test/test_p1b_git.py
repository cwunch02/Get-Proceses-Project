import pexpect
import os
import os.path
import sys
import subprocess
import unittest
import shutil
import contextlib
import TestRunner
import stat

@contextlib.contextmanager
def cd(path):
    CWD = os.getcwd()
    
    os.chdir(path)
    try:
        yield
    except Exception as ex:
        logging.exception("Error yielding after changing directory")
    finally:
        os.chdir(CWD)
output_lines = None
index = 0
exec_path="./TaskB"
test_path= "./test"

def get_line_val():
    global index
    print("Index:", index)
    out_val = None
    i = 0
    for i in range(index, len(output_lines)):
        if "TEST" in output_lines[i]:
            line = output_lines[i]
            out_val = line.split()[1]
            break
    index = i + 1
    return out_val


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# for students who don't ever listen
def find(name, path):
    result = "."
    for root, dirs, files in os.walk(path):
        for d in dirs:
            if "xv6" in d:
                return os.path.join(root, d)
    return result

def ex_vm(exe):
    global index
    err = False
    
    print(exec_path)

    print(test_path)
    shutil.copyfile( f"{test_path}/Makefile", f"{exec_path}/Makefile")
    shutil.copyfile( f"{test_path}/testgetprocs.c", f"{exec_path}/user/testgetprocs.c")
    with cd(exec_path):
        make_args = ["make", "clean"]
        p = subprocess.Popen(make_args)
        p.wait()

        make_args = ["make", "fs.img", "kernel/kernel", "CL_EXTRA=testgetprocs.c", "CL_UPROGS=_testgetprocs", "-j", "4"]
        p = subprocess.Popen(make_args)
        p.wait()
        (buf, err) = p.communicate()

        print ("ERR:", err)

        if err is None or err is False:
            vm = pexpect.spawn('qemu-system-riscv64 -nographic -machine virt -bios none -kernel kernel/kernel -m 3G -smp 3 -nographic -drive file=fs.img,if=none,format=raw,id=x0 -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0')
            vm.logfile = sys.stderr.buffer
            buf = []
            try:
                vm.expect('init: starting sh\r\n')
                vm.expect('\$ ')
                vm.sendline(exe)
                vm.expect('\$', timeout=20)
                buf = vm.before
                vm.sendline('\x01x')
            except:
                eprint("Exception in expect")
                eprint(str(vm))
                eprint(sys.exc_info()[0])
                err = True
            
    return buf, err

def run_vm():
    buf, err = ex_vm("testgetprocs")
    if (err != 0 and err != False and err != None):
        eprint ("Bad error value:", err)
        eprint ("Output buffer:\n", buf)
        err = True
    else:
        print ("Output:")
        print (buf.decode('ascii'))
        buf = buf.decode('ascii')
        err = False
    return buf, err


#project 1
class TestP1(unittest.TestCase):
    # probably should migrate the above to this function
    def setUp(self):
        global output_lines

        buf,err = run_vm()
        if err is False:
            output_lines = buf.splitlines() 
    def test1_default_procs(self):
        # Test1 checks for basic procs - should be 3
        # 1. Init
        # 2. sh
        # 3. testgetprocs
        self.assertEqual(int(get_line_val()), 3)

    def test2_forks(self):
        # Test2 includes the prior, but also creates 5 sleeping forks
        print(output_lines)
        self.assertEqual(int(get_line_val()), 8)

    def test3_fork_death(self):
        # Test3 is a repeat of the first test after 3 waits
        self.assertEqual(int(get_line_val()), 5)
    
    def test4_fork_death_2(self):
        # Test4 is a repeat of the first test all waits
        self.assertEqual(int(get_line_val()), 3)

