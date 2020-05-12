import PyInstaller.__main__
import os
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir


class Shard(object):
    def __init__(self):
        pass

    def freeze(self, entrypoint, *args, **kwargs):
        shell_params = self._build_param_list(entrypoint, *args, **kwargs)
        try:
            with TemporaryDirectory(dir=gettempdir()) as build_dir:
                shell_params.append(f'--workpath={build_dir}')
                PyInstaller.__main__.run(shell_params)
        except Exception as e:
            print(e)

    def _build_param_list(self, entrypoint, *args, **kwargs):
        return [entrypoint] + list(args) + [
            f'{k}={v}' for k, v in kwargs.items()
            ] + self._data_tree(Path(entrypoint).parent)

    def _data_tree(self, entry):
        data = []
        entry_path = Path(entry)
        for root, _, files in self._walk_data(entry):
            root_path = Path(root)
            runtime_dir_path = Path('.')
            if entry_path.stem != root_path.stem:
                runtime_dir_path = runtime_dir_path.joinpath(root_path.relative_to(entry_path))
            for file in files:
                data.append(f'--add-data={root_path.joinpath(file)};{runtime_dir_path}')
        return data

    def _walk_data(self, entry):
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
    # shard.pull_dependencies(r'D:\Users\gfvan\Desktop\Dev\python\simple-py')


# PyInstaller.__main__.run([
#     '--name=%s' % package_name,
#     '--onefile',
#     '--windowed',
#     '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
#     '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
#     '--icon=%s' % os.path.join('resource', 'path', 'icon.ico'),
#     os.path.join('my_package', '__main__.py'),
# ])


# --runtime-tmpdir PATH