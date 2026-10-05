"""Shared paths and external programs for the build tools.

Every script is run from the repository root. External programs are found automatically; override with
environment variables if needed:
  VCCI_EDGE      path to msedge.exe (or chrome.exe) used for headless HTML -> PNG/PDF rendering
  VCCI_PDFTOPPM  path to Poppler's pdftoppm, used for PDF -> PNG previews
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, 'build')          # intermediate files (git-ignored)
ASSETS = os.path.join(ROOT, 'brand-assets')  # deliverables


def _find(env, names, candidates):
    if os.environ.get(env):
        return os.environ[env]
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    for c in candidates:
        c = os.path.expandvars(c)
        if os.path.exists(c):
            return c
    return names[0]


EDGE = _find('VCCI_EDGE', ['msedge', 'chrome'], [
    r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe',
    r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe',
    r'%ProgramFiles%\Google\Chrome\Application\chrome.exe',
])
PDFTOPPM = _find('VCCI_PDFTOPPM', ['pdftoppm'], [
    r'%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdftoppm.exe',
    r'%ProgramFiles%\MiKTeX\miktex\bin\x64\pdftoppm.exe',
])


def build(*parts, mkdir=True):
    """Path inside build/; creates the parent folder."""
    p = os.path.join(BUILD, *parts)
    if mkdir:
        os.makedirs(os.path.dirname(p) if os.path.splitext(p)[1] else p, exist_ok=True)
    return p
