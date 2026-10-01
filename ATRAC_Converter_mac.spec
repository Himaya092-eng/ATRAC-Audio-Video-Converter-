# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os


def collect_pkg(name):
    d, b, h = collect_all(name)
    return d, b, h

# Python packages used by the app.
datas = []
binaries = []
hiddenimports = [
    'PIL._tkinter_finder',
    'tkinterdnd2',
]

for pkg in ('customtkinter', 'tkinterdnd2', 'ytmusicapi', 'certifi'):
    try:
        d, b, h = collect_pkg(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

# macOS helper binaries are copied into the application bundle by the GitHub Actions job.
for name in ('ffmpeg', 'ffprobe', 'ffplay', 'yt-dlp', 'deno'):
    p = os.path.join('mac_tools', name)
    if os.path.isfile(p):
        binaries.append((p, '.'))

# Keep the source icon as a resource when present. Tk itself does not require it on macOS.
if os.path.isfile('ATRAC_v30.ico'):
    datas.append(('ATRAC_v30.ico', '.'))


a = Analysis(
    ['ATRAC_UI_v31_38_UNIFIED.pyw'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ATRAC_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='ATRAC_Converter',
)
