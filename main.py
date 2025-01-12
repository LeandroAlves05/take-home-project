import os
import json
import mimetypes
import sys


def create_index(directory, output_file="index.json"):
    index = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_type = mimetypes.guess_type(file_path)[0]
            index.append(
                {
                    "name": file,
                    "path": file_path,
                    "size_bytes": file_size,
                    "type": file_type,
                }
            )
    with open(output_file, "w") as file:
        json.dump(index, file, indent=2)
    print(f"Index created: {output_file}")


def search_index(index_file, query=None, size=None, file_type=None):
    with open(index_file, "r") as file:
        index = json.load(file)
    results = [
        entry
        for entry in index
        if (query.lower() in entry["name"].lower() if query else True)
        and (entry["size_bytes"] == size if size else True)
        and (entry["type"] == file_type if file_type else True)
    ]
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
            "  To search: python main.py search <query> [--size SIZE] [--type TYPE]"
        )
        sys.exit(1)

    command = sys.argv[1]
    if command == "index" and len(sys.argv) == 3:
        directory = sys.argv[2]
        create_index(directory)
    elif command == "search":
        if len(sys.argv) < 3:
            print("Provide a query or filter for search.")
            sys.exit(1)
        query = sys.argv[2] if sys.argv[2] != '""' else None
        size = None
        file_type = None
        if "--size" in sys.argv:
            size_index = sys.argv.index("--size") + 1
            size = int(sys.argv[size_index])
        if "--type" in sys.argv:
            type_index = sys.argv.index("--type") + 1
            file_type = sys.argv[type_index]
        search_index("index.json", query=query, size=size, file_type=file_type)
    else:
        print("Invalid usage. See instructions.")
