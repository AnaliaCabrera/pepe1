# Installation

## Using Anaconda in Windows

In Windows Anaconda provides some tools to simplify the setup.

Install Anaconda3 [their installer](https://repo.continuum.io/archive/Anaconda3-5.0.1-Windows-x86_64.exe)

Once installed you will find an `Anaconda Prompt` program in the windows menu. All the following commands should be typed into this `Anaconda Prompt` shell.

1. Create a new environment for this package
```
$ conda create --name d2b_env python=3.6
```
2. Activate the new environment
```
$ activate d2b_env
```
3. Move to the cloned directory, d2b_tools folder:
```
$ cd C:\....\pepe1\d2b_tools
```
3. Install requirements:
```
$ conda install --yes --file requirements.txt
```
4. In  the same directory, run 
```
$ pip install -e .
```
5. Run the tests
```
$ cd tests
$ python test_measurements_reader.py
```
#Run test after instalation
Repeat point 2. and 5.

## Using virtualenv in Linux

1. Create a python 3 virtualenv
```
$ pyvenv d2benv
```
2. Activate the new environment
```
$ source d2benv/bin/activate
```
3. Install the dependencies
```
$ pip install -r requirements.txt
```
4. Install the d2b_tools package
```
$ pip install -e .
```
