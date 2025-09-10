class File:
    """
        Represents a virtual file in the VirtualOS.
        Stores content as a list of lines and supports optional password protection.
    """
    def __init__(self, name, content=None, is_protected=False, password=None):
        self.name = name
        self.content = content if content is not None else [] # Store file content as list of lines
        self.is_protected = is_protected
        self.password = password if is_protected else None
        """
            Initialize a File object.

            :param name: Name of the file
            :param content: Initial content (list of strings or None)
            :param is_protected: Whether the file is password-protected
            :param password: Password for the file (only if is_protected=True)
        """

    def _check_password(self, password):
        """
            Internal helper to verify the password for protected files.
            Raises PermissionError if the password is incorrect.
        """
        if self.is_protected and self.password != password:
            raise PermissionError("Incorrect password for protected file.")


    def read(self, password = None):
        """
            Return the file content as a single string.
            Requires password if the file is protected.
        """        
        self._check_password(password)
        return '\n'.join(self.content)


    def write(self, lines, password = None):
        """
            Overwrite the file content with new lines.
            Accepts either a string (split into lines) or a list of strings.
        """        
        self._check_password(password)
        if isinstance(lines, str):
            lines = lines.split("\n")
        self.content = lines


    def append_line(self, line, password=None):
        """
            Append a single line to the end of the file.
        """        
        self._check_password(password)
        self.content.append(line)


    def edit_line(self,index, new_text, password = None):
        """
            Replace the content of a specific line by index.
            Raises IndexError if the index is out of range.
        """        
        self._check_password(password)
        if 0 <= index < len(self.content):
            self.content[index] = new_text
        else:
            raise IndexError("Line index out of range.")



    def delete_line(self, index, password = None):
        """
            Delete a specific line from the file by index.
            Raises IndexError if the index is out of range.
        """        
        self._check_password(password)
        if 0 <= index < len(self.content):
            del self.content[index]
        else:
            raise IndexError("Line index out of range.")

        

