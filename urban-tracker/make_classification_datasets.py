
import sqlite3
import pprint as pp
import os
import shutil
import sys
from distutils.dir_util import copy_tree

from PIL import Image
from lxml import etree as ET

'''
Creates UT classification datasets using classification metadata of form
frame_number, frame_path, type_general, num_objects, object_id1, object_id2, ...

dest_base /
    sherbrooke /
        car/
            0/
                0001-sherbrooke-car.jpg
            1/
                0001-sherbrooke-car.jpg
                0002-sherbrooke-car.jpg
            2/
                0002-sherbrooke-car.jpg
                0003-sherbrooke-car.jpg
            negatives/
                0004-sherbrooke-car.jpg

Assumes 'dest_base' exists
Overwrites `dest_dir`
'''

def make_datasets(metadata_file, type_str, images_dir, dest_dir, identifier):

    # Create directory hierarchy
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    type_dir = os.path.join(dest_dir, type_str)
    os.makedirs(type_dir)

    tmp_dir = os.path.join(dest_dir, "tmp_images")
    os.makedirs(tmp_dir)

    # Copy images in images_dir to tmp_dir
    copy_tree(images_dir, tmp_dir)

    # Move positive images to respective object_id dirs
    # There will be repeats between dirs, with the same filename
    with open(metadata_file) as f:
        for line in f:
            values = line.rstrip().split(',')
            frame_prefix = values[1]
            type_general = values[2]
            num_objects = int(values[3])
            object_ids = values[4:]
            if type_general == type_str:
                for object_id in object_ids:
                    object_dir = os.path.join(type_dir, object_id)
                    if not os.path.exists(object_dir):
                        os.makedirs(object_dir)
                    old_frame_path = os.path.join(tmp_dir,
                                                  frame_prefix + ".jpg")
                    new_frame_path = os.path.join(object_dir,
                                                  identifier + "-" + \
                                                  type_str + "-" + \
                                                  frame_prefix + ".jpg")
                    if os.path.exists(old_frame_path):
                        shutil.move(old_frame_path, new_frame_path)

        # Move remaining images to negatives dir
        negatives_dir = os.path.join(type_dir, "negatives")
        os.makedirs(negatives_dir)
        for filename in os.listdir(tmp_dir):
            old_frame_path = os.path.join(tmp_dir, filename)
            new_frame_path = os.path.join(negatives_dir,
                                          identifier + "-" + \
                                          type_str + "-" + \
                                          filename)
            shutil.move(old_frame_path, new_frame_path)

    print "Images sorted in %s" % (type_dir)
                                        
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    base = '/datasets/BigLearning/ahjiang/bb/urban-tracker/'
    dest_base = '/datasets/BigLearning/ahjiang/image-data/instances/'

    images_dir = os.path.join(base, 'rouen/rouen_masked_frames')
    dest_dir = os.path.join(dest_base, 'rouen/')
    t1  = 'car'
    t2 = 'pedestrian'
    metadata_file = os.path.join(base, 'rouen/rouen_annotations/presence_metadata.csv')
    make_datasets(metadata_file, t1, images_dir, dest_dir, "rouen")
    make_datasets(metadata_file, t2, images_dir, dest_dir, "rouen")

    images_dir = os.path.join(base, 'stmarc/stmarc_masked_frames')
    dest_dir = os.path.join(dest_base, 'stmarc/')
    t1 = 'car'
    t2 = 'pedestrian'
    t3 = 'bike'
    metadata_file = os.path.join(base, 'stmarc/stmarc_annotations/presence_metadata.csv')
    make_datasets(metadata_file, t1, images_dir, dest_dir, "stmarc")
    make_datasets(metadata_file, t2, images_dir, dest_dir, "stmarc")

    images_dir = os.path.join(base, 'sherbrooke/sherbrooke_masked_frames')
    dest_dir = os.path.join(dest_base, 'sherbrooke/')
    t1  = 'car'
    t2 = 'pedestrian'
    metadata_file = os.path.join(base, 'sherbrooke/sherbrooke_annotations/presence_metadata.csv')
    make_datasets(metadata_file, t1, images_dir, dest_dir, "sherbrooke")
    make_datasets(metadata_file, t2, images_dir, dest_dir, "sherbrooke")

    images_dir = os.path.join(base, 'atrium/atrium_frames')
    dest_dir = os.path.join(dest_base, 'atrium/')
    t1 = 'pedestrian'
    metadata_file = os.path.join(base, 'atrium/atrium_annotations/presence_metadata.csv')
    make_datasets(metadata_file, t1, images_dir, dest_dir, "atrium")

