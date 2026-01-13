# DocuForge: Autonomous Technical Documentation Engine

> **A Multi-Agent RAG System for High-Precision R&D Workflows**

[![DocuForge Demo](https://img.youtube.com/vi/23ccmZQ1SHE/maxresdefault.jpg)](https://youtu.be/23ccmZQ1SHE)

> 📺 **[Watch the Architectural Walkthrough](https://youtu.be/23ccmZQ1SHE)** featuring core functionalities.


![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen) 
![Python](https://img.shields.io/badge/python-3.11-blue) 
![Stack](https://img.shields.io/badge/stack-LangGraph%20|%20FastAPI%20|%20React-blueviolet)

DocuForge is an agentic workflow engine designed to bridge the gap between raw engineering specifications and ISO-compliant customer documentation. Unlike standard "Chat with PDF" bots, DocuForge employs a **Self-Correcting Multi-Agent Architecture** to enforce technical accuracy and style compliance autonomously.

---

## Architectural Strategy (ADR 001)

### The Problem: Why Standard RAG Fails in R&D
Traditional RAG (Retrieval Augmented Generation) pipelines are **linear**: `Input -> Retrieve -> Generate -> Output`.
In safety-critical industries like Vaisala's (meteorology, industrial measurements), a linear process is insufficient because:
1.  **Hallucinations are dangerous:** A single wrong voltage spec can ruin hardware.
2.  **Style is strict:** Passive voice and ambiguous warnings are often forbidden by technical style guides.

### The Solution: Cyclic Agentic Graphs
We moved beyond linear chains to a **Stateful, Cyclic Graph** using **LangGraph**.

**The Logic:**
The workflow is modeled as a State Machine:
1.  **State**: A shared memory containing the `draft`, `critique`, and `revision_count`.
2.  **Nodes**: 
    * `Drafter`: Generates content based on RAG context.
    * `Critic`: Reviews content against Vaisala compliance rules.
3.  **Edges**:
    * **Conditional Logic**: If `Critic` rejects -> Loop back to `Drafter`.
    * **Termination**: If `Critic` approves OR `revision_count > 3` -> End.

---

## The Agent Workflow

1.  **Ingest**: User uploads a PDF (e.g., "HMP155 Manual"). Text is chunked and embedded into Qdrant.
2.  **Retrieve**: User asks "How do I install the sensor?". System retrieves relevant chunks using hybrid search.
3.  **Draft**: `Drafter Agent` writes an initial answer.
4.  **Critique**: `Critic Agent` checks for:
    * **Factuality:** Does it match the source?
    * **Style:** Active voice only.
    * **Safety:** Are warnings explicit?
5.  **Refine**: If rejected, the Draft is sent back to the Drafter with feedback to fix the specific errors.
6.  **Finalize**: Loop repeats until Approved or Max Retries (3).

---

## Live Demo Scenarios

To verify the system's intelligence, upload the provided `HMP-X_Manual.pdf` and run these specific prompts.

### 1. The Precision Test (RAG Accuracy)
**Question:**
> *"What are the specific wiring pinouts and the operating voltage range for the HMP-X Pro?"*

* **Why this matters:** It forces the agent to synthesize data from two disparate sections of the document ("3.2 Wiring" and "4. Technical Specifications") into a single coherent answer.
* **Success Indicator:** The system must correctly list **Pin 1 (Brown)** through **Pin 4 (Black)** AND cite the voltage as **15 ... 30 VDC**.

### 2. The Compliance Test (Agentic Reasoning)
**Question:**
> *"Write a short guide on how to mount the probe, including safety precautions."*

* **Why this matters:** This targets the **Critic Agent**. The raw source text uses passive voice (*"The probe should be mounted..."*). The Critic is programmed to reject this and enforce Active Voice.
* **Success Indicator:** The output must use command verbs (e.g., *"Insert the probe," "Secure the flange"*) and explicitly highlight the warning: *"Do not touch the sensor with bare hands."*

---

## Tech Stack

* **Orchestration:** Docker Compose (Microservices architecture)
* **Frontend:** React 18 + TypeScript + TailwindCSS (Vite)
* **Backend:** FastAPI (Async Python 3.11)
* **AI Engine:** LangGraph + LangChain (OpenAI GPT-4)
* **Knowledge Base:** Qdrant (Vector Database with Hybrid Search)
* **Testing:** Pytest (91% Coverage) with Mocking

---

## Quick Start

### Prerequisites
* Docker & Docker Compose
* OpenAI API Key

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Nibir1/DocuForge.git
    cd docuforge
    ```

2.  **Configure Environment**
    ```bash
    cp .env.example .env
    # Open .env and paste your OPENAI_API_KEY
    ```

3.  **Launch System**
    ```bash
    make up
    # System will be available at http://localhost:5173
    ```

### Testing & Validation

Run the comprehensive test suite (mocking external providers for zero-cost testing):

```bash
make test-cov
```

### Developer Commands (Makefile)

| Command | Description |
| :--- | :--- |
| `make up` | Start the full stack (Backend, UI, Database) |
| `make logs` | View real-time logs from all services |
| `make shell` | Open a terminal inside the backend container |
| `make test` | Run the standard test suite |
| `make test-cov` | Run tests with **coverage report** (Target: >90%) |
| `make clean` | Stop containers and remove volumes |

---

## Project Structure

```text
docuforge/
├── backend/
│   ├── app/
│   │   ├── agents/      # The "Brain": Graph, Nodes, Prompts
│   │   ├── services/    # The "Memory": Qdrant & Ingestion
│   │   └── models/      # Type Definitions (Pydantic)
│   └── tests/           # Integration & Unit Tests
├── frontend/            # React + TypeScript Dashboard
├── docker-compose.yml   # Infrastructure Definition
└── Makefile             # Automation Scripts

```

Designed & Architected by **Nahasat Nibir**