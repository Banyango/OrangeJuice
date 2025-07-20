# OrangeJuice

A RAG (Retrieval-Augmented Generation) tool for managing and querying git repositories with a focus on simplicity and extensibility.

## Features

- Add and manage git repositories
- Query commits and repositories

## Quickstart

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) 0.7.20+

### Installation
```bash
# Clone the repo
git clone https://github.com/your-org/orangejuice.git
cd orangejuice

# Install dependencies
uv install --dev
```

### Usage
#### CLI
```bash
python main.py --help
```

#### Example Commands
```bash
python main.py repos create my-repo --path ./data
python main.py repos ls
```


## Project Structure
```
src
├── app            # CLI (Textual, Click, etc.)
│   ├── repos
│   │   ├── repo.py        # CLI subcommands & DuckDB client
│   │   ├── repos.py
│   │   ├── responses.py
│   ├── commits
│   ├── embeddings
│   ├── config.py
│   ├── container.py
├── core           # Business logic
│   ├── repos
│   │   ├── add_repo_operation.py
│   │   ├── errors.py
├── data           # Pure queries/statements
│   ├── commits
│   ├── repos
│   │   ├── queries.py
│   │   ├── statements.py
├── entities       # Inner-level entities/models
│   ├── base.py
│   ├── commits.py
│   ├── repos.py
├── libs           # Library interfaces (DuckDB, ChromaDB, etc.)
│   ├── duckdb
│   │   ├── provider.py
│   ├── chromadb
│   │   ├── base.py
│   │   ├── providers.py
│   ├── embeddings
│   │   ├── provider.py
│   ├── git
│   │   ├── service.py
```

## Contributing
Pull requests and issues are welcome! Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributing Guide](CONTRIBUTING.md).

## License
MIT

## Acknowledgements
- [DuckDB](https://duckdb.org/)
- [ChromaDB](https://www.trychroma.com/)
- [Textual](https://textual.textualize.io/)

---

*OrangeJuice: Squeeze the most out of your git.*
