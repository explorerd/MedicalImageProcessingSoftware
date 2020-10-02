"""
事件signal和slot对象
Created by DJ at 2020/10/2
"""
from load_dicom_event import DicomDirSignal, DicomDirSlot


class Events:
    def __init__(self):
        self.dicom_dir_signal = DicomDirSignal()
        self.dicom_dir_slog = DicomDirSlot()
        self.connect()

    def connect(self):
        self.dicom_dir_signal.signal.connect(self.dicom_dir_slog.process)


events = Events()
