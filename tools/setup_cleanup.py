"""Cleanup of generated mLRS outputs only. GPL-3.0, mLRS-SensorLink.

Supports Windows read-only files and reports locked paths without concealing
an earlier deletion error behind FileExistsError.
"""
import os
from pathlib import Path
import shutil
import stat
import time

ROOT = Path(__file__).resolve().parent.parent


def _remove_readonly(func, name, exc_info):
    error = exc_info[1]
    # Do not change permissions for arbitrary errors such as sharing violations.
    if not isinstance(error, PermissionError) or getattr(error, 'winerror', None) in (32, 33):
        raise error
    mode = os.lstat(name).st_mode
    if stat.S_ISLNK(mode) or mode & stat.S_IWRITE:
        raise error
    os.chmod(name, mode | stat.S_IWRITE)
    func(name)


def reset_generated_dir(path):
    target = Path(os.path.abspath(os.fspath(path)))
    allowed = {ROOT / 'mLRS/Common/mavlink/out', ROOT / 'mLRS/Common/dronecan/out'}
    if target not in allowed:
        raise ValueError('Refusing cleanup outside the two generated out directories: ' + str(target))
    # Resolve parents too: never follow a linked project subdirectory to another location.
    if target.resolve() != target:
        raise ValueError('Refusing linked output path: ' + str(target))
    for attempt in range(4):
        try:
            if target.exists():
                if not target.is_dir():
                    raise RuntimeError('Output path is a file, not a directory: ' + str(target))
                shutil.rmtree(target, onerror=_remove_readonly)
            target.mkdir()
            return
        except OSError as exc:
            # A short retry may handle a scanner releasing a generated file.
            if attempt < 3 and (isinstance(exc, PermissionError) or getattr(exc, 'winerror', None) in (32, 33, 145)):
                time.sleep(0.25 * (attempt + 1))
                continue
            blocked = getattr(exc, 'filename', None) or str(target)
            raise RuntimeError(
                'Cannot reset generated directory: ' + str(target) + '\n'
                'Affected path: ' + str(blocked) + '\n'
                'Original error: ' + str(exc) + '\n'
                'Stop builds/monitors and any sync job accessing this folder; '
                'check permissions, then rerun setup. No success was reported.'
            ) from exc
