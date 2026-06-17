# Module name: oscal/models.py
# Author: (wattleflow@outlook.com)
# Copyright: © 2022–2026 WattleFlow. All rights reserved.
# License: Apache 2 Licence


# --------------------------------------------------------------------------- #
# region Imports                                                              #
# --------------------------------------------------------------------------- #
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Mapping, Optional
from wattleflow.core import IElement, IIterator, ISyncAggregate, IVisitor
# --------------------------------------------------------------------------- #
# endregion Imports                                                           #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Constants                                                            #
# --------------------------------------------------------------------------- #
__author__ = "WattleFlow"
__copyright__ = "© 2022–2026 WattleFlow. All rights reserved"

# OSCAL JSON uses kebab-case keys and the reserved Python word `class`.
# Map them to snake_case attribute names; everything else is converted by
# replacing '-' with '_'.
_KEY_ALIASES: Mapping[str, str] = {
    "class": "class_",
    "back-matter": "back_matter",
    "last-modified": "last_modified",
    "oscal-version": "oscal_version",
    "responsible-parties": "responsible_parties",
    "control-id": "control_id",
}
# --------------------------------------------------------------------------- #
# endregion Constants                                                         #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Helpers                                                              #
# --------------------------------------------------------------------------- #


def _normalise_key(key: str) -> str:
    if key in _KEY_ALIASES:
        return _KEY_ALIASES[key]
    return key.replace("-", "_")


def _normalise(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {_normalise_key(k): v for k, v in data.items()}


def _items(data: Optional[Mapping[str, Any]], key: str) -> List[Dict[str, Any]]:
    if not data:
        return []
    value = data.get(key, [])
    return list(value) if value else []


# --------------------------------------------------------------------------- #
# endregion Helpers                                                           #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Leaf types                                                           #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Prop:
    name: str
    value: str
    ns: Optional[str] = None
    class_: Optional[str] = None
    uuid: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Prop":
        n = _normalise(data)
        return cls(
            name=n["name"],
            value=n["value"],
            ns=n.get("ns"),
            class_=n.get("class_"),
            uuid=n.get("uuid"),
        )


@dataclass(frozen=True)
class Link:
    href: str
    rel: Optional[str] = None
    text: Optional[str] = None
    media_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Link":
        n = _normalise(data)
        return cls(
            href=n["href"],
            rel=n.get("rel"),
            text=n.get("text"),
            media_type=n.get("media_type"),
        )


@dataclass(frozen=True)
class Part:
    name: str
    id: Optional[str] = None
    class_: Optional[str] = None
    title: Optional[str] = None
    prose: Optional[str] = None
    props: List[Prop] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    parts: List["Part"] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Part":
        n = _normalise(data)
        return cls(
            name=n["name"],
            id=n.get("id"),
            class_=n.get("class_"),
            title=n.get("title"),
            prose=n.get("prose"),
            props=[Prop.from_dict(p) for p in _items(n, "props")],
            links=[Link.from_dict(p) for p in _items(n, "links")],
            parts=[Part.from_dict(p) for p in _items(n, "parts")],
        )


@dataclass(frozen=True)
class Param:
    id: str
    label: Optional[str] = None
    class_: Optional[str] = None
    values: List[str] = field(default_factory=list)
    props: List[Prop] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Param":
        n = _normalise(data)
        return cls(
            id=n["id"],
            label=n.get("label"),
            class_=n.get("class_"),
            values=list(n.get("values", []) or []),
            props=[Prop.from_dict(p) for p in _items(n, "props")],
        )


# --------------------------------------------------------------------------- #
# endregion Leaf types                                                        #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Tree nodes                                                           #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Control(IElement):
    id: str
    title: str
    class_: Optional[str] = None
    params: List[Param] = field(default_factory=list)
    props: List[Prop] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    parts: List[Part] = field(default_factory=list)
    controls: List["Control"] = field(default_factory=list)

    def __post_init__(self) -> None:
        # IWattleflow.__init__ would set self.name, but frozen dataclass __init__
        # never calls super; emulate it via object.__setattr__.
        object.__setattr__(self, "name", self.__class__.__name__)
        if not self.id:
            raise ValueError("Control.id must not be empty")
        if not self.title:
            raise ValueError(f"Control {self.id} has no title")

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Control":
        n = _normalise(data)
        return cls(
            id=n["id"],
            title=n["title"],
            class_=n.get("class_"),
            params=[Param.from_dict(p) for p in _items(n, "params")],
            props=[Prop.from_dict(p) for p in _items(n, "props")],
            links=[Link.from_dict(p) for p in _items(n, "links")],
            parts=[Part.from_dict(p) for p in _items(n, "parts")],
            controls=[Control.from_dict(c) for c in _items(n, "controls")],
        )

    def accept(self, visitor: IVisitor) -> None:
        visitor.visit(self)
        for child in self.controls:
            child.accept(visitor)


@dataclass(frozen=True)
class Group(IElement):
    title: str
    id: Optional[str] = None
    class_: Optional[str] = None
    params: List[Param] = field(default_factory=list)
    props: List[Prop] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    parts: List[Part] = field(default_factory=list)
    groups: List["Group"] = field(default_factory=list)
    controls: List[Control] = field(default_factory=list)

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.__class__.__name__)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Group":
        n = _normalise(data)
        return cls(
            title=n["title"],
            id=n.get("id"),
            class_=n.get("class_"),
            params=[Param.from_dict(p) for p in _items(n, "params")],
            props=[Prop.from_dict(p) for p in _items(n, "props")],
            links=[Link.from_dict(p) for p in _items(n, "links")],
            parts=[Part.from_dict(p) for p in _items(n, "parts")],
            groups=[Group.from_dict(g) for g in _items(n, "groups")],
            controls=[Control.from_dict(c) for c in _items(n, "controls")],
        )

    def accept(self, visitor: IVisitor) -> None:
        visitor.visit(self)
        for sub in self.groups:
            sub.accept(visitor)
        for control in self.controls:
            control.accept(visitor)


# --------------------------------------------------------------------------- #
# endregion Tree nodes                                                        #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Metadata / BackMatter                                                #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Metadata:
    title: str
    last_modified: str
    version: str
    oscal_version: str
    props: List[Prop] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Metadata":
        n = _normalise(data)
        return cls(
            title=n["title"],
            last_modified=n["last_modified"],
            version=n["version"],
            oscal_version=n["oscal_version"],
            props=[Prop.from_dict(p) for p in _items(n, "props")],
            links=[Link.from_dict(p) for p in _items(n, "links")],
        )


@dataclass(frozen=True)
class BackMatter:
    resources: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BackMatter":
        if not data:
            return cls()
        return cls(resources=list(data.get("resources", []) or []))


# --------------------------------------------------------------------------- #
# endregion Metadata / BackMatter                                             #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Catalog                                                              #
# --------------------------------------------------------------------------- #


class _ControlIterator(IIterator[Control]):
    def __init__(self, catalog: "Catalog") -> None:
        super().__init__()
        self._catalog = catalog

    def create_iterator(self) -> Iterator[Control]:
        return _walk_controls(self._catalog)


def _walk_controls(node: Any) -> Iterator[Control]:
    # Catalog has groups + controls; Group has groups + controls; Control has controls.
    controls = getattr(node, "controls", None) or []
    groups = getattr(node, "groups", None) or []
    for control in controls:
        yield control
        yield from _walk_controls(control)
    for group in groups:
        yield from _walk_controls(group)


@dataclass(frozen=True)
class Catalog(IElement, ISyncAggregate[Control]):
    uuid: str
    metadata: Metadata
    params: List[Param] = field(default_factory=list)
    controls: List[Control] = field(default_factory=list)
    groups: List[Group] = field(default_factory=list)
    back_matter: Optional[BackMatter] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.__class__.__name__)
        if not self.uuid:
            raise ValueError("Catalog.uuid must not be empty")

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Catalog":
        # Accept either a bare catalog object or the OSCAL wrapper {"catalog": {...}}.
        if "catalog" in data and isinstance(data["catalog"], Mapping):
            data = data["catalog"]
        n = _normalise(data)
        bm = n.get("back_matter")
        return cls(
            uuid=n["uuid"],
            metadata=Metadata.from_dict(n["metadata"]),
            params=[Param.from_dict(p) for p in _items(n, "params")],
            controls=[Control.from_dict(c) for c in _items(n, "controls")],
            groups=[Group.from_dict(g) for g in _items(n, "groups")],
            back_matter=BackMatter.from_dict(bm) if bm else None,
        )

    def create_iterator(self) -> IIterator[Control]:
        return _ControlIterator(self)

    def accept(self, visitor: IVisitor) -> None:
        visitor.visit(self)
        for control in self.controls:
            control.accept(visitor)
        for group in self.groups:
            group.accept(visitor)


# --------------------------------------------------------------------------- #
# endregion Catalog                                                           #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# region Profile                                                              #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class IncludeControls:
    """Selector inside a profile import that picks controls from the source
    catalog. ASD ISM profiles use ``with_ids`` exclusively; the matching/pattern
    forms are accepted but not exercised here.
    """

    with_ids: List[str] = field(default_factory=list)
    with_child_controls: Optional[str] = None
    matching: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "IncludeControls":
        n = _normalise(data)
        return cls(
            with_ids=list(n.get("with_ids", []) or []),
            with_child_controls=n.get("with_child_controls"),
            matching=list(n.get("matching", []) or []),
        )


@dataclass(frozen=True)
class Import:
    """A single ``imports`` entry inside a Profile.

    ``href`` may be a URI to an external catalog/profile or a fragment
    (``#uuid``) referring to a resource in the profile's ``back-matter``.
    """

    href: str
    include_all: Optional[Dict[str, Any]] = None
    include_controls: List[IncludeControls] = field(default_factory=list)
    exclude_controls: List[IncludeControls] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Import":
        n = _normalise(data)
        return cls(
            href=n["href"],
            include_all=n.get("include_all"),
            include_controls=[IncludeControls.from_dict(c) for c in _items(n, "include_controls")],
            exclude_controls=[IncludeControls.from_dict(c) for c in _items(n, "exclude_controls")],
        )

    def control_ids(self) -> List[str]:
        ids: List[str] = []
        for inc in self.include_controls:
            ids.extend(inc.with_ids)
        return ids


@dataclass(frozen=True)
class Merge:
    as_is: Optional[bool] = None
    combine: Optional[Dict[str, Any]] = None
    flat: Optional[Dict[str, Any]] = None
    custom: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Merge":
        n = _normalise(data)
        return cls(
            as_is=n.get("as_is"),
            combine=n.get("combine"),
            flat=n.get("flat"),
            custom=n.get("custom"),
        )


@dataclass(frozen=True)
class Profile(IElement):
    """An OSCAL Profile: a selector document that tailors a source catalog.

    Unlike ``Catalog``, a profile does not own controls directly; it
    references them via ``imports[*].include_controls[*].with_ids``.
    Resolution against a source catalog is a separate concern and is not
    performed here.
    """

    uuid: str
    metadata: Metadata
    imports: List[Import] = field(default_factory=list)
    merge: Optional[Merge] = None
    modify: Optional[Dict[str, Any]] = None
    back_matter: Optional[BackMatter] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.__class__.__name__)
        if not self.uuid:
            raise ValueError("Profile.uuid must not be empty")
        if not self.imports:
            raise ValueError(f"Profile {self.uuid} has no imports")

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Profile":
        if "profile" in data and isinstance(data["profile"], Mapping):
            data = data["profile"]
        n = _normalise(data)
        merge = n.get("merge")
        bm = n.get("back_matter")
        return cls(
            uuid=n["uuid"],
            metadata=Metadata.from_dict(n["metadata"]),
            imports=[Import.from_dict(i) for i in _items(n, "imports")],
            merge=Merge.from_dict(merge) if merge else None,
            modify=n.get("modify"),
            back_matter=BackMatter.from_dict(bm) if bm else None,
        )

    def control_ids(self) -> List[str]:
        """Flat list of all control IDs selected across all imports."""
        ids: List[str] = []
        for imp in self.imports:
            ids.extend(imp.control_ids())
        return ids

    def accept(self, visitor: IVisitor) -> None:
        visitor.visit(self)


# --------------------------------------------------------------------------- #
# endregion Profile                                                           #
# --------------------------------------------------------------------------- #
