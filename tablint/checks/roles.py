"""Shared column-role lookup for checks."""

from __future__ import annotations


def column_roles(analyzer) -> dict[str, str]:
    """Return analyzer.column_roles, inferring them for direct check callers."""
    roles = getattr(analyzer, "column_roles", None)
    if roles is not None:
        return roles

    from ..utils.type_inference import infer_roles, infer_types

    config = getattr(analyzer, "config", None)
    types = getattr(analyzer, "column_types", None)
    if types is None:
        types = infer_types(analyzer.df, config=config)
        analyzer.column_types = types
    roles = infer_roles(
        analyzer.df,
        types,
        target_col=getattr(analyzer, "target_col", None),
        config=config,
    )
    analyzer.column_roles = roles
    return roles


def columns_with_roles(analyzer, *roles: str) -> list[str]:
    """Column names whose role is one of ``roles``, in frame order."""
    mapping = column_roles(analyzer)
    wanted = set(roles)
    return [col for col in analyzer.df.columns if mapping.get(col) in wanted]
