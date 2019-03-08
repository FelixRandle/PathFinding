"""Utility functions for PathFinding application."""
import sys
import os


def getResourcePath(relativePath):
    """Get a resources path when using an executable file."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativePath)
    return os.path.join(os.path.abspath("."), relativePath)
