"""
加载DICOM 目录的事件
Created by DJ at 2020/10/2
"""
import os
from PyQt5.QtCore import QObject, pyqtSignal
from dicom import DicomDatasetGroup


class DicomDirSignal(QObject):
    """
    Define loading signal.
    """
    signal = pyqtSignal(object)

    def send(self, dicom_dir):
        self.signal.emit(dicom_dir)


class DicomDirSlot(QObject):
    """
    Define loading slot.
    """
    def process(self, dicom_dir):
        print(dicom_dir)    # TODO: for developing
        # 解析目录，提取dicom文件
        candidates = [os.path.join(dicom_dir, f) for f in sorted(os.listdir(dicom_dir))]
        file_list = [f for f in candidates if self.is_dicom_file(f)]
        print(file_list)    # TODO: for developing
        if not file_list:
            print("No file.")   # TODO: for developing
            return
        dicom_group = DicomDatasetGroup(file_list)
        dicom_group.print()
        return dicom_group

    @staticmethod
    def is_dicom_file(f):
        return '.dcm' in f or '.DCM' in f
