# Python Log Analyzer

A simple Python tool for analyzing Linux authentication logs and identifying suspicious login activity.

This project was developed as part of my cybersecurity learning journey, with a focus on Python, Linux, and Blue Team fundamentals.

## Features

- Read and analyze Linux authentication logs
- Count failed login attempts
- Group failed login attempts by source IP address
- Identify suspicious IP addresses based on a configurable threshold
- Automated tests using pytest

## Project Structure

```text
python-log-analyzer/
├── reports/
├── sample_logs/
│   └── auth.log
├── tests/
│   └── test_log_analyzer.py
├── log_analyzer.py
├── README.md
└── requirements.txt
```

## Technologies

- Python
- Linux authentication logs
- pytest

## How to Run

Clone the repository:

```bash
git clone https://github.com/lucascalhiarana/python-log-analyzer.git
```

Navigate to the project directory:

```bash
cd python-log-analyzer
```

Run the analyzer:

```bash
python log_analyzer.py
```

## Example Output

```text
=== ANALISADOR DE LOGS ===
Total de linhas analisadas: 7
Tentativas de login malsucedidas: 4

Falhas de autenticação por IP:
IP: 192.168.1.50 | Tentativas: 3
IP: 10.0.0.15 | Tentativas: 1

IPs suspeitos:
ALERTA: 192.168.1.50 atingiu o limite de tentativas.
```

## Running Tests

Install pytest:

```bash
python -m pip install pytest
```

Run the tests from the project root:

```bash
python -m pytest tests/test_log_analyzer.py
```

## Learning Objectives

This project helped me practice:

- Python functions and data structures
- File handling
- Log analysis
- Dictionaries and lists
- Basic security event detection
- Automated testing

## Disclaimer

This project uses sample authentication logs for educational purposes.

The suspicious IP detection rule is based on a simple threshold and should not be considered a complete security monitoring solution.

## Author

Lucas

Cybersecurity student focused on Blue Team and SOC fundamentals.

GitHub: [lucascalhiarana](https://github.com/lucascalhiarana)