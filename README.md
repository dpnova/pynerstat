# pynerstat

A port/reimagining of the linux minerstat.com client: https://github.com/coinscrow/minerstat-linux

Still a work in progress, not ready for use yet as I fugure out some of the quirks with the minerstat service (kinda reverse engineering it)

To get started:

* make sure you have pip3 and libffi installed: `sudo apt-get install python3-pip libffi-dev python-virtualenv`
* run `bin/install`
* edit `~/.minerstat/config.ini` and make sure you have your token from minerstat.com set up properly
* run `minerstat` in your terminal


