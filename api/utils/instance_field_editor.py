class InstanceFieldEditor:
    def __init__(self, instance):
        self.instance = instance

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self.instance, key, value)
