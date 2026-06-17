# Module name: oscal/loaders.py
# Author: (wattleflow@outlook.com)
# Copyright: © 2022–2026 WattleFlow. All rights reserved.
# License: Apache 2 Licence


# --------------------------------------------------------------------------- #
# region Imports                                                              #
# --------------------------------------------------------------------------- #
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping, Union
from wattleflow.core import IStrategy, IWattleflow
from .models import Catalog, Profile

# --------------------------------------------------------------------------- #
# endregion Imports                                                           #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Constants                                                            #
# --------------------------------------------------------------------------- #
__author__ = "WattleFlow"
__copyright__ = "© 2022–2026 WattleFlow. All rights reserved"
# --------------------------------------------------------------------------- #
# endregion Constants                                                         #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Types                                                                #
# --------------------------------------------------------------------------- #
Pathish = Union[str, Path]
# --------------------------------------------------------------------------- #
# endregion Types                                                             #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Helpers                                                              #
# --------------------------------------------------------------------------- #


def _read_json(path: Pathish) -> Mapping[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"OSCAL JSON not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _require_path(kwargs: Mapping[str, Any], loader: str) -> Pathish:
    path = kwargs.get("path")
    if path is None:
        raise ValueError(f"{loader} requires 'path' keyword argument")
    return path


# --------------------------------------------------------------------------- #
# endregion Helpers                                                           #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Loaders                                                              #
# --------------------------------------------------------------------------- #


class ASDOSCALCatalogLoader(IStrategy):
    """Loads an ASD ISM OSCAL JSON *catalog* (full ISM or resolved-profile
    catalog) into a :class:`~wattleflow.oscal.models.Catalog`.

    Accepts both the OSCAL wrapper form (``{"catalog": {...}}``) and a bare
    catalog object.
    """

    def execute(self, caller: IWattleflow, **kwargs) -> Catalog:
        path = _require_path(kwargs, self.__class__.__name__)
        payload = _read_json(path)
        if "profile" in payload:
            raise ValueError(f"{path} is an OSCAL Profile document — use ASDOSCALProfileLoader")
        return Catalog.from_dict(payload)


class ASDOSCALProfileLoader(IStrategy):
    """Loads an ASD ISM OSCAL JSON *profile* (selector document) into a
    :class:`~wattleflow.oscal.models.Profile`.

    A profile only carries imports/selectors; resolving it against a source
    catalog into a flat control list is a separate concern not performed
    here.
    """

    def execute(self, caller: IWattleflow, **kwargs) -> Profile:
        path = _require_path(kwargs, self.__class__.__name__)
        payload = _read_json(path)
        if "catalog" in payload:
            raise ValueError(f"{path} is an OSCAL Catalog document — use ASDOSCALCatalogLoader")
        return Profile.from_dict(payload)


# --------------------------------------------------------------------------- #
# endregion Loaders                                                           #
# --------------------------------------------------------------------------- #
