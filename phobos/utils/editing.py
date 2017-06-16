#!/usr/bin/python
# coding=utf-8

"""
.. module:: phobos.utils.general
    :platform: Unix, Windows, Mac
    :synopsis: This module contains general functions to use in operators and custom scripts

.. moduleauthor:: Kai von Szadowski

Copyright 2017, University of Bremen & DFKI GmbH Robotics Innovation Center

This file is part of Phobos, a Blender Add-On to edit robot models.

Phobos is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

Phobos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Phobos.  If not, see <http://www.gnu.org/licenses/>.
"""

import bpy
from . import selection as sUtils

def addDictionaryToObj(dict, obj, category=None):
    for key, value in dict:
        obj[(category+'/'+key) if category else key] = value


def getCombinedTransform(obj, effectiveparent):
    parent = obj.parent
    matrix = obj.matrix_local
    while parent != effectiveparent and parent is not None:
        matrix = parent.matrix_local * matrix
        parent = parent.parent
    return matrix


def instantiateAssembly(assemblyname):
    assembly = None
    interfaces = None
    for group in bpy.data.groups:
        if group.name.startswith(assemblyname):
            if group.name.endswith('interfaces'):
                interfaces = group
            else:
                assembly = group
    if not assembly or not interfaces:
        raise RuntimeError('Assembly and/or interfaces templates do not exist.')
    bpy.ops.object.group_instance_add(group=assembly.name) #location=(2.85218e-09, 0.0958416, 1.20279), layers=())
    assemblyobj = bpy.context.active_object
    bpy.ops.object.group_instance_add(group=interfaces.name) #location=(2.85218e-09, 0.0958416, 1.20279), layers=())
    interfaceobj = bpy.context.active_object
    bpy.ops.object.duplicates_make_real()
    sUtils.selectobjects(objects=[assemblyobj]+bpy.context.selected_objects, clear=True, active=0)
    bpy.ops.object.parent_set(type='OBJECT')
    sUtils.selectObjects(objects=[a for a in bpy.context.selected_objects
                                  if a.type == 'EMPTY' and a.name.endswith('interfaces')],
                         clear=True, active=0)
    bpy.ops.object.delete(use_global=False)


def connectInterfaces(parentinterface, childinterface):
    childassembly = childinterface.parent
    sUtils.selectobjects(objects=[childinterface], clear=True, active=0)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    sUtils.selectobjects(objects=[childinterface, childassembly], clear=True, active=0)
    bpy.ops.object.parent_set(type='OBJECT')
    sUtils.selectobjects(objects=[parentinterface, childinterface], clear=True, active=0)
    bpy.ops.object.parent_set(type='OBJECT')

