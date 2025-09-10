class File:
    def __init__(self, name, content=None, is_protected=False, password=None):
        self.name = name
        self.content = content if content is not None else []
        self.is_protected = is_protected
        self.password = password if is_protected else None

    def _check_password(self, password):
        if self.is_protected and self.password != password:
            raise PermissionError("Incorrect password for protected file.")


    def read(self, password = None):
        self._check_password(password)
        return '\n'.join(self.content)


    def write(self, lines, password = None):
        self._check_password(password)
        if isinstance(lines, str):
            lines = lines.split("\n")
        self.content = lines


    def append_line(self, line, password=None):
        self._check_password(password)
        self.content.append(line)


    def edit_line(self,index, new_text, password = None):
        self._check_password(password)
        if 0 <= index < len(self.content):
            self.content[index] = new_text
        else:
            raise IndexError("Line index out of range.")



    def delete_line(self, index, password = None):
        self._check_password(password)
        if 0 <= index < len(self.content):
            del self.content[index]
        else:
            raise IndexError("Line index out of range.")

        

