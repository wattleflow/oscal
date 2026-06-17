# WattleFlow OSCAL

![WattleFlow Logo](https://github.com/wattleflow/core/raw/default/src/wattleflow/logo/wattleflow.png)

---
Wattleflow - Open Security Controls Assessment Language
---

[![PyPI version](https://img.shields.io/pypi/v/wattleflow-oscal.svg)](https://pypi.org/project/wattleflow-oscal/)
[![Python versions](https://img.shields.io/pypi/pyversions/wattleflow-oscal.svg)](https://pypi.org/project/wattleflow-oscal/)
[![License](https://img.shields.io/pypi/l/wattleflow-oscal.svg)](https://github.com/wattleflow-oscal/core/blob/default/LICENSE)


# WattleFlow - Workflow Framework Add-In



| Characteristic           | Value                                                                   |
| ------------------------ | ----------------------------------------------------------------------- |
| **Version**              | [![PyPI version](https://img.shields.io/pypi/v/wattleflow-oscal.svg)](https://pypi.org/project/wattleflow-oscal/) (latest release on PyPI) |
| **License**              | [![License](https://img.shields.io/pypi/l/wattleflow-oscal.svg)](https://github.com/wattleflow-oscal/core/blob/default/LICENSE) |
| **Python Compatibility** | [![Python versions](https://img.shields.io/pypi/pyversions/wattleflow-oscal.svg)](https://pypi.org/project/wattleflow-oscal/)|
| **Dependencies**         | [wattleflow-core](https://www.github.com/wattleflow/core.git), [wattleflow-workflow](https://www.github.com/wattleflow/workflow.git) |
| **Size**                 | nimble                                                                  |
| **Documentation**        | [WattleFlow Core Documentation](https://github.com/wattleflow/docs.git) |


# OSCAL
Wattlelflow `oscal` is built on ISM add in for wattleflow workflow ecosystem.


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