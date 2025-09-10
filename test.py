from file import File
from folder import Folder 
from virtualos import VirtualOS

def run_all_tests():
    os = VirtualOS()

    print("\n=== 1. Test mkdir , ls ===")
    os.mkdir("docs")
    os.mkdir("docs", "images")
    print("Root:", os.ls())  # ['docs']
    print("Docs:", os.ls("docs"))  # ['images']

    print("\n=== 2. Test cd ===")
    os.cd("docs")
    print("Current folder:", os.current_folder.name)  # docs
    os.cd("images")
    print("Current folder:", os.current_folder.name)  # images
    os.cd("..")
    print("Back to:", os.current_folder.name)  # docs
    os.cd("..")
    print("Back to:", os.current_folder.name)  # root

    print("\n=== 3. Test create file , cat ===")
    notes = File("notes.txt", ["Hello", "World"])
    secret = File("secret.txt", ["Top Secret"], is_protected=True, password="1234") # This is Password
    os.root.add_child(notes)
    os.root.add_child(secret)
    print("Notes content:\n", os.cat("notes.txt"))
    # For testing the protected file, enter the correct password
    # print("Secret content:\n", os.cat("secret.txt"))

    print("\n=== 4. Test edit_file_line , delete_file_line ===")
    os.edit_file_line("notes.txt", 1, "Python")
    print("After edit:\n", os.cat("notes.txt"))
    os.delete_file_line("notes.txt", 0)
    print("After delete:\n", os.cat("notes.txt"))

    print("\n=== 5. Test rename ===")
    os.rename("notes.txt", "my_notes.txt")
    print("After rename:", os.ls())

    print("\n=== 6. Test cp , mv ===")
    os.mkdir("backup")
    os.cp("my_notes.txt", "backup/notes_copy.txt")
    print("Backup folder after cp:", os.ls("backup"))
    os.mv("secret.txt", "backup/secret_moved.txt")
    print("Backup folder after mv:", os.ls("backup"))
    print("Root after mv:", os.ls())

    print("\n=== 7. Test rm ===")
    os.rm("my_notes.txt")
    print("Root after rm:", os.ls())

    print("\n=== 8. Test search ===")
    print("Search '.txt':", os.search(".txt"))
    print("Search 'secret':", os.search("secret"))

    print("\n=== 9. Test save_to_file , load_from_file ===")
    os.save_to_file("system_data.pkl")
    new_os = VirtualOS()
    new_os.load_from_file("system_data.pkl")
    print("Loaded system:", new_os.ls())

    print("\n=== 10. Test fragment (on a sample text file) ===")
    with open("sample_text.txt", "w", encoding="utf-8") as f:
        f.write("Line 1\n\nLine 2\n\nLine 3\n")
    os.fragment("sample_text.txt")
    with open("sample_text.txt", "r", encoding="utf-8") as f:
        print("Fragmented file content:\n", f.read())

if __name__ == "__main__":
    run_all_tests()
