from PIL import Image, ImageDraw, ImageFont, ImageMath, ImageStat, ImageFilter
import json
import numpy as np

default_width = 662
default_height = 993

def draw_title(draw, title, font):
    w, _ = draw.textsize(title, font=font)
    draw.text(((default_width-w)/2,140), title, fill=(255,255,255,255), font=font)

def draw_level(draw, level, font):
    w, _ = draw.textsize(level, font=font)
    draw.text(((default_width-w)/2,70), level, fill=(255,255,255,255), font=font)

def draw_description(draw, description, font, avoid_layers, x, y):
    # print(description.split())
    description = [''] + description.split()
    avoid_layers_np = np.asarray(avoid_layers.filter(ImageFilter.BoxBlur(5)))
    
    for i in range(len(description)):
        img = Image.new('RGBA', (default_width, default_height), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.multiline_text((x,y), ' '.join(description[:i+1]), fill=(255,255,255,255), font=font)

        text_layer = np.asarray(img)

        img_product = text_layer & avoid_layers_np
        nbof_common_pixels = np.sum(img_product[:,:,3])

        if nbof_common_pixels > 0:
            if i == 10:
                Image.fromarray(img_product).show()
            description[i-1] += '\n'
            print(f'Bad {i}: {nbof_common_pixels}')
    draw.multiline_text((x,y), ' '.join(description), fill=(0, 0, 0, 255), font=font)

def draw_badstuff(draw, bad_stuff, font):
    draw.multiline_text((65, 400), bad_stuff, fill=(255,255,255,255), font=font)

def draw_treasures(draw, treasures, font):
    txt = f'Treasures: {treasures}'
    w, h = font.getsize(txt)
    margin_w = 20
    margin_h = 10
    x_start = default_width - 60 - margin_w - w
    y_start = default_height - 60 - margin_h - h
    draw.multiline_text((x_start, y_start), txt, font=font)

if __name__ == '__main__':
    cards = json.load(open('./cards.json'))
    door_frame = './imgs/door_front.png'
    for c in cards['cards']:
        if c['type'] == 'door':
            frame = Image.open(door_frame)
            background = Image.new('RGBA', (default_width, default_height), color='green')

        img = Image.new('RGBA', (default_width, default_height))
        
        draw = ImageDraw.Draw(img)
        title_font = ImageFont.truetype('./fonts/dreadringer.ttf', 50)
        level_font = ImageFont.truetype('./fonts/dreadringer.ttf', 40)
        text_font = ImageFont.truetype('./fonts/dreadringer.ttf', 35)

        element = Image.new('RGBA', (default_width, default_height), (0,0,0,0))
        element.paste(Image.open(c['element']['path']), (c['element']['x'], c['element']['y']))
        
        foreground = element
        foreground.paste(frame, (0,0), frame)

        draw_level(draw, f'Level {c["level"]}', level_font)
        draw_title(draw, c['title'], title_font)
        print(type(c['description']))

        draw_description(draw, c['description'], text_font, foreground, 65, 250)
        draw_description(draw, f"Bad Stuff: {c['bad_stuff']}", text_font, foreground, 65, 500)

        # draw_badstuff(draw, f"Bad Stuff: {c['bad_stuff']}", text_font)
        draw_treasures(draw, c['treasures'], text_font)

        out = background
        out.paste(img, (0,0), img)
        out.paste(foreground, (0,0), foreground)
        out.show()

    print('kek')