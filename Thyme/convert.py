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

shutil.copytree(src_public_path, dst_public_path, dirs_exist_ok=True)
