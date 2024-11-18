from Shape import _Shape

class ShapeContainer:
    def __init__(self):
        #keys=str id, #vals=[list of shapes]
        self._shapes:dict = {}
    def translate(self, dx, dy)->None:
        for key, shape_list in self._shapes:
            for s in shape_list:
                s.translate(dx, dy)
    def scale(self, sf)->None:
        for key, shape_list in self._shapes:
            for s in shape_list:
                s.scale(sf)
    #TODO: check if s is in shape list. Need to be able to univerally compare shapes.
    # Maybe add a type check into each shapes __eq__ function.
    def addShape(self, shape_id:str, shape:_Shape)->None:
        if not shape_id in self.shapes.keys():
            self._shapes[shape_id] = []
        if s in self.shapes[shape_id]:
            return 
        self._shapes[shape_id].append(shape)
    def removeShape(self):
        pass
    #TODO: add bbox
    def __getShapes(self)->dict:
        return self._shapes
    def __getBbox(self)->None:
        return None
    shapes = property(__getShapes, None, None, 'shape dictionary with all the sahpes')
    bbox = property(__getBbox, None, None, 'bbox surrounding all the shapes in container')
