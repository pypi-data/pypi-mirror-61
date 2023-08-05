# Configuration.py
A port of Conf.rb (https://rubygems.org/gems/confrb), my Ruby config library, to Python.

## Confpy - class
To access methods of this class, import the Confpy class (`from configurationpy import confpy`). Then: `varname = Confpy(databasename)` where `databasename` is a string and varname is the name of the variable you're going to be using to access your database. This creates a new database. Alternatively, just do `varname = Confpy.access(databasename)` where `databasename` is a string. This throws an error if the database does not already exist.  After that, just run `varname.method(parameters method accepts)`.


```python
mkcfg('cfgfilename', 'content', json: false, yamlencode = False, jsonencode = False, prepend_newline = False, append_newline = False)
```
Creates a new config file.
`cfgfilename` is the filename of the config file you wish to create.
`content` is your content! 
Use nested directories using os.path.join() for crossplatform support. The following arguments are optional:
* `jsonencode = False` is the default value and writes the data passed as-is. `json: true`, however, formats the data as JSON before writing it. This is useful for hashes being formatted as JSON to retain compatibility with other languages.
* `yamlencode = False` is the default value and writes the data passed as-is. `yaml: true`, however, formats the data as YAML before writing it. This is useful for hashes being formatted as YAML to retain compatibility with other languages.
* Newline options are obvious.

```python
mknested('nesteddirname')
```
Creates a nested config dir., where `nesteddir` is the nested directory name. 

```python
readcfg('filename', jsonencode = False, yamlencode = False)
```
Reads a config file `filename`..

OPTIONAL:
jsonencode and yamlencode take JSON/YAML data, respectively, and convert it back into a Python object. TODO: name it `yamldecode` and `jsondecode`.
```python
rmcfg('filename')
```
Removes the configuration file `filename`. 
```python
rmdb()
```
Simply removes the whole database that this is called on. 

```python
rmnested('nesteddirname')
```
Removes a nested directory `nesteddirname` inside your database. Use os.path.join() to remove multiple recursively.
```python
writecfg('cfgfilename', 'content', jsonencode = False, yamlencode = False, prepend_newline = True, append_newline = False)
```
Same as mkcfg(). However, if the file exists, it is appended to. prepend_newline is also set to True by default.
```python
exist('filename')
```
Returns a boolean (True/False) based on if the file `filename` exists in your database or not.