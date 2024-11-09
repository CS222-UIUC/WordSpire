# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\aidan\\Desktop\\WordSpire\\Game\\Front_end.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\aidan\\Desktop\\WordSpire\\Game\\__init__.py', '.'), ('C:\\Users\\aidan\\Desktop\\WordSpire\\Game\\Back_end.py', '.'), ('C:\\Users\\aidan\\Desktop\\WordSpire\\Game\\__pycache__', '__pycache__/'), ('C:\\Users\\aidan\\Desktop\\WordSpire\\misc', 'misc/'), ('C:\\Users\\aidan\\Desktop\\WordSpire\\venv', 'venv/'), ('C:\\Users\\aidan\\Desktop\\WordSpire\\.vscode', '.vscode/')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='Front_end',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
