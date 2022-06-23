from property_functions import pfunc


class SheetObject:

    def __init__(self, name, descr, proplist=None, *args, **kwargs,):
        self.name = name
        self.description = descr
        [self.apply_prop(prop) for prop in proplist]

    def apply_prop(self, prop):
        pfunc[prop](self)


class character(SheetObject):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.image = kwargs["character_image"]
        self.gear = {}


class skill(SheetObject):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.stat = kwargs["stat"]
        self.rank = kwargs["rank"]

    def get_pool(self):
        maxpool = max(self.stat.value, self.rank)
        minpool = min(self.stat.value, self.rank)
        proficiency = "c"*minpool
        attribute = "a"*(maxpool-minpool)
        return f"{proficiency}{attribute}"