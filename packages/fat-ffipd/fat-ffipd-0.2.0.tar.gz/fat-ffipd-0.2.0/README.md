# fat-ffipd

Flask Application Template - For Fast Initial Project Develoment

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/fat-ffipd/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/fat-ffipd/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/fat-ffipd/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/fat-ffipd/commits/develop)|

![Logo](fat_ffipd/static/logo.png)

fat-ffipd is a basic flask template that includes a basic authentication system
wth API support, as well as a default layout that incorporates them.

It's meant to be a starting point for a flask app.

Also incorporated are docker and docker-compose files that make setting up a
website rather simple.

# Usage

To convert this project into a new one, run ```init.py``` and follow the
prompts. This will set up the project in a new directory, defined by the
project name given during prompting.

To start the web application, you can simply call ```python server.py``` after
installing it using ```python setup.py install```.

To run the application in docker, make sure all necessary environment
variables are stored in the ```.env``` file. Also make sure that the
```HTTP_PORT``` and ```DEPLOY_MODE``` environment variables are set.
If this is the case, simply run ```docker-compose up -d``` to start the
application.

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/fat-ffipd)
* [Github](namboy94/fat-ffipd)
* [Progstats](https://progstats.namibsun.net/projects/fat-ffipd)
* [PyPi](https://pypi.org/project/fat-ffipd)
