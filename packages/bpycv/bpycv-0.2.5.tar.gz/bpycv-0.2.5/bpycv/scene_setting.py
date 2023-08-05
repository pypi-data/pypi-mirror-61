#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Thu Jan 16 18:17:20 2020
"""

from boxx import *
from boxx import deg2rad, np, pi

import bpy
import random


def set_cam_pose(cam_radius=1, cam_deg=45, cam_x_deg=None, cam=None):
    cam_rad = deg2rad(cam_deg)
    if cam_x_deg is None:
        cam_x_deg = random.uniform(0, 360)
    cam_x_rad = deg2rad(cam_x_deg)
    z = cam_radius * np.sin(cam_rad)
    xy = (cam_radius ** 2 - z ** 2) ** 0.5
    x = xy * np.cos(cam_x_rad)
    y = xy * np.sin(cam_x_rad)
    cam = cam or bpy.data.objects["Camera"]
    cam.location = x, y, z
    cam.rotation_euler = pi / 2 - cam_rad, 0.1, pi / 2 + cam_x_rad
    cam.scale = (0.1,) * 3
    return cam


def remove_useless_data():
    """
    remove all data and release RAM
    """
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)


def clear_all():
    [
        bpy.data.objects.remove(obj)
        for obj in bpy.data.objects
        if obj.type in ("MESH", "LIGHT", "CURVE")
    ]
    remove_useless_data()


if __name__ == "__main__":
    pass
