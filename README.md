# pynerstat

A port/reimagining of the linux minerstat.com client: https://github.com/coinscrow/minerstat-linux

*Still a work in progress*

Testers highly appreciated! Please feel free to open issues if you find anything or contact us on
the minerstat slack. https://minerstat.com/slack.php


### To get started:

* make sure you have python3, pip3, virtualenv, libffi and libssl already installed:

    ```shell
    sudo apt-get -y install build-essential libssl-dev libffi-dev python3-dev python3-pip python-virtualenv
    ```

* then to install *pynerstat* run:

    ```shell
    curl https://raw.githubusercontent.com/dpnova/pynerstat/master/bin/install | bash
    ```

* now you can edit your `~/.minerstat/config.ini` to change your access token, worker name or
  default miner client

* or run `~/.minerstat/run` in your terminal to start mining
