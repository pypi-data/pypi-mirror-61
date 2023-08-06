
[![](https://codecov.io/gh/nickderobertis/bibtex-gen/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/bibtex-gen)

# bibtex-gen

## Overview

Generate BibTeX reference objects from DOIs and strings

## Getting Started

Install `bibtex_gen`:

```
pip install bibtex_gen
```

A simple example:

```python
import bibtex_gen

# Note: these are fake credentials. You need to sign up for a Mendeley account, go to Mendeley Developers,
# and create an "app" which will give you this info.
mendeley_client_id: str = '9871'
mendeley_client_secret: str = 'sdfa4dfDSSDFasda'
   
# Keys are name by which reference will be accessed, values are DOIs
item_doi_dict = {
    'da-engelberg-gao-2011': '10.1111/j.1540-6261.2011.01679.x',
    'barber-odean-2008': '10.1093/rfs/hhm079',
}

# These objects contain all the article data and can be used directly with pyexlatex
bibtex_objs = bibtex_gen.item_accessor_doi_dict_to_bib_tex(item_doi_dict, mendeley_client_id, mendeley_client_secret)
```

## Links

See the
[documentation here.](
https://nickderobertis.github.io/bibtex-gen/
)

## Author

Created by Nick DeRobertis. MIT License.