# Reme - A Discord bot that will send you reminders

![PyPI - License](https://img.shields.io/pypi/l/reme) ![PyPI](https://img.shields.io/pypi/v/reme) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/reme) ![Travis (.org) branch](https://img.shields.io/travis/martinak1/reme/master?label=master%20build)
    
## NOTE: Reme uses a 24 hour clock in order to simplify datetimes

## Flags

    -d, debug - Reme echos what you send it after converting it to an Entry object
    -h, help  - Prints this usage docstring

## Message Formating
    
    !reme <Flag> <Message> @ mm/dd/yyyy hh:mm
    !reme <Flag> <Message> @ hh:mm
    !reme <Flag> <Message> +<Delta>[DdHhMm]

## Examples
    
### Print this help docstring

    !reme -h || !reme help

### Send a reminder 30 minutes from now

    !reme Take the pizza out of the oven +30m

### Send a reminder at 5:30 pm 
    !reme Go grocery shopping @ 17:30

### Send a reminder on October 30th at 4:30 pm

    !reme DND Session @ 10/30 16:30
    
## Install

    $ /usr/bin/env python3 -m pip install reme