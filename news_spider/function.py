#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import time

def LogError(msg):
    file = open('ErrorLog', 'a')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S') + '   ' + msg + '\n')
    file.close()