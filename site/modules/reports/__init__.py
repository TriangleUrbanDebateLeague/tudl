class BaseReport(object):
    args = []
    columns = []

    def __init__(self, **params):
        for param, value in self.args:
            if param not in args:
                raise NameError("{} is not a valid parameter for the report".format(param))
            setattr(self, param, value)

    def get_data(self):
        raise Exception("not implemented")

    def get_columnar_data(self):
        fields = [_[0] for _ in self.columns]
        data = [[_[1] for _ in self.columns]]
        for record in self.get_data():
            data.append([getattr(record, field) for _, field in self.columns])
        return data
