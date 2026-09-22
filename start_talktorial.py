import os, shutil, subprocess, sys
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)
runner_bin = Path(sys.executable).parent
os.environ["PATH"] = os.pathsep.join([str(runner_bin / "Scripts"), str(runner_bin), os.environ.get("PATH", "")])

from teachopencadd.cli import _find_or_fetch_talktorial, _parse_t_id
from teachopencadd.config import settings
from teachopencadd.env import configure_env
from teachopencadd.jupyter import setup_jupyter

if len(sys.argv) < 2:
    sys.exit("Bitte Talktorial-Nummer angeben, z. B.:  .\\start.ps1 2")

t_id = _parse_t_id(sys.argv[1])
talk = _find_or_fetch_talktorial(t_id, settings)
env = configure_env(t_id, talk.req_file, settings)
setup_jupyter(env, talk.nb_file)

py = str(env.py_exe)
subprocess.run(["uv", "pip", "install", "--python", py, "ipykernel"], check=True)
subprocess.run([py, "-m", "ipykernel", "install", "--user", "--name", env.name.lower(),
                "--display-name", f"TeachOpenCADD {t_id}"], check=True)

nb = talk.nb_file.resolve()
code = shutil.which("code")
if code:
    subprocess.run([code, "-r", str(nb)])
print(f"\nFertig: {t_id} bereit. Falls noetig: Strg+Shift+P > Developer: Reload Window, dann Kernel 'TeachOpenCADD {t_id}' waehlen.")
