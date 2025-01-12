# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

## Installation

1. Clone the repository:
  ```bash
    git clone git@github.com:LeandroAlves05/take-home-project.git
    cd take-home-project/
  ```

2. Make sure Python is installed: 
  ```bash
    python --version
  ```

3. Optional: Create and activate a virtual environment:
  ```bash
    python -m venv venv
  ```
  ```bash
    # For macOS/Linux
    source venv\Scripts\activate
    # For Windows
    source venv/bin/activate
  ```

## Usage

The script supports two main commands through CLI: **index** and **search**

#### 1. Index Files
Creates an index of all files in a directory and saves it to `index.json`
  ```bash
    python main.py index <directory-path>
  ```
  - Example:
    ```bash
      python main.py index test_data
    ```

#### 2. Search Files
Searches for files in the index based on name, size, and/or content type

**Search by Name**
  ```bash
    python main.py search <filename>
  ```
  - Example:
    ```bash
      python main.py search user1.json
    ```

**Search by Size**
  ```bash
    python main.py search "" --size <size-in-bytes>
  ```
  - Example:
    ```bash
      python main.py search "" --size 4567
    ```

**Search by Type**
  ```bash
    python main.py search "" --type <mime-type>
  ```
  - Example:
    ```bash
      python main.py search "" --type image/jpeg
    ```

**Combining Criteria**
You can combine the file criteria for a more specific search
  ```bash
    python main.py search <partial-name> --size <size-in-bytes> --type <mime-type>
  ```
  - Example:
    ```bash
      python main.py search sample --type application/pdf
    ```

## Index File Format
The generated `index.json` file is a JSON array of objects, where each object represents a file in the index. Each object has the following properties:

- `name`: The name of the file.
- `path`: The absolute path to the file.
- `size_bytes`: The size of the file in bytes.
- `type`: The MIME type of the file.

Here's an example of what the `index.json` file might look like:

```bash
  [
    {
      "name": "user1.json",
      "path": "test_data/data/user1.json",
      "size": 123,
      "type": "application/json"
    },
    {
      "name": "linear-regression-plot.jpg",
      "path": "test_data/linear-regression-plot.jpg",
      "size": 4567,
      "type": "image/jpeg"
    }
  ]
```
