# SQL password manager

- [SQL password manager](#sql-password-manager)
  - [Simple password manager via Mysql and Mariadb server](#simple-password-manager-via-mysql-and-mariadb-server)
  - [Installation](#installation)
    - [Windows and Linux: Using uv(recommended)](#windows-and-linux-using-uvrecommended)
    - [Linux: using pip](#linux-using-pip)
    - [Windows: using pip](#windows-using-pip)
  - [Running](#running)
    - [Windows and Linux: using uv(recommended)](#windows-and-linux-using-uvrecommended-1)
    - [Windows: using python](#windows-using-python)
    - [Linux: using python](#linux-using-python)

## Simple password manager via Mysql and Mariadb server

---

## Installation

### Windows and Linux: Using [uv](https://github.com/astral-sh/uv)(recommended)

```bash
uv sync
```

### Linux: using pip

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### Windows: using pip

```ps1
python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt
```

## Running

### Windows and Linux: using uv(recommended)

```ps1
uv run main
```

### Windows: using python

```ps1
# Activating
.\.venv\Scripts\activate

# Executing
python main.py
```

### Linux: using python

```bash
# Activating the environment
source ./.venv/bin/activate

# Running
python main.py
```

![Koishi](https://media1.tenor.com/m/200dytcMF54AAAAd/koishi-dance.gif)

> Love from koishi :green_heart:
