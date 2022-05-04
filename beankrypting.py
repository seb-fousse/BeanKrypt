from random import choice, randint
import textwrap
from os import path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# All bean images will have the same dimensions
WIDTH, HEIGHT = (512, 512)
PADDING = 12
FONT = ImageFont.load_default()

# Translate a value from one range to another
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return round(rightMin + (valueScaled * rightSpan))

# Round a R/G/B pixel value [0,255] to even
def round_to_even(num):
    if num % 2 == 0:
        return num
    else:
        return num - 1

# Round a R/G/B pixel value [0,255] to odd
def round_to_odd(num):
    if num % 2 != 0:
        return num
    else:
        return num + 1

# Generate a name for an image of beans
def generate_name():
    
    word1 = ['grandmas','aunties','my','your','forbidden','extra','stupidly']
    word2 = ['big','little','tangy','bougie','simple','humble','bad','delicious']
    
    text = ''
    
    if randint(1,6) != 6:
        text += choice(word1) + '_'
    if randint(1,6) != 6:
        text += choice(word2) + '_'
        
    text += 'beans_' + str(randint(1,1000)) + '_of_' + str(randint(1000,5000))
    
    return text

# Encode a piece of text into a given image, and return the encoded image
def encode(bean_img_path, text):

    bean_img = Image.open(bean_img_path, 'r')
    print(bean_img.size)

    # Font is monospaced, so will always have same dimensions
    char_w, char_h = FONT.getsize('1')
    line_length = int((WIDTH - PADDING) / char_w)
    text_height = int((HEIGHT - PADDING) / char_h)
    max_chars = line_length * text_height
    
    # Check if text to be encoded might be too long
    assert len(text) <= max_chars, "Text is too long"
    
    # Wrap text
    text = textwrap.fill(text=text, width=line_length)
    
    # Check if the wrapped text might be too long
    assert text.count('/n') < text_height, "Text is too long"
    
    # Create b&w image with text
    img = Image.new(size=(WIDTH,HEIGHT), mode='RGB')
    draw = ImageDraw.Draw(img)
    draw.text(xy=(PADDING / 2, PADDING / 2), text=text, font=FONT, fill="#FFFFFF")
    
    # Get bean and text images as pixel array
    new_img = bean_img.copy()
    bean_array = np.array(list(new_img.getdata()))
    img_array = np.array(list(img.getdata()))
    n = len(bean_array[0])
    
    # For each pixel in the bean and text image
    for idx, (bean_pix, img_pix) in enumerate(zip(bean_array, img_array)):
        
        # If there is a pixel representing text, round the R value to odd
        if np.array_equal(img_pix, [255, 255, 255]):
            bean_array[idx][0] = round_to_odd(bean_pix[0])
        else: # Round the R value to even
            bean_array[idx][0] = round_to_even(bean_pix[0])
    
    # Reshape array and turn into image
    bean_array = np.reshape(np.array(bean_array, dtype=np.uint8), (WIDTH, HEIGHT, n))
    if n == 3:
        encoded_img = Image.fromarray(bean_array, mode='RGB')
    elif n == 4:
        encoded_img = Image.fromarray(bean_array, mode='RGBA')
    else:
        raise Exception(f'Error: Pixel in array has {n} values. Cannot save as RGB or RGBA')
    
    return encoded_img

# Decode an image that was previously encoded with the encode function, return decoded image filepath
def decode(encoded_img):
    
    #encoded_img = Image.open(encoded_img_path, mode='r')
    encoded_img = Image.open(encoded_img, mode='r')

    # Get encoded img as a pixel array
    encoded_array = np.array(list(encoded_img.getdata()))
    n = len(encoded_array[0])
    
    print(encoded_array.shape)

    # Logic to handle images that have/don't have an alpha channel
    pix = []
    if n == 3:
        pix = [255,255,255]
    elif n == 4:
        pix = [255,255,255,255]
    else:
        raise Exception(f'Error: Pixel in array has {n} values')

    # Create blank image array
    blank_array = np.full(encoded_array.shape, pix)

    # Update blank image array
    for idx, encoded_pix in enumerate(encoded_array):
        if encoded_pix[0] % 2 != 0:
            blank_array[idx] = [0,0,0] if n == 3 else [0,0,0,255]
        else:
            blank_array[idx] = [translate(x, 0, 255, 200, 255) for x in encoded_pix]
            
    # Convert image array into an iamge
    nonblank_array = np.reshape(np.array(blank_array, dtype=np.uint8), (WIDTH, HEIGHT, n))
    if n == 3:
        decoded_img = Image.fromarray(nonblank_array, mode='RGB')
    elif n == 4:
        decoded_img = Image.fromarray(nonblank_array, mode='RGBA')
    else:
        raise Exception(f'Error: Pixel in array has {n} values. Cannot save as RGB or RGBA')
    
    return decoded_img