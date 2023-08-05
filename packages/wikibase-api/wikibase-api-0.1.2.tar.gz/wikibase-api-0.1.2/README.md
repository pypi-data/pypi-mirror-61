# wikibase-api

**`wikibase-api` is a Python library for simple access to the [Wikibase API](https://www.wikidata.org/w/api.php?action=help).**

It simplifies the authentication process and can be used to query and edit information on Wikidata or any other Wikibase instance.

**For a simpler, object-oriented abstraction of the Wikibase API, have a look at [`python-wikibase`](https://github.com/samuelmeuli/python-wikibase).**

## Installation

```sh
pip install wikibase-api
```

## Usage

Simple example for fetching all information about a Wikidata page:

```py
from wikibase_api import Wikibase

wb = Wikibase()
r = wb.entity.get("Q1")
print(r)
```

Output:

```python
{
  "entities": {
    "Q1": {
      # ...
    }
  },
  "success": 1,
}
```

**See the [documentation](https://wikibase-api.readthedocs.io) for descriptions and examples of all commands.**

## Development

### Contributing

Suggestions and contributions are always welcome! Please discuss larger changes via issue before submitting a pull request.

### Setup

See [this guide](https://wikibase-api.readthedocs.io/en/latest/development/development.html) on how to set up a development environment for this package.

## Related

- [`python-wikibase`](https://github.com/samuelmeuli/python-wikibase) – Wikibase queries and edits made easy
