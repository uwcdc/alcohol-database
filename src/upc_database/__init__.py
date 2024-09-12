from __future__ import annotations

from ._version import version as VERSION  # type: ignore[import-not-found]

from .models import Products

__version__ = VERSION
__author__ = "Cordero Core"

__all__ = [
    "Products"
    ]
