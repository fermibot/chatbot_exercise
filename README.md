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

[![Watch the video](demo_video.png)](https://www.youtube.com/watch?v=u9sWso45cRw)


---

## Overview of the architecture

