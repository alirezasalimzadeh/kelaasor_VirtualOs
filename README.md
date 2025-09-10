# 💾 VirtualOS

A lightweight **virtual file system** in Python — create, read, edit, move, copy, search, and protect files & folders, all in memory.  
Think of it as your own **mini OS** without touching the real disk.

## ✨ Features
- 📂 Create & navigate folders (`mkdir`, `cd`, `ls`)
- 📄 Create, read, edit, and delete files
- 🔒 Password-protected files
- 📦 Copy / move / rename / remove
- 🔍 Search by name or extension
- 💾 Save & load the entire system state


## 🛠 How It Works
- 🧠 All files and folders exist **in memory** as Python objects .
- 📍 Supports both **absolute paths** (`root/...`) and **relative paths** (`./`, `../`) for navigation.
- 🔐 Files can be **password-protected**, blocking read or edit access without the correct key.
- 💾 The entire virtual file system can be **saved** to a binary file and **restored** later using Python’s `pickle` module.


## 🚀 Quick Start
```python
from virtualos import VirtualOS

# Initialize the virtual OS
os = VirtualOS()

# Create and navigate into a folder
os.mkdir("projects")
os.cd("projects")

# Create a file and write content
from file import File
myfile = File("notes.txt", ["Hello World"])
os.current_folder.add_child(myfile)

# List current folder contents
print(os.ls())  # ['notes.txt']

# Read file content
print(os.cat("notes.txt"))
