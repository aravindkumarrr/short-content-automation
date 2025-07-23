import os
import json

# Define the input JSON file path and output directory
# It's good practice to make this configurable or use a relative path.
# For example, if hooked_stories.json is in the same directory as the script:
# input_json_path = "hooked_stories.json"
input_json_path = r"C:\Users\Aravind Kumar\Desktop\short-form-content-creation\hooked_stories.json"
output_directory = "exports"

def ttfpreprocessing():
    # Create the output directory if it doesn't exist
    try:
        os.makedirs(output_directory, exist_ok=True)
        print(f"Directory '{output_directory}' ensured.")
    except OSError as e:
        print(f"Error creating directory '{output_directory}': {e}")
        exit() # Exit if directory cannot be created

    # Read the JSON file once outside the loop
    stories_data = None # Renamed 'data' to 'stories_data' for clarity
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            stories_data = json.load(f)
        print(f"Successfully loaded data from '{input_json_path}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_json_path}' not found.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_json_path}'. Check file format.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_json_path}': {e}")
        exit()

    # Check if the loaded data is a list and contains dictionaries with expected structure
    if not isinstance(stories_data, list):
        print("Error: JSON data is not a list of stories as expected.")
        exit()

    # Loop through each story in the list and create a separate output file
    for i, story in enumerate(stories_data):
        # Check if each item in the list is a dictionary and has 'hook' and 'body'
        if not isinstance(story, dict) or "hook" not in story or "body" not in story:
            print(f"Warning: Story at index {i} does not contain 'hook' and 'body' keys. Skipping.")
            continue # Skip to the next item if the structure is not as expected

        output_file_name = os.path.join(output_directory, f"story_output_{i}.txt")
        try:
            # Use 'with open' for proper file handling (automatic closing)
            # Use an f-string for dynamic file names
            with open(output_file_name, 'w', encoding='utf-8') as writingfile:
                # Remove leading/trailing double quotes from hook and body
                cleaned_hook = story["hook"].strip('"')
                cleaned_body = story["body"].strip('"')
                content = cleaned_hook + "\n\n" + cleaned_body # Added newlines for better readability
                writingfile.write(content)
            print(f"Content written to '{output_file_name}'.")
        except IOError as e:
            print(f"Error writing to file '{output_file_name}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing story {i}: {e}")

    print("Script finished.")
