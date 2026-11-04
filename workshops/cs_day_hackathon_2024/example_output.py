"""Console output and portable plot/map files for the examples."""
from pathlib import Path
from itertools import count
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT = Path("outputs") / Path(sys.argv[0]).stem
OUTPUT.mkdir(parents=True, exist_ok=True)
_sequence = count(1)

def save_plots(*args, **kwargs):
    for number in plt.get_fignums():
        path = OUTPUT / f"figure-{next(_sequence):03d}.png"
        plt.figure(number).savefig(path, bbox_inches="tight")
        print(f"Figure: {path.resolve()}")
    plt.close("all")

plt.show = save_plots

def display(*values):
    for value in values:
        if value is None:
            continue
        if hasattr(value, "get_root") and hasattr(value, "save"):
            path = OUTPUT / f"map-{next(_sequence):03d}.html"
            value.save(str(path))
            print(f"Map: {path.resolve()}")
        elif hasattr(value, "flat_graph"):
            import json
            print(json.dumps(value.flat_graph(), indent=2))
        elif isinstance(value, bytes):
            print(f"Downloaded {len(value)} bytes")
        else:
            print(value)
