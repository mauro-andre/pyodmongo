class DbField:
    def __init__(self):
        self.field_name = None
        self.field_alias = None
        self.path_str = None
        # self.annotation = None
        self.by_reference = None
        self.is_list = None
        self.is_union = None
        self.types = []
        # self.has_model_fields = None

    def __repr__(self):
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"DbField({attrs_str})"

    def __eq__(self, value) -> dict:
        if isinstance(value, DbField):
            return super().__eq__(value)
        return {self.path_str: {"$eq": value}}
