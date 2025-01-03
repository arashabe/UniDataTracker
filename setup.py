import sys
from cx_Freeze import setup, Executable

include_files = ['config.ini', 'UniDataTracker.ico']

build_exe_options = {
    "packages": ["os","pyodbc"],
    "excludes": ["tkinter"],
    'include_files': include_files}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="StudentTrackApp",
    author="Arash A.",
    version="2025.1",
    description="An application to manage and track student information using SQL Server and PyQt5.",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "ssms.py",
            icon="UniDataTracker.ico",
            copyright="Copyright (C) 2025 Arash A.",

            base=base
        )
    ],
)

# pip install cx_Freeze
# python setup.py bdist_msi
# simple windows installer - python setup.py bdist_msi
# https://cx-freeze.readthedocs.io/en/latest/setup_script.html

