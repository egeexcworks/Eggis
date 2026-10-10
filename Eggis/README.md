# Eggis

Eggis is a personal AI assistant project built with Python. The long-term goal is to support natural interaction, persistent memory, reasoning, and safe desktop automation.

> **Early development:** features are being implemented incrementally; the modules currently contain only starter scaffolding.

## Requirements

- Python 3.11 or newer recommended

## Run

From the repository root:

```bash
python -m eggis.main
```

## Project layout

```text
eggis/
├── main.py       # Application entry point
├── brain.py      # Request understanding and reasoning
├── memory.py     # Persistent memory
└── tools/        # Tools Eggis may use
tests/            # Automated tests
```

## Development

Create and activate a virtual environment, then install dependencies from `requirements.txt` when dependencies are added.

## Security

Never commit API keys, passwords, `.env` files, or private memory/database files. Review changes before pushing to this public repository.
