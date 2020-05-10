import PyInstaller.__main__
import os
from pathlib import Path


class Shard(object):
    def __init__(self):
        pass

    def freeze(self, entrypoint, *args, **kwargs):
        shell_params = [entrypoint] + list(args) + [
            f'{k}={v}' for k, v in kwargs.items()] + self._dependency_tree(Path(entrypoint).parent)
        print(shell_params)
        try:
            PyInstaller.__main__.run(shell_params)
        except Exception as e:
            print(e)

    def _dependency_tree(self, entrydir):
        data = []
        for root, _, files in self._walk_data(entrydir):
            if Path(entrydir).stem == Path(root).stem:
                runtime_dir = '.'
            else:
                runtime_dir = Path(root).stem
            for file in files:
                arg = f'--add-data={Path(root).joinpath(file)};{runtime_dir}'
                data.append(arg)
        return data

    def _walk_data(self, entrydir):
        for root, dirs, files in os.walk(entrydir):
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
