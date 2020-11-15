"""
定义解剖面枚举
Created by DJ at 2020/11/15
"""
from enum import Enum


class PlaneType(Enum):
    """
    三个解剖面
    """
    SAGITTAL_PLANE = 0
    CORONAL_PLANE = 1
    AXIAL_PLANE = 2
