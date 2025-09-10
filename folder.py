class Folder:
    """
        Represents a virtual folder in the VirtualOS.
        Can contain both File and Folder objects as children.
    """
    def __init__(self, name, parent=None):
        """
            Initialize a Folder object.

            :param name: Name of the folder
            :param parent: Parent Folder object (None for root)
        """  
        self.name = name
        self.parent = parent
        self.children = [] # List of File or Folder objects
      

    def has_children(self, name):
        """
            Check if a child with the given name exists in this folder.

            :param name: Name of the child to check
            :return: True if a child with the given name exists, False otherwise
        """
        return any(child.name == name for child in self.children)

    def add_child(self, child):
        """
            Add a File or Folder object as a child of this folder.

            :param child: File or Folder object to add
            :raises ValueError: If a child with the same name already exists
        """        
        if self.has_children(child.name):
            raise ValueError(f"An item named '{child.name}' already exists in folder '{self.name}")
        child.parent = self  # Set this folder as the parent of the child
        self.children.append(child)

    def get_child(self, name):
        """
            Retrieve a child object by name.

            :param name: Name of the child to retrieve
            :return: The File or Folder object with the given name
            :raises FileNotFoundError: If no child with the given name exists
        """        
        for child in self.children:
            if child.name == name:
                return child
        raise FileNotFoundError(f"No item named '{name}' found in folder '{self.name}'")


    def remove_child(self, name):
        """
            Remove a child object by name.

            :param name: Name of the child to remove
            :raises FileNotFoundError: If no child with the given name exists
        """        
        for i, child in enumerate(self.children):
            if child.name == name:
                del self.children[i]
                return
        raise FileNotFoundError(f"No item named '{name}' to remove from folder '{self.name}'")

    def list_children(self):
        """
            List the names of all children in this folder.

            :return: List of child names (empty list if no children)
        """
        if not self.children:
            return []
        return [child.name for child in self.children]





