# -*- mode: python ; coding: utf-8 -*-
"""蜂巢 桌面客户端 macOS 打包配置（PyInstaller onedir）"""
from pathlib import Path

ROOT = Path(SPECPATH).resolve()

datas = [
    ("app", "app"),
    ("desktop/web", "desktop/web"),
    ("assets", "assets"),
    ("config.example.yaml", "."),
    ("requirements.txt", "."),
    ("desktop-version.txt", "."),
]
# 可选资源：存在才打包
for optional in ("guide", "preview", "frontend"):
    if (ROOT / optional).is_dir():
        datas.append((optional, optional))

# patchright 需要自带的 node driver 才能启动浏览器；PyInstaller 不会自动收集，
# 漏了会在 launch 时报 FileNotFoundError。
import patchright as _pw_pkg
_driver = Path(_pw_pkg.__file__).parent / "driver"
if _driver.is_dir():
    datas.append((str(_driver), "patchright/driver"))

hiddenimports = [
    # pywebview macOS 后端
    "webview.platforms.cocoa",
    "webview.http",
    "objc",
    # pystray macOS 后端
    "pystray._darwin",
    # uvicorn 动态选择
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.loops.asyncio",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.protocols.websockets.websockets_impl",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    # 数据库
    "sqlmodel",
    "sqlalchemy.dialects.sqlite",
    "sqlalchemy.dialects.postgresql",
    "aiosqlite",
    # 应用模块
    "app.main",
    "app.config",
    "app.db",
    "app.models",
    "desktop.launcher",
    "desktop.web_shell",
    "desktop.controller",
    "desktop.ui",
    "desktop.lifecycle",
]

a = Analysis(
    ["desktop/launcher.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter.test", "test", "unittest", "pydoc_data"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="蜂巢",
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
    icon="assets/hive.icns",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="蜂巢",
)

app = BUNDLE(
    coll,
    name="蜂巢.app",
    icon="assets/hive.icns",
    bundle_identifier="com.hive.creatorhub",
    info_plist={
        "CFBundleName": "蜂巢",
        "CFBundleDisplayName": "蜂巢",
        "CFBundleShortVersionString": "1.0.4",
        "CFBundleVersion": "1.0.4",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "11.0",
        "NSHumanReadableCopyright": "蜂巢 · 多平台获客工作台",
    },
)
