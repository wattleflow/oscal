# Module name: oscal/resolver.py
# Author: (wattleflow@outlook.com)
# Copyright: © 2022–2026 WattleFlow. All rights reserved.
# License: Apache 2 Licence


# --------------------------------------------------------------------------- #
# region Imports                                                              #
# --------------------------------------------------------------------------- #
from __future__ import annotations
import uuid as _uuid
from dataclasses import replace
from typing import List, Optional, Set, Tuple
from .models import Catalog, Control, Group, Profile
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
# region Helpers                                                              #
# --------------------------------------------------------------------------- #


def _filter_controls(
    controls: List[Control],
    selected: Set[str],
) -> Tuple[List[Control], Set[str]]:
    """Return (kept_controls, ids_found). Keeps a control if its id is
    selected OR any descendant is selected; in the latter case the control
    is rebuilt with only the surviving children.
    """
    kept: List[Control] = []
    found: Set[str] = set()
    for ctrl in controls:
        sub_kept, sub_found = _filter_controls(ctrl.controls, selected)
        is_self_selected = ctrl.id in selected
        if is_self_selected or sub_kept:
            if sub_kept != ctrl.controls:
                kept.append(replace(ctrl, controls=sub_kept))
            else:
                kept.append(ctrl)
            found.update(sub_found)
            if is_self_selected:
                found.add(ctrl.id)
    return kept, found


def _filter_groups(
    groups: List[Group],
    selected: Set[str],
) -> Tuple[List[Group], Set[str]]:
    """Recursively prune groups; drop any group that contains no surviving
    controls or sub-groups.
    """
    kept: List[Group] = []
    found: Set[str] = set()
    for group in groups:
        sub_groups, gfound = _filter_groups(group.groups, selected)
        sub_controls, cfound = _filter_controls(group.controls, selected)
        if sub_groups or sub_controls:
            kept.append(replace(group, groups=sub_groups, controls=sub_controls))
            found.update(gfound)
            found.update(cfound)
    return kept, found


# --------------------------------------------------------------------------- #
# endregion Helpers                                                           #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Resolver                                                             #
# --------------------------------------------------------------------------- #


def resolve(
    profile: Profile,
    source: Catalog,
    *,
    catalog_uuid: Optional[str] = None,
    strict: bool = True,
) -> Catalog:
    """Resolve an OSCAL Profile against a source Catalog.

    Walks ``source`` and keeps only controls whose ids are selected by
    ``profile.imports[*].include_controls[*].with_ids``, minus any in
    ``exclude_controls``. Group hierarchy is preserved (``as-is`` merge);
    empty groups are pruned.

    Resolution is intentionally minimal — ``modify`` (alters/sets), pattern
    matching, parameter overrides, and ``include-all`` selectors are not
    implemented because ASD ISM profiles do not use them.

    Parameters
    ----------
    profile
        The Profile selecting controls.
    source
        The Catalog the profile imports from. The caller is responsible
        for ensuring this matches ``profile.imports[*].href``.
    catalog_uuid
        UUID for the resolved Catalog. Defaults to a fresh UUID4.
    strict
        If True (default), raise when the profile references control ids
        absent from the source catalog.
    """
    selected: Set[str] = set(profile.control_ids())
    if not selected:
        raise ValueError(f"Profile {profile.uuid} selects no controls")

    excluded: Set[str] = set()
    for imp in profile.imports:
        for exc in imp.exclude_controls:
            excluded.update(exc.with_ids)
    target_ids = selected - excluded

    kept_controls, ctrl_found = _filter_controls(source.controls, target_ids)
    kept_groups, group_found = _filter_groups(source.groups, target_ids)

    found = ctrl_found | group_found
    if strict:
        missing = target_ids - found
        if missing:
            raise KeyError(
                f"Profile {profile.uuid} references {len(missing)} control(s) "
                f"absent from source catalog {source.uuid}: "
                f"{sorted(missing)[:10]}{'...' if len(missing) > 10 else ''}"
            )

    return Catalog(
        uuid=catalog_uuid or str(_uuid.uuid4()),
        metadata=profile.metadata,
        params=list(source.params),
        controls=kept_controls,
        groups=kept_groups,
        back_matter=profile.back_matter or source.back_matter,
    )


# --------------------------------------------------------------------------- #
# endregion Resolver                                                          #
# --------------------------------------------------------------------------- #
