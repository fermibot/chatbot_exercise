# PDF Chatbot

Outlined in this repository is a Simple Chatbot. This document gives an overview of the document

---

## Getting Started

Use the following command to

- Install the required packages
- Export the relevant env variables to the memory

```commandline
sh init.sh
```

## Example

Show below is an example of how to use this Chatbot for searching a PDF document for information.

### Input

```commandline
python chatbot.py chapter6.pdf
```

### Output

```commandline
 🤖💬️ FileLoad|chapter6.pdf|Attempting
 🤖💬️ FileLoad|chapter6.pdf|Successful
 🤖💬️ TextSplitter|Instantiation|Start
 🤖💬️ TextSplitter|Instantiation|End
 🤖💬️ TextSplitter|split_documents|Start
 🤖💬️ TextSplitter|split_documents|End
 🤖💬️ ChatOpenAI|Model|loading|
 🤖💬️ ChatOpenAI|model|loaded|
 🤖💬️  Enter Your Query:
```

### Overview

Here is a video showing the above in action.

[//]: # ([![Watch the video]&#40;demo_video.png&#41;]&#40;https://www.youtube.com/watch?v=u9sWso45cRw&#41;)

---

## Architecture

### Document Loader and TextSplitter

This Chatbot uses
the  [PyPDFLoader](https://api.python.langchain.com/en/latest/document_loaders/langchain.document_loaders.pdf.PyPDFLoader.html)
for loading the document. By default, each of the page of the PDF is loaded into separate documents. But there is an
inherent problem with this. Many a times, the context is spread across multiple pages. This is problematic for
retrieval.

**How to solve this?** To make sure that context is "together", the first step is to combine all the separate texts into
a single long text and later split that using a `TextSplitter` of our choice. This chatbot does that
using [SpacyTextSplitter](https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.SpacyTextSplitter.html)
. `SpacyTextSplitter` uses the `spaCy` framework for splitting and is able to automatically detect the sentence contexts
for making the split decisions. Though we can specify the chunk length, it can vary depending on the context length.

### Prompt Template

A simple prompt that tells the Chatbot to only answer based on the context provided. This is to reduce the occurrences
of hallucinations.


