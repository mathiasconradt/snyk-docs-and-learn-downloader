# Snyk Docs Downloader

Retrieve all markdown files from the Snyk User Docs Github repo and merge it into a single markdown file called snyk-docs.md, which can then be used to add context to an LLM and query it.

```
uv pip install -r requirements.txt
python snyk_doc_downloader.py
```

## Gemini Prompt

```
Refer to attached md file. Always list the source urls for your answers as stated in the doc for the relevant section. Do not make URLs up that are not in the markdown file and do not use google.com/search urls. Only show source urls that are actually in the md file.
List the source URLs as clickable links all together at the very bottom of your answer. 
Make sure the source URLs are clickable!

Here is my question:

I use snyk with gitlab and the broker, as its onpremise. how to configure it and how to best debug it?
```
