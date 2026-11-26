#!/usr/bin/env python3
"""mLRS project setup. Copyright (c) mLRS project, GPL-3.0.
Always run generators with the interpreter that launched this script.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(command, cwd, silent=False):
    print('\nRunning: ' + str(command[0]) + ' ' + ' '.join(map(str, command[1:])), flush=True)
    subprocess.run(list(map(str, command)), cwd=str(cwd), check=True,
                   stdout=subprocess.DEVNULL if silent else None)


def verify(paths):
    missing = [str(p) for p in paths if not p.is_file() or p.stat().st_size == 0]
    if missing:
        raise RuntimeError('Missing or empty generated files:\n' + '\n'.join(missing))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--silent', '--s', action='store_true')
    parser.add_argument('--nopause', '-np', action='store_true')
    parser.add_argument('--submodules', '-g', '-G', action='store_true')
    parser.add_argument('--copy', '-c', '-C', action='store_true')
    parser.add_argument('--mavlink', '-m', '-M', action='store_true')
    parser.add_argument('--dronecan', '-d', '-D', action='store_true')
    args = parser.parse_args(argv)
    everything = not any((args.submodules, args.copy, args.mavlink, args.dronecan))
    print('Project:', ROOT, flush=True)
    print('Python:', sys.executable, flush=True)
    try:
        if everything or args.submodules:
            run(['git', 'submodule', 'update', '--init', '--recursive'], ROOT, args.silent)
        if everything or args.copy:
            run([sys.executable, ROOT / 'tools/run_copy_st_drivers.py', '-silent'],
                ROOT / 'tools', args.silent)
        if everything or args.mavlink:
            folder = ROOT / 'mLRS/Common/mavlink'
            run([sys.executable, folder / 'fmav_generate_c_library.py'], folder, args.silent)
            verify([folder / 'out/mlrs_all/mlrs_all.h'])
        if everything or args.dronecan:
            folder = ROOT / 'mLRS/Common/dronecan'
            run([sys.executable, folder / 'dronecan_generate_c_library.py', '-np'], folder, args.silent)
            verify([folder / 'out/include/uavcan.protocol.NodeStatus.h',
                    folder / 'out/src/uavcan.protocol.NodeStatus.c',
                    folder / 'out/include/dronecan.sensors.rc.RCInput.h'])
    except (subprocess.CalledProcessError, OSError, RuntimeError) as exc:
        print('\nSETUP FAILED: ' + str(exc), file=sys.stderr)
        return 1
    print('\nSETUP OK', flush=True)
    if not args.nopause and sys.stdin.isatty():
        input('Press Enter to continue')
    return 0


if __name__ == '__main__':
    sys.exit(main())
