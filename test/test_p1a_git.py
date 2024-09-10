#!/usr/bin/python3
import os
import sys
import subprocess
import contextlib
import unittest
import shutil
import glob
import TestRunner
import time
from pathlib import Path
#import timeout_decorator


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
gpath = "./test/testfiles/"
exec_path = "./TaskA/"
fastsort_path = "./TaskA/fastsort "
def setUp():
    err = False
    print ()
    print("Cleaning working dir...")
    with cd(exec_path):
        make_args = ["rm", "-f", "fastsort"]
        p = subprocess.Popen(make_args)
        p.wait()

        print("Building...")
        make_args = ["make"]
        p = subprocess.Popen(make_args)
        p.wait()

        if not os.path.isfile("fastsort") and os.path.isfile("a.out"):
            shutil.move("a.out", "fastsort")
        (buf, err) = p.communicate()
    
    return err

def ex(exe):
    print("Running test...")
    owd = os.getcwd()
    print(exe)
    print(exec_path)
    p = subprocess.Popen(exe, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (buf, err) = p.communicate(timeout=120)
    
    return buf, err


#project 1a
class TestP1A_MainFunctionality(unittest.TestCase):
    def setUp(self):
        err = setUp() 
        if err is not None:
            self.fail()

    def ex(self, exe):
        return ex(exe)

    def testSort1(self):
        buf, err = self.ex(fastsort_path + gpath + "simple.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "simple1.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)

    def testSort2(self):
        buf, err = self.ex( f"{fastsort_path} -2 " + gpath + "simple.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "simple2.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)
    
    def testSort3(self):
        buf, err = self.ex(fastsort_path + gpath + "shuffled.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open( gpath + "sorted.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)
    
    def testSort4(self):
        buf, err = self.ex( f"{fastsort_path} -6 " + gpath + "shuffled6.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sorted6.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)

class TestP1A_ErrorCases(unittest.TestCase):
    def setUp(self):
        err = setUp() 
        if err is not None:
            self.fail()

    def ex(self, exe):
        return ex(exe)

    
    def testTooLong1(self):
        buf, err = self.ex(fastsort_path + gpath + "toolong1.txt")
        sol = "line too long"
        self.assertRegex(err.decode().replace("\r\n", "\n").lower(), sol)
        sol = ''
        self.assertEqual(buf.decode(), sol)

    def testTooLong2(self):
        buf, err = self.ex(fastsort_path + gpath + "toolong2.txt")
        sol = "line too long"
        self.assertRegex(err.decode().replace("\r\n", "\n").lower(), sol)
        sol = ''
        self.assertEqual(buf.decode(), sol)
    
    def testTooLong3(self):
        buf, err = self.ex(fastsort_path + gpath + "toolong3.txt")
        sol = "line too long"
        self.assertRegex(err.decode().replace("\r\n", "\n").lower(), sol)
        sol = ''
        self.assertEqual(buf.decode(), sol)
    
    def testNotTooLong(self):
        buf, err = self.ex(fastsort_path + gpath + "nottoolong.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sortednottoolong.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)
    

class TestP1A_EdgeCases(unittest.TestCase):
    def setUp(self):
        err = setUp() 
        if err is not None:
            self.fail()

    def ex(self, exe):
        return ex(exe)

    def testEmptyLine(self):
        buf, err = self.ex(fastsort_path + gpath + "emptyline.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sortedemptyline.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)
    
    def testUnevenLines(self):
        buf, err = self.ex(f"{fastsort_path} -2 " + gpath + "unevenwords.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sortedunevenwords.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)
    
    def testStartSpace(self):
        buf, err = self.ex(fastsort_path + gpath + "startspace.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sortedstartspace.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)

    def testNoSecondWord(self):
        buf, err = self.ex( f"{fastsort_path} -2 " + gpath + "startspace.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sortedstartspace.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)
    
    def testMultiSpace(self):
        buf, err = self.ex( f"{fastsort_path} -2 " + gpath + "multispace.txt")
        sol = ""
        self.assertEqual('', err.decode())
        with open(gpath + "sortedmultispace.txt", "r") as sor:
            sol = sor.read()
        self.assertRegex(buf.decode().replace("\r\n", "\n"), sol)

class TestP1A_MemLeaks(unittest.TestCase):
    def setUp(self):
        err = setUp() 
        if err is not None:
            self.fail()

    def ex(self, exe):
        return ex(exe)

    def testMemLeaks(self):
        buf, err = self.ex(f"valgrind {fastsort_path} -2 " + gpath + "simple.txt")
        sol = "All heap blocks were freed"
        self.assertRegex(err.decode().replace("\r\n", "\n"), sol)


