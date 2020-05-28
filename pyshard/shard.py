import os
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir
from typing import Generator, List, Tuple

import PyInstaller.__main__


class Shard(object):
    """Main PyShard class - Comprises all freezing functionality"""
    def __init__(self):
        pass

    def freeze(self, entrypoint: str, *args: str, **kwargs: str) -> None:
        """Start freezing operation by calling pyinstaller executable, passing in
        parsed depency tree and user compiling specifications"""
        shell_params = self._build_param_list(entrypoint, *args, **kwargs)
        try:
            with TemporaryDirectory(dir=gettempdir()) as build_dir:
                shell_params.append(f'--workpath={build_dir}')
                PyInstaller.__main__.run(shell_params)
        except Exception as e:
            print(e)

    def _build_param_list(self, entrypoint: str, *args: str, **kwargs: str) -> List[str]:
        """Build pyinstaller parameter list from user input"""
        return [entrypoint] + list(args) + [
            f'{k}={v}' for k, v in kwargs.items()
        ] + self._data_tree(Path(entrypoint).parent) + self.__bundle_dlls()

    def _data_tree(self, entry: str) -> List[str]:
        """Generate recursive dependency tree starting from package entrypoint"""
        data = []
        entry_path = Path(entry)
        for root, _, files in self._walk_data(entry):
            root_path = Path(root)
            runtime_dir_path = Path('.')
            if entry_path.stem != root_path.stem:
                runtime_dir_path = runtime_dir_path.joinpath(
                    root_path.relative_to(entry_path))
            for file in files:
                data.append(
                    f'--add-data={root_path.joinpath(file)};{runtime_dir_path}')
        return data

    def __bundle_dlls(self) -> List[str]:
        """Bundle required visual C++ run-time dlls from Visual Studio 2015"""
        return [f'--add-binary={Path(__file__).parent.joinpath("crt_dlls", "*.dll")};.']

    def _walk_data(self, entry: str) -> Generator[Tuple[str, List[str], List[str]], None, None]:
        """Generate next walk step including only data files, source files will not be listed"""
        for root, dirs, files in os.walk(entry):
            dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__']]
            files[:] = [f for f in files if Path(f).suffix not in ['.py']]
            yield (root, dirs, files)


if __name__ == "__main__":
    shard = Shard()
    shard_args = ['./tests/sample_package.py',
                  '--noconfirm', '--clean', '--uac-admin']
    shard_kwargs = {'--distpath': './tests/dist/'}
    shard.freeze(*shard_args, **shard_kwargs)
