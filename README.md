# WattleFlow Core
![WattleFlow Logo](src/wattleflow/logo/wattleflow.png)

[![PyPI version](https://img.shields.io/pypi/v/wattleflow.svg)](https://pypi.org/project/wattleflow/)
[![Python versions](https://img.shields.io/pypi/pyversions/wattleflow.svg)](https://pypi.org/project/wattleflow/)
[![License](https://img.shields.io/pypi/l/wattleflow.svg)](https://github.com/wattleflow/core/blob/default/LICENSE)

# WattleFlow workflow framework add-in

---
Wattleflow OSCAL (Open Security Controls Assessment Language)
---

| Characteristic           | Value                                                                   |
| ------------------------ | ----------------------------------------------------------------------- |
| **Version**              | [![PyPI version](https://img.shields.io/pypi/v/wattleflow.svg)](https://pypi.org/project/wattleflow/) (latest release on PyPI) |
| **License**              | Apache 2.0 License                                                      |
| **Python Compatibility** | Python >=3.11                                                           |
| **Dependencies**         | wattleflow, wattleflow-oscal, wattleflow-workflow                       |
| **Size**                 | nimble                                                                  |
| **Documentation**        | [WattleFlow Core Documentation](https://github.com/wattleflow/docs.git) |


# WattleFlow Processors
Wattlelflow `oscal` is built on ISM add in for wattleflow ecosystem.

# Installation
```bash

pip install wattleflow-oscal

```


# Key Features

---

| Key Features         | Characteristic                                                             |
| ---------------------| -------------------------------------------------------------------------- |
| crosswalk.py         | Rewrites control ids from a source taxonomy into a target taxonomy/        |
| loaders.py           | Loads an ASD ISM OSCAL JSON *catalog*, and ASD ISM OSCAL JSON *profile*.   |
| models.py            | OSCAL model dataclasses.                                                   |
| policy.py            | Gate that validates components against an active OSCAL Profile.            |
| registry.py          | In-memory registry of OSCAL Catalogs indexed by UUID, with a flat          |
|                      | control-id lookup across all registered catalogs.                          |
| resolver.py          | Resolver constants, helpers and methods.                                   |


# Documentation
Comprehensive documentation will be available at the [Git Hub](https://github.com/wattleflow/docs.git).

# Contributing
We welcome contributions! Please check our GitHub repository for guidelines.

# License
Wattleflow OSCAL is licensed under the Apache 2.0 License. 
See the LICENSE file for more details.