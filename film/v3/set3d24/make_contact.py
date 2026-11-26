"""contact.jpg (6 columns, 720x1280 tiles, label strip UNDER each image, cyan y-880 caption line) + contact_small.jpg (1/3)
from final/ in contact_order.txt order (name|label)."""
from PIL import Image, ImageDraw, ImageFont
rows_ = [l.strip().split('|') for l in open('contact_order.txt') if l.strip()]
W, H, LB, C = 720, 1280, 56, 6
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
rows = (len(rows_) + C - 1) // C
S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S)
for i, (n, lab) in enumerate(rows_):
    im = Image.open('joseon_work/final/%s.png' % n).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB)
    S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
    d.text((x + 12, y + H + 11), lab, fill=(235, 235, 235), font=F)
S.save('contact.jpg', quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save('contact_small.jpg', quality=88)
print(S.size, len(rows_))
