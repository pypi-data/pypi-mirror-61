class DataBuffer:

    def __init__(self, data, schema, rel=True, exclusions=None):
        self.object = True
        self.relationships = rel
        self.showrefs(rel)
        if isinstance(data, list):
            self.object = False
        self.schema = schema
        self.data = data
        self.exclusions = exclusions or list()
        self.include = list(map(lambda sch: sch.get('key'), self.schema))

    def schema(self):
        return self.schema

    def name(self):
        return str(self.data)

    def showrefs(self, value=True):
        """
        Set the model references value. References are backref and relationships on Alchemy model instances
        :param value: boolean True / False
        :return: self
        :rtype: DataBuffer
        """

        self.relationships = value
        return self

    def __instance_prep(self, instance, exclude):
        if not exclude:
            exclude = []
        if isinstance(instance, tuple):
            return instance[0].serialize(
                rel=self.relationships,
                exc=exclude
            )
        return instance.serialize(
            rel=self.relationships,
            exc=exclude
        )

    def json(self, exclude=None):
        if not exclude:
            exclude = list()
        elif exclude and not hasattr(exclude, '__iter__'):
            raise ValueError('Cannot use exclusions that are not in a collection')

        exclude = exclude + self.exclusions
        
        if isinstance(self.data, list):
            pass

        if self.data is None:
            return list()

        if self.object:
            return self.__instance_prep(self.data, exclude)
        return [self.__instance_prep(entry, exclude) for entry in self.data]

    def view(self):
        return self.data

    def __iter__(self):
        return iter(self.data)
