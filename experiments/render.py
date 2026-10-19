import re
import sys
from pathlib import Path

MARKER = re.compile(r"<!-- include:([\w.-]+) -->")


def render(template, fragments):
    return MARKER.sub(lambda m: (fragments / f"{m.group(1)}.md").read_text().rstrip(), template)


if __name__ == "__main__":
    source, fragments, target = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    target.write_text(render(source.read_text(), fragments))
