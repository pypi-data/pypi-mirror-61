pyMODI
======

[![image](https://img.shields.io/pypi/v/pymodi.svg)](https://pypi.python.org/pypi/pymodi)

[![image](https://img.shields.io/pypi/pyversions/pymodi.svg)](https://pypi.python.org/pypi/pymodi)

[![image](https://img.shields.io/travis/LUXROBO/pyMODI.svg)](https://travis-ci.org/LUXROBO/pyMODI)

[![Documentation Status](https://readthedocs.org/projects/pymodi/badge/?version=latest)](https://pymodi.readthedocs.io/en/latest/?badge=latest)

[![Updates](https://pyup.io/repos/github/LUXROBO/pyMODI/shield.svg)](https://pyup.io/repos/github/LUXROBO/pyMODI/)

Easy😆 and fast💨 MODI Python API package.

-   Free software: MIT license
-   Documentation: <https://pymodi.readthedocs.io>.

Features
--------

-   Connect to the MODI network module and control input & output
    modules.
-   List serial ports of MODI network modules.
-   Turn on or off the PnP mode of MODI modules.
-   Get the position information of each modules.

Build Status
--------

master:

[![image](https://travis-ci.org/LUXROBO/pyMODI.svg?branch=master)](https://travis-ci.org/LUXROBO/pyMODI)

develop:

[![image](https://travis-ci.org/LUXROBO/pyMODI.svg?branch=develop)](https://travis-ci.org/LUXROBO/pyMODI)

Quickstart
--------

Install the latest pyMODI if you haven\'t installed it yet:

    pip install -U pymodi

Import [modi]{.title-ref} package and create [MODI]{.title-ref}
instance:

    import modi
    bundle = modi.MODI()

List connected modules:

    bundle.modules

List connected LED modules and pick the first one:

    bundle.leds # List.
    bundle.leds[0] # Pick.

Let\'s blink the LED\'s light 5 times:

    import time

    led = bundle.leds[0]

    for _ in range(10):
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
