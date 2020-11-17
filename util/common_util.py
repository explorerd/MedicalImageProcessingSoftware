"""
Some common tool functions.
Created by DJ at 2020/11/17
"""
from dicom import PlaneType


def get_plane_name(plane):
    """
    Get the name of plane.
    :param plane:
    :return:
    """
    if plane == PlaneType.SAGITTAL_PLANE:
        return 'Sagittal'
    if plane == PlaneType.CORONAL_PLANE:
        return 'Coronal'
    if plane == PlaneType.AXIAL_PLANE:
        return 'Axial'


def get_other_planes(plane):
    """
    Get all other planes，exclude the given one.
    :param plane:
    :return:
    """
    return [get_plane_name(each) for each in PlaneType if each != plane]


def get_plane(plane_name):
    """
    根据名字（和get_plane_name函数中返回的名字对应）获取指定的Plane枚举
    :param plane_name:
    :return:
    """
    for each in PlaneType:
        if plane_name == get_plane_name(each):
            return each
