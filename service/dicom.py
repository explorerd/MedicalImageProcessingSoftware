"""
描述一系列dicom文件
Created by DJ at 2020/11/15
"""
from constants.PlaneType import PlaneType
from util.image_processer import *


class Dicom:
    def __init__(self, dicom_files):
        self.dicom_files = dicom_files
        self.is_not_none = False
        if self.dicom_files:
            self.is_not_none = True
        if self.is_not_none:
            # TODO: 这是对于axial 图像的处理，对于其他轴面的图像是否适用，还需要验证
            self.dicom_files.sort(key=lambda x: x.ImagePositionPatient[2])
            # 用于提取公共参数
            self.base_dicom = self.dicom_files[0]
            # 原始切片解剖面
            self.original_plane_type = self.get_original_plane()
            # 各个解剖面图像和坐标信息，plane_info为一个列表，下标对应 PlaneType
            # plane_info的元素为列表--> tuple(position, image)
            self.plane_info = self.build_plane_info()

    def get_original_plane(self):
        """
        获取原始切片的截面方向
        :return:
        """
        image_orientation_patient = self.base_dicom.ImageOrientationPatient
        x_cos = image_orientation_patient[: 3]
        y_cos = image_orientation_patient[3:]
        # 计算图像平面的法向量
        normal_z = np.cross(x_cos, y_cos)
        normal_z_abs = np.abs(normal_z)
        return PlaneType(np.argmax(normal_z_abs))

    def build_plane_info(self):
        """
        建立三个截面的切片和解剖面坐标
        :return:
        """
        column_plane_type, column_orientation_info, row_plane_type, row_orientation_info, layer_orientation_info = \
            self.build_slice()
        # 存储三个解剖面信息，下标与PlaneType 对应
        plane_info = [0, 0, 0]
        if column_plane_type is PlaneType.AXIAL_PLANE:
            plane_info[PlaneType.AXIAL_PLANE.value] = column_orientation_info
        elif row_plane_type is PlaneType.AXIAL_PLANE:
            plane_info[PlaneType.AXIAL_PLANE.value] = row_orientation_info
        elif self.original_plane_type is PlaneType.AXIAL_PLANE:
            plane_info[PlaneType.AXIAL_PLANE.value] = layer_orientation_info

        if column_plane_type is PlaneType.SAGITTAL_PLANE:
            plane_info[PlaneType.SAGITTAL_PLANE.value] = column_orientation_info
        elif row_plane_type is PlaneType.SAGITTAL_PLANE:
            plane_info[PlaneType.SAGITTAL_PLANE.value] = row_orientation_info
        elif self.original_plane_type is PlaneType.SAGITTAL_PLANE:
            plane_info[PlaneType.SAGITTAL_PLANE.value] = layer_orientation_info

        if column_plane_type is PlaneType.CORONAL_PLANE:
            plane_info[PlaneType.CORONAL_PLANE.value] = column_orientation_info
        elif row_plane_type is PlaneType.CORONAL_PLANE:
            plane_info[PlaneType.CORONAL_PLANE.value] = row_orientation_info
        elif self.original_plane_type is PlaneType.CORONAL_PLANE:
            plane_info[PlaneType.CORONAL_PLANE.value] = layer_orientation_info
        return plane_info

    def build_slice(self):
        """
        提取行，列切片图像，以及每一个切片的空间坐标和解剖面类型
        :return:
        """
        # 首先提取图像，组合成一个三维数组
        rows, columns = self.base_dicom.Rows, self.base_dicom.Columns
        layer = len(self.dicom_files)
        pixel_array_3d = np.zeros([rows, columns, layer], dtype=self.base_dicom.pixel_array.dtype)
        for i in range(layer):
            pixel_array_3d[:, :, i] = self.dicom_files[i].pixel_array
        '提取i(列方向)图像'
        # 计算列方向切片的解剖面类型
        column_plane_type = self.get_plane_type(0)
        column_orientation_info = []
        for i in range(columns):
            img = pixel_array_3d[:, i, :]
            img = process_slice_image(img, columns, rows)
            # 计算RCS坐标
            # 对于一个切片，我们需要的是在它的解剖面方向的位置，而在这个切片中的所有voxel，这个位置应该是一样的
            # 提取第i列进行坐标计算
            position = get_rcs(self.base_dicom, 0, i)[column_plane_type.value]
            column_orientation_info.append(Slice(position, img))
        '提取j(行方向)图像'
        row_plane_type = self.get_plane_type(1)
        row_orientation_info = []
        for i in range(rows):
            img = pixel_array_3d[i, :, :]
            img = process_slice_image(img, columns, rows)
            # 计算RCS坐标
            # 对于一个切片，我们需要的是在它的解剖面方向的位置，而在这个切片中的所有voxel，这个位置应该是一样的
            # 提取第i行进行坐标计算
            position = get_rcs(self.base_dicom, i, 0)[row_plane_type.value]
            row_orientation_info.append(Slice(position, img))
        '提取k(层方向)图像'
        # k方向的图像即原始切片图像, 其解剖面方向坐标也可以直接从ImagePositionPatient对应分量中提取
        layer_orientation_info = []
        for each in self.dicom_files:
            layer_orientation_info.append(
                Slice(each.ImagePositionPatient[self.original_plane_type.value], each.pixel_array))
        return column_plane_type, column_orientation_info, row_plane_type, row_orientation_info, layer_orientation_info

    def get_plane_type(self, orientation):
        """
        判断指定的方向的切片的解剖面类型
        :param orientation: {@code 0: i(列方向)}, {@code 1: j(行方向)}， {@code 2: k(层方向)}
        :return:
        """
        # 根据原切片的解剖面，判断i，j, k方向切片的解剖面
        if self.original_plane_type is PlaneType.SAGITTAL_PLANE:
            if orientation is 0:
                return PlaneType.CORONAL_PLANE
            if orientation is 1:
                return PlaneType.AXIAL_PLANE
        if self.original_plane_type is PlaneType.CORONAL_PLANE:
            if orientation is 0:
                return PlaneType.SAGITTAL_PLANE
            if orientation is 1:
                return PlaneType.AXIAL_PLANE
        if self.original_plane_type is PlaneType.AXIAL_PLANE:
            if orientation is 0:
                return PlaneType.SAGITTAL_PLANE
            if orientation is 1:
                return PlaneType.CORONAL_PLANE
        # 层方面就是其自身的切片
        return self.original_plane_type


class Slice:
    """
    表示每一个切片的信息，位置、图像等
    """
    def __init__(self, position, image_data):
        self.data = image_data
        self.position = position


def get_rcs(dicom, row, column):
    """
    通过矩阵变换实现坐标计算
    :param dicom: 需要计算的dicom
    :param row: row index 从0开始
    :param column: column index 从0开始
    :return:
    """
    image_orientation_patient = dicom.ImageOrientationPatient
    image_position_patient = dicom.ImagePositionPatient
    pixel_spacing = dicom.PixelSpacing
    # 变换矩阵, 变换矩阵的元素说明参考：https://dicom.innolitics.com/ciods/ct-image/image-plane/00200037
    m = np.array([[image_orientation_patient[0] * pixel_spacing[1],
                   image_orientation_patient[3] * pixel_spacing[0],
                   0, image_position_patient[0]],
                  [image_orientation_patient[1] * pixel_spacing[1],
                   image_orientation_patient[4] * pixel_spacing[0],
                   0, image_position_patient[1]],
                  [image_orientation_patient[2] * pixel_spacing[1],
                   image_orientation_patient[5] * pixel_spacing[0],
                   0, image_position_patient[2]],
                  [0, 0, 0, 1]])
    image_position_vector = np.array([column, row, 0, 1]).reshape((-1, 1))
    rcs = np.dot(m, image_position_vector)
    return rcs.squeeze()[0:-1]
