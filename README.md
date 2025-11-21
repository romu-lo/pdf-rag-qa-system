# RAG PDF Question-Answering System

This project was developed as part of the AI Engineer Challenge.
The goal is to build a system capable of **receiving PDF files, extracting their contents, locally indexing them**, and finally allowing users to **ask questions** that the system answers using **Retrieval-Augmented Generation (RAG)**.

## Motivation

Modern LLMs are powerful but lack access to private or domain-specific documents.
This project demonstrates how to bridge that gap by combining:

- Document ingestion and chunking

- Vector embeddings for semantic search

- Fast retrieval of relevant context

- LLM-based answer generation

The goal was to create a clean, modular, production-ready structure that integrates a backend API, a lightweight frontend, and a retrieval pipeline.

## What Was Built

### A FastAPI backend to:

- Upload and process PDF files

- Extract text using `pdfplumber`

- Chunk the text and generate embeddings

- Locally store embeddings using ChromaDB

-  Answer user questions using LangChain + OpenAI models

### A Streamlit frontend to:

- Upload documents interactively

- Ask questions and display model answers

- A Makefile-based setup with `uv` for environment management

- A clean architecture following a domain-driven structure to ensure maintainability

## Technologies & Libraries Used

The project was developed on a `WSL` with `Ubuntu 22.04`, and using a `Python 3.12` environment managed by `uv`.

### Core Libraries

- `FastAPI` + `Uvicorn` – backend REST API

- `Streamlit` – frontend web interface

- `ChromaDB` – local vector storage for semantic search

- `LangChain` and it's OpenAI, Chroma, and community modules

- `OpenAI` – LLM & embedding models

- `pdfplumber` – PDF text extraction, aiming for better maintaining the original file's structure 

### Other Tools

- `python-multipart` – file upload handling

- `pydantic-settings` – configuration management

- `uv` – environment and package manager

- `Makefile` – project automation

## How to Run the Project

Environment used during development: `Ubuntu 22.04` (`Linux` or `WSL` required). An OpenAI API Key is necessary to run the project

1. Clone the repository
```bash
git clone https://github.com/romu-lo/pdf-rag-qa-system.git
```

2. Create a `.env` file in the repository's root, and insert your OpenAI API Key following the example bellow. Your `.env` file should look like this:

```
OPENAI_API_KEY = "insert your key here"
```

3. Install `uv` using the following terminal command
```bash
make setup
```

4. Start the frontend and backend
```bash
make run
```


This will open two terminal panes using `tmux`:

- Backend (`FastAPI`) → http://127.0.0.1:8000/

- Backend Docs (`Swagger UI`) → http://127.0.0.1:8000/docs

- Frontend (`Streamlit`) → http://localhost:8501/

## API Endpoints

It is possible to run just the backend using the command:

```bash
make api
```

To use the backend separately, you can access the `Swagger UI` → http://127.0.0.1:8000/docs

### POST /documents

Upload one or more PDF files.

Example Response
```JSON
{
  "message": "Documents processed successfully",
  "documents_indexed": 1,
  "total_chunks": 42
}
```

### DELETE /documents

Delete all previously uploaded documents

Example Response
```JSON
{
  "message": "All indexed documents have been cleared."
}
```

### POST /question

Ask a question about the previously uploaded documents.

Example Request
```JSON
{
  "question": "What is the purpose of this document?"
}
```

Example Response
```JSON 
{
  "answer": "To provide general procedures and guidelines that apply to Baldor motor products, including safety notices; the manual covers general guidelines for installation, operation and maintenance.",
  "references": [
    "Overview This manual contains general procedures that apply to Baldor Motor products. Be sure to read and understand the Safety Notice statements in this manual. For your protection, do not install, operate or attempt to perform maintenance procedures until you understand the Warning and Caution statements.", 
    "Important: This instruction manual is not intended to include a comprehensive listing of all details for all procedures required for installation, operation and maintenance. This manual describes general guidelines that apply to most of the motor products shipped by Baldor."
  ]
}
```

## Frontend Usage Example (`Streamlit`)

1. Open: http://localhost:8501/

2. Upload your PDF documents

3. Ask a question such as:
“Summarize the maintenance requirements of the machine.”

4. Receive an LLM-generated answer including retrieved references

### Examples

With `MN414_0224.pdf` uploaded

Question: 

    What is the step by step instalation process for this pump?

Answer:

    1. Step-by-step installation procedure:
    2. Turn off and lockout all power and verify the voltage at the motor starter connectors are zero.Connect the motor power leads to the connectors in the motor starter. (See “Grounding”). Note: The motor lead cable assembly for all Submersible Pump Motors has 3 marked power leads plus two ground leads, two thermal leads and two moisture sensing probe leads.
    3. Three Phase Motors ONLY. a. Turn off and lockout all power and verify the voltage at the motor starter connectors are zero. i. Turn off and lockout all power and verify that the voltage at the motor leads is zero. ii. Reverse any two of three motor power leads at the motor starter. iii. Restore power and verify correct rotation. iv. Turn off and lockout all power and verify that the voltage at the motor leads is zero.
    4. Connect the two Thermal Protectors at the motor starter.
    5. Connect the two Moisture Sensing Probes at the motor starter.
    6. Follow pump manufacturer’s instructions and mount the pump on the motor shaft.
    7. Secure the pump case to the motor flange.
    8. Attach drain piping to pump.
    9. Use spreader bar and lifting eyes to lower the motor/pump assembly to the proper depth. Be sure that motor wires are not damaged (contact with metal objects etc.)
    10. Set control parameter values (if applicable) according to motor nameplate values.

With both `WEG-CESTARI-manual...` and `MN414_0224.pdf` uploaded

Question

    What is the WEG-CESTARI document about?

Answer

    It is the WEG-CESTARI product manual for gear units and gearmotors, detailing important requirements and guidance for shipment, storage, installation, operation and maintenance (including related warranty and environmental guidance).

## Project Structure (simplified)
```
app/
source/
  domain/
  core/
  infrastructure/
  api/
resources/
Makefile
pyproject.toml
README.md
```

## Project Considerations

`pdfplumber` was chosen as the PDF loader because it is fast and can reasonably well maintain the structure of the file, including tables. During development I discovered `PyMuPDF4LLM`, which trasnforms PDFs into Markdowns, and can detect tables and multiple columns. As LLMs understand Markdown formatting, it is ideal for RAG applications, but it took a long time to process the bigger files. In a production environment where files are only ingested once and new files are rare, `PyMuPDF4LLM` would be a great choice.

The application is using MMR retrieval technique, which aims to retrieve not only relevant documents, but also documents that are diverse among each other. I hadn't worked with this retrieving method before, but found it very interesting and  the results were great.

This system does not store conversation history in any way. This means each question is independent from previous ones. Even though the back and front end implementations are ready to support chat history management, I chose not to use it in this challenge because it would increase the complexity of the system.

While testing, I found out that the system developed works better with a single document uploaded. This is a point that can be worked on, maybe by filtering the retrieving results in some way or by implementing and retrieval agent.
