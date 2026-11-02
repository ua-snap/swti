# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for the macOS desktop app. Build with desktop/build_macos.sh.
# pylint: skip-file

from pathlib import Path

from PyInstaller.utils.hooks import copy_metadata

APP_NAME = "Alaska Statewide Temperature Index"
BUNDLE_ID = "edu.alaska.uaf.accap.swti"
VERSION = "1.0.0"

ROOT = Path(SPECPATH).parent

datas = [
    (str(ROOT / "assets"), "assets"),
    (str(ROOT / "data" / "StationsList.txt"), "data"),
    (str(ROOT / "data" / "normals.csv"), "data"),
    (str(ROOT / "data" / "test-daily-index.csv"), "data"),
]
for package in ("dash", "plotly", "flask", "werkzeug", "pywebview"):
    datas += copy_metadata(package)

a = Analysis(
    [str(ROOT / "desktop" / "swti_desktop.py")],
    pathex=[str(ROOT)],
    datas=datas,
    hiddenimports=["application", "gui", "luts", "data"],
    excludes=["tkinter", "matplotlib", "scipy", "IPython", "pytest", "PyQt5", "PyQt6", "PySide6"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="swti",
    console=False,
    argv_emulation=False,
    target_arch=None,
)
coll = COLLECT(exe, a.binaries, a.datas, name="swti")

app = BUNDLE(
    coll,
    name=f"{APP_NAME}.app",
    icon=str(ROOT / "desktop" / "swti.icns"),
    bundle_identifier=BUNDLE_ID,
    version=VERSION,
    info_plist={
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "LSApplicationCategoryType": "public.app-category.weather",
        "LSMinimumSystemVersion": "11.0",
        "NSHighResolutionCapable": True,
        "NSRequiresAquaSystemAppearance": True,
        "NSHumanReadableCopyright": "Alaska Center for Climate Assessment and Policy, University of Alaska Fairbanks",
        # The UI is served from the app's own localhost server.
        "NSAppTransportSecurity": {"NSAllowsLocalNetworking": True},
    },
)
