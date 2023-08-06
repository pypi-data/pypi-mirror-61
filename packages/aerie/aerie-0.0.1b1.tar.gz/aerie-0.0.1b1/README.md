<p align="center">
<a href="https://travis-ci.org/alex-oleshkevich/aerie">
    <img src="https://api.travis-ci.com/alex-oleshkevich/aerie.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/alex-oleshkevich/aerie">
    <img src="https://codecov.io/gh/alex-oleshkevich/aerie/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/aerie/">
    <img src="https://badge.fury.io/py/aerie.svg" alt="Package version">
</a>
</p>

---

# An object mapper for async python.

## Installation

```bash
pip install aerie
```

## Usage

```python
from aerie import Connection, Store, Schema, fields

connection = Connection('postgresql://user:pass@localhost/db_name')
store = Store(connection)

class User(Schema):
    id = fields.IntegerField()
    name = fields.StringField()

rows = await store.raw('select * from users').to(User)

```
