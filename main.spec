# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['neptunseye\\main.py'],
    pathex=['C:\\Users\\games\\.pyenv\\pyenv-win\\versions\\3.7.9', 'C:\\Users\\games\\.pyenv\\pyenv-win\\versions\\3.11.4'],
    binaries=[],
    datas=[
        ('D:\\programowanie\\python\\projekt_zespołowy\\neptuns-eye\\neptunseye\\config\\classes_definition.json', 'config'),
        ('D:\\programowanie\\python\\projekt_zespołowy\\neptuns-eye\\neptunseye\\locales\\*', 'locales'),
        ('D:\\programowanie\\python\\projekt_zespołowy\\neptuns-eye\\neptunseye\\resources\\neptuns-eye-logo.ico', 'resources')
    ],

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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
