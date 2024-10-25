# Schema Evolution Analyzer

The Schema Evolution Analyzer is a tool that helps you understand and manage changes in your database schema over time. It provides insights into the impact of schema changes on existing queries and applications, making it easier to evolve your database schema with confidence.

## Features

- Analyze schema evolution patterns and detect potential issues
- Identify queries and applications affected by schema changes
- Suggest optimizations and modifications for impacted queries
- Integrate with your existing database change management process
- Provide a standalone version for quick and easy analysis

## Getting Started

### Prerequisites

- Python 3.9 or higher
- PostgreSQL (if using the PostgreSQL storage backend)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/schema-evolution-analyzer.git
   cd schema-evolution-analyzer
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a copy of the `config.example.yaml` file and rename it to `config.yaml`:

   ```bash
   cp config.example.yaml config.yaml
   ```

2. Open `config.yaml` and modify the configuration settings according to your environment.

### Usage

1. Import the necessary classes in your Python script:

   ```python
   from schema_analyzer import SchemaEvolutionAnalyzer, AnalyzerConfig
   ```

2. Load the configuration and create an instance of the analyzer:

   ```python
   config = AnalyzerConfig.from_file("config.yaml")
   analyzer = SchemaEvolutionAnalyzer(config)
   ```

3. Analyze your schema evolution:

   ```python
   result = analyzer.analyze_evolution(old_schema, new_schema)
   print(result)
   ```

   Replace `old_schema` and `new_schema` with your actual schema definitions.

### Running Tests

To run the test suite, use the following command:

```bash
pytest tests/
```

## Repository Structure

```
schema-evolution-analyzer/
├── schema_analyzer/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── config.py
│   ├── models.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── postgresql.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_config.py
│   └── test_storage.py
├── config.example.yaml
├── requirements.txt
├── README.md
└── LICENSE
```

- `schema_analyzer/`: Contains the main package code.
  - `analyzer.py`: Implements the core schema evolution analysis logic.
  - `config.py`: Handles configuration management.
  - `models.py`: Defines data models and schemas used in the analyzer.
  - `storage/`: Contains storage backend implementations.
  - `utils/`: Contains utility functions and helper modules.
- `tests/`: Contains test cases for the package.
- `config.example.yaml`: An example configuration file template.
- `requirements.txt`: Lists the required Python dependencies.
- `README.md`: Provides an overview of the project and instructions for getting started.
- `LICENSE`: Specifies the license under which the project is distributed.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository. If you'd like to contribute code, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.