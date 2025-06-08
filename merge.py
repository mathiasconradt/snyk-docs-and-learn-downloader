import os

def merge_markdown_files(file1_name, file2_name, output_file_name):
    """
    Merges the content of two Markdown files into a new single Markdown file.

    Args:
        file1_name (str): The name of the first Markdown file to merge.
        file2_name (str): The name of the second Markdown file to merge.
        output_file_name (str): The name of the output merged Markdown file.
    """
    try:
        # Check if the input files exist
        if not os.path.exists(file1_name):
            print(f"Error: The file '{file1_name}' was not found in the current directory.")
            return
        if not os.path.exists(file2_name):
            print(f"Error: The file '{file2_name}' was not found in the current directory.")
            return

        # Read content of the first file
        with open(file1_name, 'r', encoding='utf-8') as f1:
            content1 = f1.read()

        # Read content of the second file
        with open(file2_name, 'r', encoding='utf-8') as f2:
            content2 = f2.read()

        # Define a separator to clearly distinguish content from each file
        separator = "\n\n---\n\n" \
                    "<!-- Content from " + os.path.basename(file2_name) + " starts here -->\n\n"

        # Write the combined content to the output file
        with open(output_file_name, 'w', encoding='utf-8') as outfile:
            outfile.write(content1)
            outfile.write(separator)
            outfile.write(content2)

        print(f"Successfully merged '{file1_name}' and '{file2_name}' into '{output_file_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the file names
file_one = "snyk-docs.md"
file_two = "snyk-learn.md"
output_file = "snyk-docs-and-learn.md"

# Call the function to merge the files
merge_markdown_files(file_one, file_two, output_file)
