class Visibility():

    def __init__(self):
        self.internal_fieldname = None
        self.page_name = None
        self.external_page_name = None
        self.order_number = None
        self.external_fieldname = None
        self.field_type = None
        self.enum_name = None

    def __init__(self, internal_fieldname, page_name, external_page_name, order_number, external_fieldname, field_name, enum_name):
        self.internal_fieldname = internal_fieldname
        self.page_name = page_name
        self.external_page_name = external_page_name
        self.order_number = order_number
        self.external_fieldname = external_fieldname
        self.field_type = field_name
        self.enum_name = enum_name