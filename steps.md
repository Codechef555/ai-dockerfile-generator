# Local Dockerfile Generator — Implementation Roadmap

## Implementation Sequence

Follow this exact order when creating and implementing the project. Complete each step before moving to the next.

### 1. `requirements.txt`
Defines the Python libraries required by the project, including the Ollama client and testing dependencies.

### 2. `app/__init__.py`
Initializes the `app` directory as a Python package so its modules can be imported cleanly.

### 3. `templates/python.txt`
Contains the prompt instructions for generating Dockerfiles for Python applications.

### 4. `templates/nodejs.txt`
Contains the prompt instructions for generating Dockerfiles for Node.js applications.

### 5. `templates/java.txt`
Contains the prompt instructions for generating Dockerfiles for Java applications.

### 6. `app/prompt_templates.py`
Loads the appropriate language template and combines it with the user's project description to create the LLM prompt.

### 7. `app/llm_client.py`
Connects the Python application to Ollama and sends prompts to the locally running language model.

### 8. `app/generator.py`
Coordinates prompt creation and LLM inference to generate Dockerfile content for the selected language.

### 9. `app/validator.py`
Checks generated Dockerfiles for basic structural issues, missing instructions, and potentially unsafe patterns.

### 10. `app/main.py`
Provides the main application entry point, accepts user input, invokes generation and validation, and saves the resulting Dockerfile.

### 11. `examples/python-api/`
Contains a sample Python API application used to generate, build, and test a Python Dockerfile.

### 12. `examples/node-api/`
Contains a sample Node.js API application used to generate, build, and test a Node.js Dockerfile.

### 13. `examples/java-api/`
Contains a sample Java application used to generate, build, and test a Java Dockerfile.

### 14. `tests/test_generator.py`
Contains automated tests for Dockerfile generation, prompt handling, supported languages, and error cases.

### 15. `tests/test_validator.py`
Contains automated tests for Dockerfile validation, including valid output, missing instructions, empty content, and suspicious patterns.

### 16. `evaluation/results.csv`
Stores experimental results, including the language, model, build success, generation time, image size, and evaluation notes.

### 17. `.gitignore`
Specifies local files and generated artifacts that Git should exclude, such as virtual environments, Python caches, and local secrets.

### 18. `README.md`
Documents the project overview, architecture, installation, usage, supported languages, testing, evaluation, and limitations.

### 19. End-to-End Testing and Final Refinements
Tests the complete workflow from user input to Dockerfile generation, validation, saving, Docker builds, and application startup. Fixes issues and finalizes the documentation.

---

## Development Rule

Implement files in the order listed above. Test each component before proceeding to the next, and ensure the complete workflow works locally through Ollama without requiring cloud LLM APIs.
