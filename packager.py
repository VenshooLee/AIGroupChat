#!/usr/bin/env python3
"""
打包脚本 - 将应用打包为 Windows exe 和 macOS App
需要先安装 PyInstaller: pip install pyinstaller
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在安装 PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def get_pyinstaller():
    """确保 PyInstaller 已安装"""
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True)
    except FileNotFoundError:
        install_pyinstaller()

def create_spec_file():
    """创建 PyInstaller spec 文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('config.yaml', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=['flask', 'flask_cors', 'pymongo', 'requests', 'urllib3', 'certifi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GroupChat',
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
'''
    with open('GroupChat.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("已创建 GroupChat.spec")

def build_windows():
    """打包 Windows 版本"""
    print("\n" + "="*50)
    print("开始打包 Windows 版本...")
    print("="*50)

    if not os.path.exists('GroupChat.spec'):
        create_spec_file()

    # Windows 打包
    subprocess.run([
        'pyinstaller',
        '--name=GroupChat',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--add-data=config.yaml;.',
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=pymongo',
        '--hidden-import=requests',
        'run_app.py'
    ], shell=True)

    # 移动输出文件
    if os.path.exists('dist/GroupChat.exe'):
        shutil.copy('dist/GroupChat.exe', 'GroupChat-Windows.exe')
        print("Windows 版本已生成: GroupChat-Windows.exe")
        print("位置: " + os.path.abspath('GroupChat-Windows.exe'))

def build_macos():
    """打包 macOS 版本"""
    print("\n" + "="*50)
    print("开始打包 macOS 版本...")
    print("="*50)

    if not os.path.exists('GroupChat.spec'):
        create_spec_file()

    # macOS 打包
    subprocess.run([
        'pyinstaller',
        '--name=GroupChat',
        '--onefile',
        '--windowed',
        '--add-data=templates:templates',
        '--add-data=static:static',
        '--add-data=config.yaml:.',
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=pymongo',
        '--hidden-import=requests',
        'run_app.py'
    ])

    # 移动输出文件
    if os.path.exists('dist/GroupChat.app'):
        shutil.copy('dist/GroupChat.app', 'GroupChat-macOS.app')
        print("macOS 版本已生成: GroupChat-macOS.app")
        print("位置: " + os.path.abspath('GroupChat-macOS.app'))

def main():
    print("="*50)
    print("GroupChat 打包工具")
    print("="*50)

    # 确保 PyInstaller 已安装
    get_pyinstaller()

    # 获取当前平台
    current_platform = sys.platform

    print(f"\n当前平台: {current_platform}")

    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
    else:
        print("\n请选择打包目标:")
        print("1. Windows (.exe)")
        print("2. macOS (.app)")
        print("3. 同时打包两个平台")
        choice = input("\n请输入选择 (1/2/3): ").strip()
        target_map = {'1': 'windows', '2': 'macos', '3': 'both'}
        target = target_map.get(choice, 'both')

    if target in ['windows', 'both']:
        if current_platform.startswith('win') or 'windows' in target:
            build_windows()
        else:
            print("\n注意: Windows 打包需要在 Windows 系统上进行")
            print("或者使用 wine 等跨平台工具")

    if target in ['macos', 'both']:
        if current_platform.startswith('darwin') or 'macos' in target:
            build_macos()
        else:
            print("\n注意: macOS 打包需要在 macOS 系统上进行")

    print("\n" + "="*50)
    print("打包完成!")
    print("="*50)

if __name__ == '__main__':
    main()
