class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def has_children(self, name):
        return any(child.name == name for child in self.children)

    def add_child(self, child):
        if self.has_children(child.name):
            raise ValueError(f"An item named '{child.name}' already exists in folder '{self.name}")
        child.parent = self
        self.children.append(child)

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        raise FileNotFoundError(f"No item named '{name}' found in folder '{self.name}'")


    def remove_child(self, name):
        for i, child in enumerate(self.children):
            if child.name == name:
                del self.children[i]
                return
        raise FileNotFoundError(f"No item named '{name}' to remove from folder '{self.name}'")

    def list_children(self):
        if not self.children:
            return []
        return [child.name for child in self.children]





