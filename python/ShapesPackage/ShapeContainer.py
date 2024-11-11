from Shape import _Shape

class ShapeContainer:
    def __init__(self, sl:list=None):
        self._shape_list = []
        if sl is None: return 
        for s in sl:
            self.addShape(s)
    def translate(self, dx, dy)->None:
        for s in self._shape_list:
            s.translate(dx, dy)
#    def moveTo(self, xpos, ypos)->None:
#        for s in self._shape_list:
#            s.moveTo(xpos, ypos)
    def scale(self, sf)->None:
        for s in self._shape_list:
            s.scale(sf)
    #TODO: check if s is in shape list. Need to be able to univerally compare shapes.
    # Maybe add a type check into each shapes __eq__ function.
    def addShape(self, s:_Shape)->None:
        if s in self._shape_list:
            return 
        self._shape_list.append(s)
    def removeShape(self, s:_Shape)->None:
        if not(s in self._shape_list):
            return 
        self._shape_list.remove(s)
    #TODO: add bbox
    def __getBbox(self):
        return None
    bbox = property(__getBbox, None, None, 'bbox surrounding all the shapes in container')
