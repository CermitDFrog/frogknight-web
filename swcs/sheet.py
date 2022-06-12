from property_functions import pfunc


class SheetObject:

    def __init__(self,name, descr, proplist=None, *args, **kwargs,):
        self.name = name
        self.description = descr
        self.extendedinit(*args, **kwargs)
        
        # Always Last.
        [self.apply_prop(prop) for prop in proplist]

    def apply_prop(self, prop):
        pfunc[prop](self)

    def extendedinit(self,*args, **kwargs):
        pass


class character(SheetObject):
    def extendedinit(self,*args, **kwargs):
        pass


class skill(SheetObject):
    def extendedinit(self,*args, **kwargs):
        pass
