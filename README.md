# 🔪 Test Generator – Automated Firmware Test Plan & Script Generation

## 📌 Project Overview

**Test Generator** is a modular Python project designed to automate the creation of firmware test plans and generate executable Python test scripts based on feature requirements. It uses a combination of:

* LLM prompting via [Ollama](https://ollama.ai/)
* Embedding-based semantic search for matching
* Structured output using `pandas`, `jinja2`, and `pytest`

This project is especially geared toward testing **optical communication transceivers** but can be adapted for other firmware systems as well.

---

## 📁 Project Structure

```
test_generator/
├── main.py                         # Main entry point for the pipeline
├── requirement_document/          # Contains markdown requirement/spec files
├── output/                        # Stores generated CSVs and test scripts
├── src/                           # All core modules are here
│   ├── firmware_library.py        # Empty function stubs representing firmware actions
│   ├── firmware_registry.json     # JSON mapping of firmware function metadata
│   ├── registry_matcher.py        # Embedding-based matcher to link steps to functions
│   ├── test_plan_generator.py     # Generates test plan (CSV) from requirement
│   ├── test_script_generator.py   # Generates pytest code from test plan + matcher
│   └── templates/
│       └── pytest_case.jinja2     # Optional Jinja template for structured test generation
```

---

## ⚙️ How It Works

### 🔀 End-to-End Workflow

1. **Start with a Markdown file** containing a firmware feature requirement (`requirement_document/*.md`)
2. **Generate a test plan** (20 SMART test cases) using an LLM
3. **Save the test plan** as a `.csv` file in `output/`
4. **Match test steps** to known firmware API stubs using semantic embeddings
5. **Generate `pytest` test scripts** using a hybrid of LLM + your function registry

---

## 📦 Key Components (Detailed)

### 1. `test_plan_generator.py` – 🧠 Converts Specs → Test Plan

This module:

* Reads a markdown file describing a firmware feature
* Sends it to an LLM using a structured system prompt that follows SMART test case methodology
* Generates test cases in the following format:

```json
{
  "Test Case Title": "Initialize Link",
  "Test Case Description": "Check if link initializes correctly.",
  "Test Steps": ["Call initialize_link()", "Check link status"],
  "Priority": "High",
  "Type": "Functional"
}
```

* Converts the list of test cases into a CSV using `pandas`

**Output**:

* `generated_test_plan_<timestamp>.csv` inside a timestamped folder in `output/`

---

### 2. `firmware_library.py` – 🧪 Your Function Test Stub Library

This Python file defines \~20 empty function **stubs** that:

* Mirror operations typically performed in firmware tests
* Have clear docstrings, parameters, and naming conventions
* Will eventually be called in generated test scripts

Example:

```python
def validate_register(register: str, expected_value: int) -> bool:
    """Validates that a register contains the expected value."""
    pass
```

**Why this matters**:
These functions are the vocabulary that generated test scripts will use. They help enforce consistency and avoid hallucinated APIs from LLMs.

---

### 3. `firmware_registry.json` – 📚 Function Metadata & Matching Index

This JSON file acts as a **machine-readable registry** of all functions in `firmware_library.py`. Each entry includes:

```json
{
  "name": "simulate_power_cycle",
  "description": "Simulates a power-off and power-on cycle on the firmware.",
  "parameters": [],
  "examples": ["simulate_power_cycle()"],
  "tags": ["simulate", "reset", "power"]
}
```

**Purpose**:

* Supports keyword/tag-based and semantic matching from natural language test steps
* Prevents hallucination by narrowing LLM’s response set to known, defined behaviors

---

### 4. `registry_matcher.py` – 🧠 Embedding-Based Step Matcher

This module uses `sentence-transformers` (MiniLM) to:

* Embed all function descriptions and tags from the registry
* Embed the natural-language test step from the test plan
* Return the **top-k closest functions** using cosine similarity

```python
match_step_to_function("Validate register value", top_k=2)
→ ["validate_register('REG1', 0x01)", "read_register('REG1')"]
```

**Advantage**:

* Enables LLMs to stay grounded in domain-specific, pre-approved logic
* Supports extensibility — add new functions to the registry without retraining or changing prompts

---

### 5. `test_script_generator.py` – 🧪 Converts Test Plan → Pytest Code

This module:

* Loads the test plan CSV
* For each test step:

  * Finds matching functions using `registry_matcher`
  * Constructs a prompt for the LLM with recommended API calls
  * Asks the LLM to write Python test code using `pytest`
* Extracts the generated code (with markdown extraction fallback)
* Writes each test to its own `.py` file

**Output**:

* Files like: `test_001_initialize_link.py`, `test_002_register_validation.py`, etc.

Optional:

* You can enable a `Jinja2` template (`pytest_case.jinja2`) to impose formatting or class structure.

---

## 🧪 Example Output

### 📝 Input Markdown (Feature Description)

```
## Performance Monitoring

The transceiver supports performance monitoring through a set of registers. Registers like RX_POWER and TX_POWER must be validated every second.
```

### ✅ Generated Test Case (from CSV)

```
Test Case Title: Validate RX Power Register
Test Steps:
  - Read RX_POWER register
  - Validate it is within expected range
```

### 🧪 Generated Pytest File

```python
import pytest
from firmware_library import *

def test_validate_rx_power_register():
    """Read RX_POWER and validate the range."""
    value = read_register("RX_POWER")
    assert 0 <= value <= 100  # Assuming expected power range
```

---

## 🛠️ Requirements

Install required packages:

```bash
pip install pandas jinja2 sentence-transformers ollama mdextractor
```

---

## 🚀 Running the Project

```bash
python main.py
```

Make sure:

* Your Ollama server is running locally (default at `http://127.0.0.1:11434`)
* Your markdown file exists under `requirement_document/`
* You have `firmware_library.py` and `firmware_registry.json` in `src/`