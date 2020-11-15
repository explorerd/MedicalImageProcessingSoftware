"""
处理读取文件相关操作
Created by DJ at 2020/11/15
"""
import os
import pydicom


def read_dicom(dicom_dir):
    """
    读取目录dicom_dir下的dicom文件
    :param dicom_dir:
    :return:
    """
    files = [os.path.join(dicom_dir, each) for each in os.listdir(dicom_dir)]
    dicom_files = [pydicom.read_file(each) for each in files if each.endswith('.dcm') or each.endswith('.DCM')]
    return dicom_files
