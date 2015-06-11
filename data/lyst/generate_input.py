#!/usr/bin/env python
import os
import random
try:
    from sparkey import HashReader
except ImportError:
    from spotify.sparkey import HashReader

spr = lambda (s): HashReader('%s.spi' % s, '%s.spl' % s)

fn = spr('/home/shumbody/data/terms_to_images_sample')

train_file = open('/home/qamar/cudamonster/caffe/data/lyst/train.txt', 'w')
test_file = open('/home/qamar/cudamonster/caffe/data/lyst/test.txt', 'w')

data = {}
for label, images in fn.iteritems():
    images = images.split(',')
    if len(images) <= 100:
        continue
    data[label.strip()] = images

map = dict([(lbl, idx) for idx, lbl in enumerate(data.keys())])
map_file = open('/home/qamar/cudamonster/caffe/data/lyst/map.txt', 'w')
for d in map.iteritems():
    map_file.write('%s %d\n' % d)
map_file.close()

tot = 0
fail = 0
for label, images in data.iteritems():
    for im in images:
        tot += 1
        path = '/home/qamar/data/lyst/%s/%s/%s.jpeg' % (im[0], im[1], im)
        if os.path.isfile(path):
            train_file.write('%s %s\n' % (path, map[label]))
            if random.random() < 0.01:
                pass
                test_file.write('%s %s\n' % (path, map[label]))
        else:
            fail += 1
            print 'this non-image file was deleted', path
        if tot % 100000 == 0:
            print 'total: %d, failed: %d' % (tot, fail)

print
print 'total: %d, failed: %d' % (tot, fail)

train_file.close()
test_file.close()
