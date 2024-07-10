# srv-provider_inventory

## Description

A simple python app that gather instance data from client and generate ansible inventory.

technical data :
- backend : fastapi
- database / orm : postgresql / SQLAlchemy

## Usage

### Classic python script

- configure venv and dependencies
```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
fastapi dev app/main.py
```

### Docker usage

@TODO

### Other usage

- launch test case :
```
python -m pytest tests/
```

## Sources
