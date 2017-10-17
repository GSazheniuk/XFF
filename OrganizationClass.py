class Organization:
    def __init__(self, name):
        self.Name = name
        pass
    def toJSON(self):
        res = '{'
        res += '"Name": "%s"' % self.Name
        res += '}'
        return res
