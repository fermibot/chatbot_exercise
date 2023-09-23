<p align="center">
<img src="https://img.shields.io/badge/PDFChatbot-1.0-green.svg"/>
<img src="https://img.shields.io/badge/LangChain-OpenAI-blue"/>
</p>

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
. `SpacyTextSplitter` uses the `spaCy` framework for splitting and is able to _automatically detect the sentence
contexts_ for making the split decisions. Though we can specify the chunk length, it can vary depending on the context
length.

Config for splitter: A chunk size of `1024` with an overlap of `256` was used.

### Prompt Template

A simple prompt that tells the Chatbot to only answer based on the context provided. This is to reduce the occurrences
of hallucinations.

```text
"""Answer the following question based on the context only and nothing else. 
                            if the user is asking for instructions, return the answer as bullets
                            context: {context}
                            question: {user_input}
                            answer: """
```

### Embeddings

Used [OpenAIEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html)
for this use case.

ℹ️ Experiments with a
few [HuggingFaceEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.huggingface.HuggingFaceEmbeddings.html)
resulted in performance was not as expected. Sometimes, there was
misinterpretation of the context for the given question. Sometimes, the retrieval was also nonsensical. Some
models used were

### Retriever(s)

To be able to get the most expected reponse possible, I have combined several concepts to design a
custom [EnsembleRetriever](https://python.langchain.com/docs/modules/data_connection/retrievers/ensemble). Explained
below is the methodology.

1. Create a [FAISS](https://faiss.ai/index.html) vectorstore and use the `as_retriever` method to turn this into a
   retriever.
2. Create
   a [MultiQueryRetriever](https://python.langchain.com/docs/modules/data_connection/retrievers/MultiQueryRetriever)
   to **augment** the user's question for better contextual search. Use the link for details on this concept.
3. Create
   a [ContextualCompressionRetriever](https://python.langchain.com/docs/modules/data_connection/retrievers/contextual_compression/)
   retriever for using the correct context from the extracted chunk for prompting the LLM
4. Finally, use the `ContextualCompressionRetriever`, `FAISS.as_retriever` and the `MultiQueryRetriever` to assemble
   the `EnsembleRetriever`
5. ℹ️ Abandoned the `BM25Retriever` after a few experiments, might integrate that back depending on the use case

### Chat Model

Used the [LLMChain](https://docs.langchain.com/docs/components/chains/llm-chain) for performing the chat operations.

### Bringing it all together!

The architecture for this bot is shown below

<p align="center">
  <img src="PDFChatBot.svg" width="400"/>
</p>

---
<p align="center">Fermibot ✌️</p>