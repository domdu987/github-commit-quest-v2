"""contact.jpg (9 columns, 720x1280 tiles, label strip, cyan y-880 caption line) + contact_small.jpg (1/3) from final/ in contact_order.txt order."""
from PIL import Image, ImageDraw
names = open('contact_order.txt').read().split()
W, H, LB, C = 720, 1280, 18, 9
rows = (len(names) + C - 1) // C
S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S)
for i, n in enumerate(names):
    f = ('final/%s.png' % n) if not n.startswith('REF') else '%s.jpg' % n
    im = Image.open(f).convert('RGB').resize((W, H)); x, y = (i % C) * W, (i // C) * (H + LB)
    S.paste(im, (x, y + LB)); d.text((x + 4, y + 3), n, fill=(230, 230, 230))
    if not n.startswith('REF'): d.line([(x, y + LB + 880), (x + W, y + LB + 880)], fill=(0, 230, 255), width=2)
S.save('../contact.jpg', quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save('../contact_small.jpg', quality=88)
print(S.size, len(names))
