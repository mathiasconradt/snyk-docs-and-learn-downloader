import requests
from bs4 import BeautifulSoup
import html2text
import os

def fetch_and_convert_snyk_lessons():
    """
    Fetches Snyk lessons, extracts content from their URLs,
    converts it to Markdown, and saves it as .md files.
    """
    json_url = "https://api.snyk.io/v1/learn/lessons"
    try:
        response = requests.get(json_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        lessons_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON from {json_url}: {e}")
        return

    if not lessons_data:
        print("No lesson data found.")
        return

    # Create a directory to store the markdown files
    output_dir = "learn"
    os.makedirs(output_dir, exist_ok=True)

    for lesson in lessons_data:
        lesson_url = lesson.get("url")
        lesson_title = lesson.get("title")

        if not lesson_url or not lesson_title:
            print(f"Skipping lesson due to missing URL or title: {lesson}")
            continue

        print(f"Processing lesson: {lesson_title} from {lesson_url}")

        try:
            html_response = requests.get(lesson_url)
            html_response.raise_for_status()
            html_content = html_response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTML from {lesson_url}: {e}")
            continue

        soup = BeautifulSoup(html_content, 'html.parser')
        content_div = soup.find("div", class_="content")

        if content_div:
            h = html2text.HTML2Text()
            h.unicode_snob = True  # Preserve Unicode characters
            h.body_width = 0  # Disable line wrapping
            markdown_content = h.handle(str(content_div))

            # Find the first occurrence of '#' (which signifies an H1 in markdown)
            first_h1_index = markdown_content.find('# ')

            if first_h1_index != -1:
                # Remove everything before the first H1
                markdown_content = markdown_content[first_h1_index:]
            else:
                print(f"Warning: No H1 heading found in markdown for {lesson_title}. Keeping full content.")

            # Prepend the system prompt to the content
            system_prompt = f"""### System Prompt: Start ###
Refer to the following URL as the source of the information for anything used below. This applies to the content below until the next System Prompt.
Source URL: {lesson_url}
### System Prompt: End ###

            """
            markdown_content = system_prompt + "\n" + markdown_content

            # Sanitize the title for use as a filename
            filename = "".join([c for c in lesson_title if c.isalnum() or c in (' ', '-')]).rstrip()
            markdown_filepath = os.path.join(output_dir, f"{filename}.md")

            try:
                with open(markdown_filepath, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                print(f"Successfully saved: {markdown_filepath}")
            except IOError as e:
                print(f"Error writing file {markdown_filepath}: {e}")
        else:
            print(f"Could not find div with class 'content' in {lesson_url}")

    # Merge all created markdown files into one
    merged_output_filepath = "snyk-learn.md"
    with open(merged_output_filepath, "w", encoding="utf-8") as outfile:
        for filename in os.listdir(output_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n---\n\n")  # Add a separator between merged files
    print(f"\nAll markdown files merged into {merged_output_filepath}")

if __name__ == "__main__":
    fetch_and_convert_snyk_lessons()