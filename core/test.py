import os

def update_env_file(key, new_value, file_path='../.env'):
    # Read the contents of the .env file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Update the value for the specified key
    for i, line in enumerate(lines):
        if line.startswith(key + '='):
            lines[i] = f"{key}={new_value}\n"
            break
    else:
        # If the key doesn't exist, add it to the end of the file
        lines.append(f"{key}={new_value}\n")

    # Write the updated contents back to the .env file
    with open(file_path, 'w') as f:
        f.writelines(lines)

# Example usage
update_env_file('API_KEY', 'new_values')
