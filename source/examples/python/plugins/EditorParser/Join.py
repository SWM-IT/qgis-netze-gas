class Join:

    def __init__(self):
        self.own_table = None
        self.own_field = None
        self.foreign_table = None
        self.foreign_field = None
        self.external_name = None


    def __init__(self, own_table, own_field, foreign_table, foreign_field, external_name):
        self.own_table = own_table
        self.own_field = own_field
        self.foreign_table = foreign_table
        self.foreign_field = foreign_field
        self.external_name = external_name