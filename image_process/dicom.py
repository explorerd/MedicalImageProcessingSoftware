"""
DicomGroup 对象用于保存一组dicom图像信息
Created by DJ at 2020/10/2
"""
import pydicom
import numpy as np
from modalities import Modality


class DicomDatasetGroup:
    """
    包含一组Dicom文件的信息，主要存储图像信息
    """
    def __init__(self, file_list: list):
        # 假定当前的一组dicom文件是同一个病人的同一个series的图像
        dss = [pydicom.read_file(each) for each in file_list]
        ds = dss[0]
        self.dss = [DicomDataset(each) for each in dss]
        self.patient_name = None
        self.patient_id = None
        self.series = None
        if 'PatientName' in ds:
            self.patient_name = ds.PatientName
        if 'PatientId' in ds:
            self.patient_id = ds.PatientId
        if 'SeriesNumber' in ds:
            self.series = ds.SeriesNumber

    def print(self):
        print(f'Patient name is {self.patient_name}, patient id is {self.patient_id}, '
              f'series number is {self.series}')
        print('=====pixel array is ========')
        for each in self.dss:
            print(each.pixel_array)


class DicomDataset:
    """
    表示一个Dicom文件
    """
    def __init__(self, ds):
        self.pixel_array = None
        if 'Modality' not in ds:
            return
        modality = ds.Modality
        if modality is Modality.CT.name:
            # ds.RescaleSlope * ds.pixel_array + ds.RescaleIntercept 将原始数据
            self.pixel_array = ds.RescaleSlope * ds.pixel_array + ds.RescaleIntercept
        if 'pixel_array' in ds:
            self.pixel_array = ds.pixel_array
