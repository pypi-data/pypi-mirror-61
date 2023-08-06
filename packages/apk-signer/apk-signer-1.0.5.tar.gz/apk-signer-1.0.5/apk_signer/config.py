import shutil
from pathlib import Path

p = Path(__file__)
ROOT_DIR = p.parent.resolve()
TEMP_DIR = ROOT_DIR.joinpath('temp')

APKTOOL = JAVA = None
binaries = ['apksigner', 'zipalign', 'adb']
for binary in binaries:
    path = shutil.which(binary)
    if not path:
        raise Exception("Please download and set to your environment this file: " + binary)

    locals()[binary] = path

JAVA_JAR = [JAVA, '-jar']
