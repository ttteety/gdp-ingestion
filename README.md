# GDP-INGESTION

This project is used to ingest historical GDP data from the world bank API https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json and import to postgres database.

## Prerquites

- Python 3.x
- Docker

## Setting up a Virtual Environment
### 1. Install 'virtualenv'
If you don't have `virtualenv` installed, you can install it using the following command:

```
pip install virutalenv
```

### 2. Setup a Virtual Environment

```
virtualenv venv
```

### 3. Activate the Virtual Environment
On Windows:

```
venv\Scripts\activate
```

On macOS and Linux:

```
source venv/bin/activate
```

### 4. Install Project Dependencies

```
pip install -r requirements.txt
```

### 5. Deactivate the Virtual Environment
When you're done working on the project, deactivate the virtual environment.

```
deactivate
```

### 6. Run python script to ingest data to Postgres

```
python main.py
```