"""Run the Ren'Py Android build with bounded retries for Windows sharing locks."""
import argparse
import os
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, default=ROOT.parents[1])
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    # Solo reintentar la eliminación que el SDK ya realiza en su carpeta temporal.
    # No ocultar otros errores ni ampliar las rutas que puede borrar el compilador.
    temporary = (sdk / "tmp").resolve()
    original_rmdir = os.rmdir

    def retry_rmdir(path, *positional, **keyword):
        resolved = Path(path).resolve()
        for attempt in range(41):
            try:
                return original_rmdir(path, *positional, **keyword)
            except OSError as error:
                if (getattr(error, "winerror", None) != 32 or attempt == 40
                        or not resolved.is_relative_to(temporary)):
                    raise
                time.sleep(0.05)

    os.rmdir = retry_rmdir
    sys.path.insert(0, str(sdk))
    sys.argv = [str(sdk / "renpy.py"), str(sdk / "launcher"), "android_build",
                str(ROOT), "--destination", str(ROOT / "dist")]
    try:
        runpy.run_path(str(sdk / "renpy.py"), run_name="__main__")
    finally:
        os.rmdir = original_rmdir


if __name__ == "__main__":
    main()
