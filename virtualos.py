import pickle
from folder import Folder
from file import File

class VirtualOS:
    """
        A virtual file system that simulates basic OS file/folder operations in memory.
    """
    def __init__(self):
        """Initialize the VirtualOS with a root folder."""
        self.root = Folder("root")
        self.current_folder = self.root


    def _resolve_path(self, path):
        """
            Convert a given path (absolute or relative) into a Folder object.
            Supports '.', '..', and 'root/...'.
        """
        if not path or path == ".":
            return self.current_folder

        parts = path.split("/")
        if parts[0] == "root":
            folder = self.root
            parts = parts[1:]
        else:
            folder = self.current_folder

        for part in parts:
            if part == ".":
                continue
            elif part == "..":
                if folder.parent is not None:
                    folder = folder.parent
            else:
                folder = folder.get_child(part)
                if not isinstance(folder, Folder):
                    raise NotADirectoryError(f"'{part}' is not a folder")
        return folder


    def cd(self, path):
        """Change the current working folder."""        
        folder = self._resolve_path(path)
        self.current_folder = folder


    def ls(self, path=None):
        """List the contents of the given folder (or current folder if None)."""
        folder = self._resolve_path(path)
        return folder.list_children()


    def cat(self, path):
        """
            Display the content of a file.
            If the file is protected, prompt for a password.
        """
        parts = path.split("/")
        file_name = parts[-1]
        folder_path = "/".join(parts[:-1]) if len(parts) > 1 else "."

        folder = self._resolve_path(folder_path)
        file_obj = folder.get_child(file_name)

        if not isinstance(file_obj, File):
            raise TypeError(f"'{file_name}' is not a file.")

        if file_obj.is_protected:
            password = input(f"Enter password for '{file_name}': ")
            return file_obj.read(password=password)
        else:
            return file_obj.read()


    def _copy_or_move(self, src_path, dest_path, move=False):
        """
            Internal helper for copying or moving files.
            If move=True, the source file is removed after copying.
        """
        # Resolve source        
        src_parts = src_path.split("/")
        src_name = src_parts[-1]
        src_folder_path = "/".join(src_parts[:-1]) if len(src_parts) > 1 else "."
        src_folder = self._resolve_path(src_folder_path)
        src_file = src_folder.get_child(src_name)

        if not isinstance(src_file, File):
            raise TypeError(f"'{src_name}' is not a file.")

        if src_file.is_protected:
            password = input(f"Enter password for '{src_name}': ")
            src_file._check_password(password)
        else:
            password = None

        # Resolve destination
        dest_parts = dest_path.split("/")
        dest_name = dest_parts[-1]
        dest_folder_path = "/".join(dest_parts[:-1]) if len(dest_parts) > 1 else "."
        dest_folder = self._resolve_path(dest_folder_path)

        if not isinstance(dest_folder, Folder):
            raise NotADirectoryError(f"Destination '{dest_folder.name}' is not a folder.")

        # If destination exists, overwrite content
        if dest_folder.has_children(dest_name):
            dest_file = dest_folder.get_child(dest_name)
            if not isinstance(dest_file, File):
                raise TypeError(f"Destination '{dest_name}' is not a file.")
            dest_file.write(src_file.read(password))
        else:
            # Create a new file with copied content
            new_file = File(dest_name, src_file.content.copy())
            dest_folder.add_child(new_file)

        # Remove source if move=True
        if move:
            src_folder.remove_child(src_name)


    def cp(self, src_path, dest_path):
        """Copy a file from source to destination."""
        self._copy_or_move(src_path, dest_path, move=False)


    def mv(self, src_path, dest_path):
        """Move a file from source to destination."""
        self._copy_or_move(src_path, dest_path, move=True)


    def rm(self, path):
        """Remove a file or folder."""        
        parts = path.split("/")
        item_name = parts[-1]
        folder_path = "/".join(parts[:-1]) if len(parts) > 1 else "."

        folder = self._resolve_path(folder_path)
        item = folder.get_child(item_name)

        if isinstance(item, File) and item.is_protected:
            password = input(f"Enter password for '{item_name}': ")
            item._check_password(password)

        folder.remove_child(item_name)
        print(f"'{item_name}' removed successfully.")


    def mkdir(self, path, name=None):
        """Create a new folder."""
        if name is None:
            target_folder = self.current_folder
            folder_name = path
        else:
            target_folder = self._resolve_path(path)
            folder_name = name

        if not isinstance(target_folder, Folder):
            raise NotADirectoryError(f"Destination '{target_folder.name}' is not a folder.")

        new_folder = Folder(folder_name)
        target_folder.add_child(new_folder)


    def rename(self, path, new_name):
        """
            Rename a file or folder to a new name.

            :param path: Path to the item to rename (absolute or relative)
            :param new_name: The new name for the item
        """        
        parts = path.split("/")
        old_name = parts[-1]
        folder_path = "/".join(parts[:-1]) if len(parts) > 1 else "."

        folder = self._resolve_path(folder_path)
        item = folder.get_child(old_name)

        if folder.has_children(new_name):
            raise ValueError(f"An item named '{new_name}' already exists in folder '{folder.name}'")

        item.name = new_name
        print(f"Renamed '{old_name}' to '{new_name}' successfully.")


    def search(self, keyword, start_path="."):
        """
            Search for files or folders by keyword starting from a given path.

            :param keyword: Search term (can be part of a name or file extension starting with '.')
            :param start_path: Path to start searching from (default is current folder)
            :return: List of matching paths
         """ 
        start_folder = self._resolve_path(start_path)
        if not isinstance(start_folder, Folder):
            raise NotADirectoryError(f"'{start_path}' is not a folder.")

        results = []

        def _recursive_search(folder, current_path):
            """Recursively search through all subfolders."""            
            for child in folder.children:
                full_path = f"{current_path}/{child.name}"

                # Match by extension if keyword starts with '.'            
                if keyword.startswith(".") and isinstance(child, File) and child.name.endswith(keyword):
                    results.append(full_path)
                # Match by name (case-insensitive)
                elif keyword.lower() in child.name.lower():
                    results.append(full_path)

                # Continue searching in subfolders
                if isinstance(child, Folder):
                    _recursive_search(child, full_path)

        _recursive_search(start_folder, start_path if start_path != "." else self.current_folder.name)
        return results


    def fragment(self, filename):
        """
            Remove empty lines from a real file on disk (not a virtual file).

            :param filename: Name of the file on the real filesystem
        """    
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Keep only non-empty lines        
            cleaned_lines = [line for line in lines if line.strip() != ""]

            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(cleaned_lines)

            print(f"File '{filename}' fragmented successfully. Removed {len(lines) - len(cleaned_lines)} empty lines.")

        except FileNotFoundError:
            print(f"File '{filename}' not found.")


    def save_to_file(self, filename):
        """
            Save the entire virtual file system to a binary file using pickle.

            :param filename: Name of the file to save the system state
        """
        with open(filename, "wb") as f:
            pickle.dump(self.root, f)
        print(f"System saved to '{filename}' successfully.")


    def load_from_file(self, filename):
        """
            Load the virtual file system state from a binary file created by save_to_file().

            :param filename: Name of the file to load the system state from
        """
        with open(filename, "rb") as f:
            self.root = pickle.load(f)
        self.current_folder = self.root
        print(f"System loaded from '{filename}' successfully.")


    def edit_file_line(self, path, index, new_text):
        """
            Edit a specific line in a file.

            :param path: Path to the file
            :param index: Line index to edit (0-based)
            :param new_text: New text to replace the line
        """

        parts = path.split("/")
        file_name = parts[-1]
        folder_path = "/".join(parts[:-1]) if len(parts) > 1 else "."

        folder = self._resolve_path(folder_path)
        file_obj = folder.get_child(file_name)

        if not isinstance(file_obj, File):
            raise TypeError(f"'{file_name}' is not a file.")

        if file_obj.is_protected:
            password = input(f"Enter password for '{file_name}': ")
            file_obj.edit_line(index, new_text, password=password)
        else:
            file_obj.edit_line(index, new_text)

        print(f"Line {index} in '{file_name}' updated successfully.")


    def delete_file_line(self, path, index):
        """
            Delete a specific line from a file.

            :param path: Path to the file
            :param index: Line index to delete (0-based)
        """

        parts = path.split("/")
        file_name = parts[-1]
        folder_path = "/".join(parts[:-1]) if len(parts) > 1 else "."

        folder = self._resolve_path(folder_path)
        file_obj = folder.get_child(file_name)

        if not isinstance(file_obj, File):
            raise TypeError(f"'{file_name}' is not a file.")

        # Check password if file is protected
        if file_obj.is_protected:
            password = input(f"Enter password for '{file_name}': ")
            file_obj.delete_line(index, password=password)
        else:
            file_obj.delete_line(index)

        print(f"Line {index} in '{file_name}' deleted successfully.")

