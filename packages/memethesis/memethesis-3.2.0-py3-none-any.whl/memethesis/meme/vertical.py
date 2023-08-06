from PIL import Image, ImageDraw
import yaml
from ..fancyprint import color
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from ..fonts import *
from .imageops import stack
from ..format_utils import read_formats
from os import path
import sys

FORMATS = read_formats()

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)


def make_vertical(format: str, entities: list, cmdfont=None):
    format_info = FORMATS[format]
    if not format_info['composition'] == 'vertical':
        print(color(
            f'Error: meme format `{format}` is not vertically stacked.',
            fgc=1))
        sys.exit(1)

    panels = format_info['panels']

    global_font = get_fontpath(
        format_info['font'] if 'font' in format_info
        else 'notosans')
    global_style = format_info['style'] if 'style' in format_info else None

    meme_width = Image.open(path.join(  # width of an arbitrary panel
        path.dirname(__file__), 'res/template',
        list(panels.values())[0]['image'])).size[0]
    generated_panels = []

    for name, text in entities:
        # (identifier, text) or its list equivalent
        if name in panels.keys():
            meta = panels[name]

            if not cmdfont:
                font = (get_fontpath(meta['font'])
                        if 'font' in meta else global_font)
                style = (meta['style']
                         if 'style' in meta else global_style)
            else:
                font = get_fontpath(cmdfont)
                style = 'stroke' if cmdfont in IMPLY_STROKE else ''

            temp = Image.open(path.join(
                path.dirname(__file__),
                'res/template', meta['image']))

            text = make_text(
                text, box=meta['textbox'][2:], font_path=font,
                stroke=BLACK if style == 'stroke' else None)
            temp.paste(text, box=meta['textbox'][:2], mask=text)
            generated_panels.append(temp)

        elif name == 'caption':
            # assumes constant widths
            generated_panels.append(
                make_caption(text=text, width=meme_width, font=global_font,
                             stroke=BLACK if global_style == 'stroke' else None))

        elif name == 'sep':
            generated_panels.append(
                make_sep(width=meme_width))

    return stack(generated_panels)
