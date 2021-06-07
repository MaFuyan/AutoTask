#!/usr/bin/env python
# -*- encoding=utf8 -*-

class AsstException(Exception):

    def __init__(self, message):
        super().__init__(message)
        print(message)
