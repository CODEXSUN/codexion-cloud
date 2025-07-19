Here's how to **use your `filegenerator.py`** in various scenarios:

---

### ✅ 1. **Interactive Mode**

You can allow a user to interactively create a file by calling:

```python
from commands.utils.filegenerator import generate_interactive

generate_interactive()
```

**What it does:**

* Prompts the user for:

  * File name (no extension)
  * File type (from `.py`, `.md`, `.env`, etc.)
  * Folder path
  * Optional file content
* Creates the file with:

  * Header including author, timestamp, and file path

---

### ✅ 2. **Single File Programmatically**

To generate a file from code directly:

```python
from pathlib import Path
from commands.utils.filegenerator import generate_file

generate_file(Path("backend/main.py"), content="print('Hello from main')", overwrite=True)
```

**Output:**

```
✅ Created: backend/main.py
```

---

### ✅ 3. **Multiple Files at Once**

To generate many files in one go:

```python
from commands.utils.filegenerator import generate_multiple_files

generate_multiple_files([
    {
        "name": "main",
        "path": "backend",
        "extension": ".py",
        "content": "print('Hello World')"
    },
    {
        "name": "README",
        "path": ".",
        "extension": ".md",
        "content": "# Project Title\n\nDescription goes here."
    },
    {
        "name": ".env",
        "path": ".",
        "extension": "",
        "content": "SECRET_KEY=your_key_here"
    },
    {
        "name": "requirements",
        "path": ".",
        "extension": ".txt",
        "content": "fastapi\nuvicorn"
    }
])
```

---

### 📌 Notes

* If a file already exists, it will **skip** unless `overwrite=True` is passed.
* The header inside the file contains:

  * File path
  * Created timestamp
  * Author (from `getpass.getuser()`)

---
