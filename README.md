# Pyshard

An ease-of-use, customized Pyinstaller wrapper made entirely in python.

**Features**

- Able to handle complex project structures by generating a recursive dependency tree of configuration and resource files, later parsed to a series of instructions which [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/index.html) can understand and use to properly reproduce the original directory hierarchy.

- Solves the infamous [Universal CRT](https://devblogs.microsoft.com/cppblog/introducing-the-universal-crt/) problem of missing dlls for Python >= 3.5 targeting Windows < 10 by automatically bundling the required Visual C++ run-time dlls from visual Studio 2015, which has been renamed into "Universal CRT" and is now part of Windows 10 core.

[See demo gif in full screen](https://raw.githubusercontent.com/northernSage/pyshard/master/resources/demogif.gif)

![shard_demo_gif](https://github.com/northernSage/pyshard/blob/master/resources/demogif.gif)