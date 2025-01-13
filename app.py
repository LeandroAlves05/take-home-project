import os
import json
import mimetypes
import sys


def create_index(directory, output_file="index.json"):
    index = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            stat = os.stat(file_path)
            file_type = mimetypes.guess_type(file_path)[0]
            index.append(
                {
                    "name": file,
                    "path": file_path,
                    "size_bytes": stat.st_size,
                    "type": file_type,
                }
            )
    with open(output_file, "w") as file:
        json.dump(index, file, indent=2)
    print(f"Index created: {output_file}")


def search_index(
    index_file, filename=None, size_min=None, size_max=None, file_type=None
):
    with open(index_file, "r") as file:
        index = json.load(file)

    results = []
    for entry in index:
        if filename and filename.lower() not in entry["name"].lower():
            continue
        if size_min is not None and entry["size_bytes"] < size_min:
            continue
        if size_max is not None and entry["size_bytes"] > size_max:
            continue
        if file_type and entry["type"] != file_type:
            continue
        results.append(entry)

    if results:
        print(f"Found {len(results)} results:")
        for result in results:
            print(
                f"- {result['name']} ({result['size_bytes']} bytes, {result['type']}) at {result['path']}"
            )
    else:
        print("No results found.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  To index: python main.py index <directory>\n"
            "  To search: python main.py search [--filename NAME] [--size-min SIZE] [--size-max SIZE] [--type TYPE]"
        )
        sys.exit(1)

    command = sys.argv[1]
    if command == "index" and len(sys.argv) == 3:
        directory = sys.argv[2]
        create_index(directory)
    elif command == "search":
        filename = None
        size_min = None
        size_max = None
        file_type = None

        if "--filename" in sys.argv:
            filename_index = sys.argv.index("--filename") + 1
            filename = sys.argv[filename_index]
        if "--size-min" in sys.argv:
            size_min_index = sys.argv.index("--size-min") + 1
            size_min = int(sys.argv[size_min_index])
        if "--size-max" in sys.argv:
            size_max_index = sys.argv.index("--size-max") + 1
            size_max = int(sys.argv[size_max_index])
        if "--type" in sys.argv:
            type_index = sys.argv.index("--type") + 1
            file_type = sys.argv[type_index]

        search_index(
            "index.json",
            filename=filename,
            size_min=size_min,
            size_max=size_max,
            file_type=file_type,
        )
    else:
        print("Invalid usage. See instructions.")
