import json


def remove_ids(data):
    """Removes the 'id' key from a dictionary or list of dictionaries.

    Args:
      data: A dictionary or list of dictionaries.

    Returns:
      The modified data with the 'id' key removed.
    """
    if isinstance(data, dict):
        if "id" in data:
            del data["id"]
        for key, value in data.items():
            data[key] = remove_ids(value)
    elif isinstance(data, list):
        for item in data:
            remove_ids(item)
    return data


# Load the JSON data from a file or string
with open("parsegames.json", "r") as f:
    data = json.load(f)

# Remove the 'id' keys
modified_data = remove_ids(data)

# Print the modified JSON data
print(json.dumps(modified_data, indent=2))
with open("newgames.json", "t+w") as f:
    f.write(json.dumps(modified_data, indent=2))
