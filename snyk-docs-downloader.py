import requests
import re
import os


def download_and_merge_snyk_docs():
    summary_url = "https://raw.githubusercontent.com/snyk/user-docs/refs/heads/main/docs/SUMMARY.md"
    base_doc_url = "https://raw.githubusercontent.com/snyk/user-docs/refs/heads/main/docs/"
    base_snyk_docs_url = "https://docs.snyk.io/"  # Base URL for the Snyk documentation
    subfolder = "docs/"

    try:
        response = requests.get(summary_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        summary_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading SUMMARY.md: {e}")
        return

    lines = summary_content.splitlines()
    counter = 0
    downloaded_md_files = []  # This list will now store only the paths to the downloaded MD files

    for line in lines:
        # Regex to find patterns like "[Title](relative/url.md)"
        match = re.search(r'\[.*?\]\((.*\.md)\)', line)
        if match:
            relative_url = match.group(1).strip()
            if relative_url:
                counter += 1
                doc_url = os.path.join(base_doc_url, relative_url).replace("\\", "/")  # Ensure forward slashes for URL

                # Construct the actual Snyk documentation URL
                snyk_source_url = base_snyk_docs_url + relative_url
                if relative_url.lower() == "readme.md":
                    snyk_source_url = snyk_source_url.replace("/readme.md", "")
                    snyk_source_url = snyk_source_url.replace("/README.md", "")
                else:
                    snyk_source_url = snyk_source_url.replace(".md", "")

                # Format counter to be 4 digits
                file_prefix = f"{counter:04d}"
                md_filename = f"{file_prefix}.md"

                print(f"Processing {doc_url} -> {md_filename} (Source URL: {snyk_source_url})")

                # Check if the markdown file already exists
                if os.path.exists(subfolder + md_filename):
                    print(f"Skipping download: {md_filename} already exists.")
                    downloaded_md_files.append(subfolder + md_filename)  # Still add to list for merging
                    continue  # Skip to the next line in the summary

                try:
                    doc_response = requests.get(doc_url)
                    doc_response.raise_for_status()

                    # Prepend the system prompt to the content
                    system_prompt = f"""### System Prompt: Start ###
Refer to the following URL as the source of the information for anything used below. This applies to the content below until the next System Prompt.
Source URL: {snyk_source_url}
### System Prompt: End ###

"""
                    full_content = system_prompt + doc_response.text

                    with open(subfolder + md_filename, 'w', encoding='utf-8') as f:
                        f.write(full_content)
                    downloaded_md_files.append(subfolder + md_filename)
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading {doc_url}: {e}")
                    continue

    output_md_name = "snyk-docs.md"
    print(f"\nMerging individual Markdown files into {output_md_name}...")
    try:
        with open(output_md_name, 'w', encoding='utf-8') as outfile:
            for md_file in sorted(downloaded_md_files):  # Ensure consistent order
                with open(md_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n---\n\n")  # Add a separator between documents for readability
        print(f"All Markdown files merged into {output_md_name}")
    except Exception as e:
        print(f"Error merging Markdown files: {e}")

    print("\nIndividual Markdown files are retained.")


if __name__ == "__main__":
    download_and_merge_snyk_docs()