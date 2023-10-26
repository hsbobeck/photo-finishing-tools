"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ["GUI.py"]
APP_NAME = "Henry's Photo Finishing Tools"
DATA_FILES = []
OPTIONS = {
    "iconfile": "assets/favicon/macos-512x512.icns",
    "plist": {
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleGetInfoString": "python app for photo finishing",
        "CFBundleIdentifier": "com.henrybobeck.osx.photo-finishing-tools",
        "CFBundleVersion": "0.1.0",
        "CFBundleShortVersionString": "0.1.0",
        "NSHumanReadableCopyright": "Copyright © 2023, Henry Bobeck LLC, All Rights Reserved",
    },
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
