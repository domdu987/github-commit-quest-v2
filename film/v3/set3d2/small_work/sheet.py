import sys
from PIL import Image
def sheet(paths, out, cols=4, cell=(360, 640)):
    rows = (len(paths) + cols - 1) // cols; W, H = cell
    s = Image.new('RGB', (cols * (W + 6), rows * (H + 6)), (25, 25, 25))
    for i, p in enumerate(paths):
        s.paste(Image.open(p).convert('RGB').resize(cell, Image.LANCZOS), ((i % cols) * (W + 6), (i // cols) * (H + 6)))
    s.save(out, quality=88)
if __name__ == '__main__':
    sheet(sys.argv[2:], sys.argv[1], cols=min(4, len(sys.argv) - 2))
