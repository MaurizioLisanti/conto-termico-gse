"""Shared pytest configuration for conto-termico-gse tests."""
import sys
import os
from types import ModuleType
from unittest.mock import MagicMock

# Stub the elysia package so tools.py can be imported without the real
# dependency.  The pure module-level functions under test (_verifica_ammissibilita,
# _stima_incentivo) never touch Elysia internals.
_elysia = ModuleType("elysia")
_elysia.tool = lambda *args, **kwargs: (lambda f: f)
_elysia.Error = MagicMock
_elysia.Tree = MagicMock
sys.modules["elysia"] = _elysia

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
