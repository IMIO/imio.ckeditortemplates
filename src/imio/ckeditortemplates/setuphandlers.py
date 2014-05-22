# -*- coding: utf-8 -*-
def testSetup(context):
    if context.readDataFile('imio.ckeditortemplates.txt') is None:
        return
