# srv-provider_inventory

## Description

A simple python app that create an inventory of the public cloud instance for multiple provider

technical data :
- backend : fastapi
- database / orm : postgresql


## Usage

- configure venv and dependencies
```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

- launch test case :
```
python -m pytest tests/
```

- start dev instance :
```
fastapi dev app/main.py
```


## Sources
