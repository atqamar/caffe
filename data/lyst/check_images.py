#!/usr/bin/env python
import os
import multiprocessing
try:
    from sparkey import HashReader
except ImportError:
    from spotify.sparkey import HashReader
from PIL import Image

spr = lambda (s): HashReader('%s.spi' % s, '%s.spl' % s)

fn = spr('/home/shumbody/data/terms_to_images_sample')

images = set()
for label, image in fn.iteritems():
    for i in image.split(','):
        images.add(i)

def is_PIL_compatible(path):
    try:
        image = Image.open(path)
        return True
    except:
        return False

def is_image(path):
    data = open(path, 'rb')
    bytes= data.read(11)
    data.close()
    if bytes[:4] != '\xff\xd8\xff\xe0':
        return False
    if bytes[6:] != 'JFIF\0':
        return False
    return True

def image_check(im):
    path = '/home/qamar/data/lyst/%s/%s/%s.jpeg' % (im[0], im[1], im)
    if not os.path.isfile(path):
        return
    if not is_image(path):
        print 'REMOVING INCOMPATIBLE IMAGE: %s' % path
        os.remove(path)

if __name__ == '__main__':
    pool = multiprocessing.Pool(multiprocessing.cpu_count() + 2)
    pool.map(image_check, images)
