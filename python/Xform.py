import numpy as np


class Xform2D:
    def __init__(self, xform_origin:Point2D=Point2D(0,0)):
        self._xform_origin = Point
    def __setOrigin(self, p:Point2D)->None:
        self._xform_origin = p
    def __getOrigin(self)->Point2D:
        return self._xform_origin
    xf_origin = property(self.__getOrigin, self.__setOrigin, None, 'The origin point for the xform')
    #adjust data depending on origin point
    def __formatData(self, data)->np.ndarray:
        if self.xf_origin == Point2D(0,0):
            return data
        else: #TODO: adjust the data
            return data
    def xform(self, xform:np.array, data:np.ndarray):
        assert xform.shape==(2,2), f'xform shape is: {xform.shape}, but xform needs to have exact shape (2,2).'
        assert data.shape(0)==2, f'data shape is: {data.shape}, but must have exactly 2 rows.'
        data = self.__formatData(data)
        return np.matmul(xform, data)
