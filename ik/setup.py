from distutils.core import setup, Extension

module = Extension('hex_ik', sources=["main.c"])

setup(
    name="hex_ik",
    version="1.0.0",
    ext_modules=[module]
)

