import source.registry as reg

class BaseInstance:
    def __init__(self, name, dataType):
        self.dataType = dataType
        self.name = name
        reg.add(dataType, name, self)
    def destroy(self):
        reg.remove(self.dataType, self.name)
    def __del__(self):
        try:
            self.destroy()
        except:
            pass