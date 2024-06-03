# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
     pathex=[
        'E:\GitHub\neptuns-eye-official\neptunseye',
        '%USERPROFILE%\.pyenv\pyenv-win\versions\3.11.9\*'
    ],
    binaries=[],
    datas=[
        ('config/*', 'config'),
        ('locales/*', 'locales'),
        ('resources/*', 'resources'),
        ('resources/models/*', 'resources/models')
    ],
    hiddenimports=[
        'classification_frame',
        'classification_utils',
        'file_frame',
        'las_handler',
        'visualisation_frame',
    ],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    upx=True,
    upx_exclude=[],
    name='main',
)