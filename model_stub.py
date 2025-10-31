from PIL import Image, ImageFilter, ImageEnhance

def apply_aging(img: Image.Image, years: int) -> Image.Image:
    w, h = img.size
    # scale the dog slightly as it gets older (synthetic growth)
    scale = 1.0 + min(years / 30.0, 0.6)
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # crop or pad back to original canvas center
    canvas = Image.new('RGB', (w, h), (240,240,240))
    x = max(0, (w - new_w)//2)
    y = max(0, (h - new_h)//2)
    canvas.paste(img, (x, y))
    img = canvas

    # apply aging effects
    if years < 2:
        enh = ImageEnhance.Color(img)
        img = enh.enhance(1.2)
    else:
        enh = ImageEnhance.Color(img)
        img = enh.enhance(max(0.6, 1.0 - years * 0.02))
        img = img.filter(ImageFilter.GaussianBlur(radius=min(2, years*0.05)))
        enh2 = ImageEnhance.Brightness(img)
        img = enh2.enhance(max(0.85, 1.0 - years * 0.01))
    return img
