
import sqlite3
import pprint as pp
import os

from PIL import Image
from lxml import etree as ET

'''
Converts Urban Tracker annotations to Pascal VOC format
'''

############################# SCHEMA #################################

# Tables
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# objects, objects_type, bounding_boxes

# objects
# object_id, road_user_type, description

# objects_type
# road_user_type, type_string

# bounding_boxes
# object_id, frame_number, x_top_left, y_top_left, x_bottom_right, y_bottom_right

######################################################################

def get_annotations(sqlite_files, general_types, image_dirs):

    # frame_number: [{type,
    #                 type_general, 
    #                 image_file_prefix, 
    #                 [xmin, ymin, xmax, ymax]}]

    annotations = {}

    for sqlite_file, type_general, image_dir in zip(sqlite_files,
                                                    general_types,
                                                    image_dirs):

        print sqlite_file

        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bounding_boxes;")
        bbs = cursor.fetchall() #objects, objects_type, bounding_boxes

        for bb in bbs:
            object_id = bb[0]
            frame_number = bb[1]

            file_prefix = str(frame_number).zfill(8)
            frame_path = os.path.join(image_dir, file_prefix+".jpg")
            im=Image.open(frame_path)
            width, height = im.size

            x_top_left  = bb[2]
            y_top_left  = bb[3]
            x_bottom_right = bb[4]
            y_bottom_right = bb[5]

            assert x_bottom_right > x_top_left
            assert y_bottom_right > y_top_left

            assert x_bottom_right < width
            assert y_bottom_right < height

            cursor.execute("SELECT road_user_type FROM objects where object_id == {};".format(object_id))
            road_user_type = cursor.fetchone()[0]

            cmd = "SELECT type_string FROM objects_type where road_user_type == {};".format(road_user_type)
            cursor.execute(cmd)
            type_string = cursor.fetchone()[0]

            new_bb = {"type": type_string,
                      "type_general": type_general,
                      "image_file_prefix": file_prefix,
                      "width": width,
                      "height": height,
                      "bb": [x_top_left, y_top_left, x_bottom_right, y_bottom_right]}

            annotations.setdefault(frame_number, []).append(new_bb)

    return annotations

def write_annotations(annotations_dict, save_dir):

    for frame_number, annotations in annotations_dict.iteritems():

        width = annotations[0]["width"]
        height = annotations[0]["height"]

        # write out annotation and image size
        root = ET.Element("annotation")
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(width)
        ET.SubElement(size, "height").text = str(height)
        ET.SubElement(size, "depth").text = "3"
        ET.SubElement(root, "segmentation").text = "0"

        for annotation in annotations:

            xmin = annotation["bb"][0]
            ymin = annotation["bb"][1]
            xmax = annotation["bb"][2]
            ymax = annotation["bb"][3]

            assert xmax <= width
            assert ymax <= height

            obj = ET.SubElement(root, "object")
            ET.SubElement(obj, "name").text = annotation["type"]
            ET.SubElement(obj, "name-general").text = annotation["type_general"]
            ET.SubElement(obj, "pose").text = "unspecified"
            ET.SubElement(obj, "truncated").text = "0"
            ET.SubElement(obj, "difficult").text = "0"

            bb = ET.SubElement(obj, "bndbox")
            ET.SubElement(bb, "xmin").text = str(xmin)
            ET.SubElement(bb, "xmax").text = str(xmax)
            ET.SubElement(bb, "ymin").text = str(ymin)
            ET.SubElement(bb, "ymax").text = str(ymax)

            file_prefix = annotation["image_file_prefix"]

            # Save annotation
            annot_name = os.path.join(save_dir, file_prefix+".xml")
            tree = ET.ElementTree(root)
            tree.write(annot_name, pretty_print=True)

if __name__ == "__main__":
    base = '/datasets/BigLearning/ahjiang/bb/urban-tracker/'

    s1 = os.path.join(base, 'rouen/rouen_annotations/rouen_gt_cars.sqlite')
    i1 = os.path.join(base, 'rouen/rouen_frames')
    t1  = 'car'

    s2 = os.path.join(base, 'rouen/rouen_annotations/rouen_gt_pedestrians.sqlite')
    i2 = os.path.join(base, 'rouen/rouen_frames')
    t2 = 'pedestrian'

    save_dir = os.path.join(base, 'rouen/rouen_annotations/annotations/')

    annotations = get_annotations([s1,s2], [t1,t2], [i1,i2])
    write_annotations(annotations, save_dir)

    s1 = os.path.join(base, 'stmarc/stmarc_annotations/stmarc_gt_cars.sqlite')
    i1 = os.path.join(base, 'stmarc/stmarc_frames')
    t1  = 'car'

    s2 = os.path.join(base, 'stmarc/stmarc_annotations/stmarc_gt_pedestrians.sqlite')
    i2 = os.path.join(base, 'stmarc/stmarc_frames')
    t2 = 'pedestrian'

    s3 = os.path.join(base, 'stmarc/stmarc_annotations/stmarc_gt_bike.sqlite')
    i3 = os.path.join(base, 'stmarc/stmarc_frames')
    t3 = 'bike'

    save_dir = os.path.join(base, 'stmarc/stmarc_annotations/annotations/')

    annotations = get_annotations([s1,s2,s3], [t1,t2,t3], [i1,i2,i3])
    write_annotations(annotations, save_dir)

    s2 = os.path.join(base, 'rene/rene_annotations/rene_gt.sqlite')
    i2 = os.path.join(base, 'rene/rene_frames')
    t2 = 'all'

    save_dir = os.path.join(base, 'rene/rene_annotations/annotations/')

    annotations = get_annotations([s1,s2], [t1,t2], [i1,i2])
    write_annotations(annotations, save_dir)

    s1 = os.path.join(base, 'sherbrooke/sherbrooke_annotations/sherbrooke_gt_cars.sqlite')
    i1 = os.path.join(base, 'sherbrooke/sherbrooke_frames')
    t1  = 'car'

    s2 = os.path.join(base, 'sherbrooke/sherbrooke_annotations/sherbrooke_gt_pedestrians.sqlite')
    i2 = os.path.join(base, 'sherbrooke/sherbrooke_frames')
    t2 = 'pedestrian'

    save_dir = os.path.join(base, 'sherbrooke/sherbrooke_annotations/annotations/')

    annotations = get_annotations([s1,s2], [t1,t2], [i1,i2])
    write_annotations(annotations, save_dir)

