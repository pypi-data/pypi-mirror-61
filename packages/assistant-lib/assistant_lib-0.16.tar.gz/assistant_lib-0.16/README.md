# Assistant library

This Python 3.x library is used to write programs that can interact with the Assistant. 

Assistant : https://gitlab.com/goassistant/assistant

Pypi webpage : https://pypi.org/project/assistant-lib

# Changelog

## 1.0 : new discovery format 

Improvments :

* Handle the new peer discovery protocol set in Assistant > 0.3

Features : 

* (NEW) Helper to get the version from git.
* Helper to init logging properly.
* Helper to show the component to the others (peer discovery). Seeing the other components is not yet implemented.
* Helper to generate SSL certificates.

## 0.15 : initial usable release

First usable release.

Features : 

* Helper to init logging properly.
* Helper to show the component to the others (peer discovery). Seeing the other components is not yet implemented.
* Helper to generate SSL certificates

# License

The license choosen for this project it the LGPLv3. It was choosen instead of the GPLv3 because : 

> The license allows developers and companies to use and integrate a software component released under the LGPL into their own (even proprietary) software without being required by the terms of a strong copyleft license to release the source code of their own components. However, any developer who modifies an LGPL-covered component is required to make their modified version available under the same LGPL license. 

See [Wikipedia](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License) for more informations.

# Installation

pip3 install assistant-lib

# Usage

Here is a simple test :

```
$ python3
Python 3.7.4 (default, Jul 11 2019, 10:43:21) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from assistant_lib import assistant
>>> ac = assistant.AssistantClient()
Output redirected to the file : 'assistant.log'
>>> ac.get_hostname()
'ambre'
```

# Logging

When you initialise the assistant client with:

```
ac = assistant.AssistantClient()
```

It will also configure the python logging engine. You will just have to use the standard logging functions :

```
logging.debug("A debug message")
logging.info("An info message")
logging.warning("A warning message")
logging.error("An error message")
```

By default, the logs are written in a log file named __assistant.log__ in the __debug__ log level. The logs are written in json format to be ready to be used by logging centralization tools as Elastic or Datalog.

If you want to change this behavious, just set the following environement variables:

* LOG_FILE : a path to a file
* LOG_LEVEL : a log level : DEBUG, INFO, WARNING, ERROR

Examples with an application foobar.py : 

```
$ LOG_LEVEL=DEBUG LOG_FILE=/var/log/foobar.log /usr/bin/python3 foobar.py
$ LOG_LEVEL=WARNING /usr/bin/python3 foobar.py
```

If you don't want to log in a file and prefer to log in the console, use this environment variable :

* LOG_OUTPUT : TTY to log in console, anything else to log in a file.

Example :

```
$ LOG_OUTPUT=TTY /usr/bin/python3 foobar.py
```

The log displayed in the console are no more in json format.

## Logging limitations

The json logging formatter does not handle the old python way to include variables in strings like this :

```
a = 8
logging.info("The number 8 will not be display : %d" % a)
```

You must use the new way :

```
a = 8
logging.info("The number 8 will be display : {0}".format(a))
```

# Local tests

If you plan to make some upgrades and test them, here is how to process :

* Edit your changes in the code
* Run the clean and build command: 

```
make
```

* Check the dist/ folder
* Install the builded package from the dist/ folder:

```
pip3 install dist/assistant_lib-<version>.tar.gz
```

# Releasing 

The version number is automatically get from git thanks to the setuptools_scm library. So you have no version to set in the code.

To create a new release, just create a tag and push it to Gitlab. The CI/CD pipeline will build a release and publish it to Pypi. This is just magic ;). You can check the .gitlab-ci.yml file to understand how it works.





