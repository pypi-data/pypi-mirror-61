#
#    Copyright (c) 2020 Google LLC.
#    All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

#
#    @file
#      Python interface for Weave Stack
#

"""Weave Stack interface
"""

from __future__ import absolute_import
from __future__ import print_function
import functools
import sys
import os
import re
import copy
import binascii
import datetime
import time
import glob
import platform
import ast
from threading import Thread, Lock, Event
from ctypes import *
from .WeaveUtility import WeaveUtility

__all__ = [ 'DeviceStatusStruct', 'WeaveStackException', 'DeviceError', 'WeaveStackError', 'WeaveStack' ]

WeaveStackDLLBaseName = '_WeaveDeviceMgr.so'

def _singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper

class DeviceStatusStruct(Structure):
    _fields_ = [
        ("ProfileId",       c_uint32),
        ("StatusCode",      c_uint16),
        ("SysErrorCode",    c_uint32)
    ]

class WeaveStackException(Exception):
    pass

class WeaveStackError(WeaveStackException):
    def __init__(self, err, msg=None):
        self.err = err
        if msg != None:
            self.msg = msg
        else:
            self.msg = "Weave Stack Error %ld" % (err)

    def __str__(self):
        return self.msg

class DeviceError(WeaveStackException):
    def __init__(self, profileId, statusCode, systemErrorCode, msg=None):
        self.profileId = profileId
        self.statusCode = statusCode
        self.systemErrorCode = systemErrorCode
        if (msg == None):
            if (systemErrorCode):
                return "[ %08X:%d ] (system err %d)" % (profileId, statusCode, systemErrorCode)
            else:
                return "[ %08X:%d ]" % (profileId, statusCode)
        self.message = msg

    def __str__(self):
        return "Device Error: " + self.message

_CompleteFunct                              = CFUNCTYPE(None, c_void_p, c_void_p)
_ErrorFunct                                 = CFUNCTYPE(None, c_void_p, c_void_p, c_ulong, POINTER(DeviceStatusStruct))

@_singleton
class WeaveStack(object):
    def __init__(self):
        self.networkLock = Lock()
        self.completeEvent = Event()
        self._weaveStackLib = None
        self._weaveDLLPath = None
        self.devMgr = None
        self.callbackRes = None

        self._InitLib()

        def HandleComplete(appState, reqState):
            self.callbackRes = True
            self.completeEvent.set()

        def HandleError(appState, reqState, err, devStatusPtr):
            self.callbackRes = self.ErrorToException(err, devStatusPtr)
            self.completeEvent.set()

        self.cbHandleComplete = _CompleteFunct(HandleComplete)
        self.cbHandleError = _ErrorFunct(HandleError)
        self.blockingCB = None # set by other modules(BLE) that require service by thread while thread blocks.

    def Shutdown(self):
        self._weaveStack.Call(
            lambda: self._dmLib.nl_Weave_Stack_Shutdown()
        )
        self.networkLock = None
        self.completeEvent = None
        self._weaveStackLib = None
        self._weaveDLLPath = None
        self.devMgr = None
        self.callbackRes = None

    def Call(self, callFunct):
        # throw error if op in progress
        self.callbackRes = None
        self.completeEvent.clear()
        with self.networkLock:
            res = callFunct()
        self.completeEvent.set()
        if res == 0 and self.callbackRes != None:
            return self.callbackRes
        return res

    def CallAsync(self, callFunct):
        # throw error if op in progress
        self.callbackRes = None
        self.completeEvent.clear()
        with self.networkLock:
            res = callFunct()
    
        if (res != 0):
            self.completeEvent.set()
            raise self.ErrorToException(res)
        while (not self.completeEvent.isSet()):
            if self.blockingCB:
                self.blockingCB()
    
            self.completeEvent.wait(0.05)
        if (isinstance(self.callbackRes, WeaveStackException)):
            raise self.callbackRes
        return self.callbackRes
    
    def ErrorToException(self, err, devStatusPtr=None):
        if (err == 4044 and devStatusPtr):
            devStatus = devStatusPtr.contents
            msg = WeaveUtility.CStringToString((self._weaveStackLib.nl_Weave_Stack_StatusReportToString(devStatus.ProfileId, devStatus.StatusCode)))
            sysErrorCode = devStatus.SysErrorCode if (devStatus.SysErrorCode != 0) else None
            if (sysErrorCode != None):
                msg = msg + " (system err %d)" % (sysErrorCode)
            return DeviceError(devStatus.ProfileId, devStatus.StatusCode, sysErrorCode, msg)
        else:
            return WeaveStackError(err, WeaveUtility.CStringToString((self._weaveStackLib.nl_Weave_Stack_ErrorToString(err))))

    def LocateWeaveDLL(self):
        if self._weaveDLLPath:
            return self._weaveDLLPath

        scriptDir = os.path.dirname(os.path.abspath(__file__))

        # When properly installed in the weave package, the Weave Device Manager DLL will
        # be located in the package root directory, along side the package's
        # modules.
        dmDLLPath = os.path.join(scriptDir, WeaveStackDLLBaseName)
        if os.path.exists(dmDLLPath):
            self._weaveDLLPath = dmDLLPath
            return self._weaveDLLPath

        # For the convenience of developers, search the list of parent paths relative to the
        # running script looking for an OpenWeave build directory containing the Weave Device
        # Manager DLL. This makes it possible to import and use the WeaveDeviceMgr module
        # directly from a built copy of the OpenWeave source tree.
        buildMachineGlob = '%s-*-%s*' % (platform.machine(), platform.system().lower())
        relDMDLLPathGlob = os.path.join('build', buildMachineGlob, 'src/device-manager/python/.libs', WeaveStackDLLBaseName)
        for dir in self._AllDirsToRoot(scriptDir):
            dmDLLPathGlob = os.path.join(dir, relDMDLLPathGlob)
            for dmDLLPath in glob.glob(dmDLLPathGlob):
                if os.path.exists(dmDLLPath):
                    self._weaveDLLPath = dmDLLPath
                    return self._weaveDLLPath

        raise Exception("Unable to locate Weave Device Manager DLL (%s); expected location: %s" % (WeaveStackDLLBaseName, scriptDir))

    # ----- Private Members -----
    def _AllDirsToRoot(self, dir):
        dir = os.path.abspath(dir)
        while True:
            yield dir
            parent = os.path.dirname(dir)
            if parent == '' or parent == dir:
                break
            dir = parent

    def _InitLib(self):
        if (self._weaveStackLib == None):
            self._weaveStackLib = CDLL(self.LocateWeaveDLL())
            self._weaveStackLib.nl_Weave_Stack_Init.argtypes = [ ]
            self._weaveStackLib.nl_Weave_Stack_Init.restype = c_uint32
            self._weaveStackLib.nl_Weave_Stack_Shutdown.argtypes = [ ]
            self._weaveStackLib.nl_Weave_Stack_Shutdown.restype = c_uint32
            self._weaveStackLib.nl_Weave_Stack_StatusReportToString.argtypes = [ c_uint32, c_uint16 ]
            self._weaveStackLib.nl_Weave_Stack_StatusReportToString.restype = c_char_p
            self._weaveStackLib.nl_Weave_Stack_ErrorToString.argtypes = [ c_uint32 ]
            self._weaveStackLib.nl_Weave_Stack_ErrorToString.restype = c_char_p

        res = self._weaveStackLib.nl_Weave_Stack_Init()
        if (res != 0):
            raise self._weaveStack.ErrorToException(res)