from thyme import make_archieve, make_til, make_writings, preserve_hierachy, root_path
import shutil
import os
from pathlib import Path
from subprocess import run

make_writings()
make_archieve()
make_til()
preserve_hierachy()

src_public_path = os.path.join(root_path, "public")
dst_public_path = os.path.join(Path(root_path).parent, "blog")

for path in list(filter(lambda x: x[0] != ".", os.listdir(dst_public_path))):
    target = os.path.join(dst_public_path, path)
    if os.path.isfile(target) or os.path.islink(target):
        os.remove(target)
    elif os.path.isdir(target):
        shutil.rmtree(target)

shutil.copytree(src_public_path, dst_public_path, dirs_exist_ok=True)
