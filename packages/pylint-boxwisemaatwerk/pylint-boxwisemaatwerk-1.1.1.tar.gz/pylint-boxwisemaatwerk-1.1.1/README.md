# **pylint-boxwisemaatwerk maintainer README**

Build and dist are the files that are literally getting uploaded to PyPi. Its preferable that you make an account on PyPi to make updates. Most custom checkers are in in the checkers folders. Made a small monkeypatch to alter pylint default functionality. The files the checkers use are mostly made in the stub generator folder.  

**how to create:**  
note: make version 0.0.1 higher in the setup.py and delete the build and dist folder before executing the following code.

*   "python setup.py sdist bdist_wheel"
*   "python -m twine upload dist/* --verbose"  

login:*

password:*

**To install:**

execute "pip install pylint_boxwisemaatwerk" in command prompt

sources:

https://packaging.python.org/tutorials/packaging-projects/