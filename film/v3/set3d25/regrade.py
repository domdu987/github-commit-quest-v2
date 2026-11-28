import sys, os, subprocess; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import front as F
H=os.path.dirname(os.path.abspath(__file__))
for n in sys.argv[1:]:
    F.post(f'{H}/{os.environ.get("RGDIR","finals")}/{n}_raw.png', f'/tmp/rg_{n}.png'); print(subprocess.run(['python3', H+'/../../film25/tools/light_metrics.py', f'/tmp/rg_{n}.png'], capture_output=True, text=True).stdout.strip())
