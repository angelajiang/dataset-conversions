
import sqlite3
import pprint as pp
import os

from PIL import Image
from lxml import etree as ET

'''
Converts Urban Tracker annotations to per-frame classification data
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
    #                 object_id, 
    #                 width, 
    #                 height, 
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
                      "object_id": object_id,
                      "width": width,
                      "height": height,
                      "bb": [x_top_left, y_top_left, x_bottom_right, y_bottom_right]}

            annotations.setdefault(frame_number, []).append(new_bb)

    return annotations

def write_classification_metadata(sqlite_files, general_types, image_dirs, save_file):

    # Write to file: 
    # frame_number, frame_path, type_general, num_objects, object_id1, object_id2, ... 

    annotations_dict = get_annotations(sqlite_files, general_types, image_dirs)

    events_dict =  {}
    # frame_number: 
    #   type_general: {image_file_prefix, 
    #                  num_objects,
    #                  [object_ids...]}

    for frame_number, annotations_arr in annotations_dict.iteritems():
        for annotations in annotations_arr:

            file_prefix = annotations["image_file_prefix"]
            type_general = annotations["type_general"]
            object_id = annotations["object_id"]

            if frame_number not in events_dict.keys():
                events_dict[frame_number] = {}
            if type_general not in events_dict[frame_number].keys():
                events_dict[frame_number][type_general] = {"num_objects": 0,
                                                           "object_ids": [],
                                                           "image_file_prefix": file_prefix}

            events_dict[frame_number][type_general]["num_objects"] += 1
            events_dict[frame_number][type_general]["object_ids"].append(object_id)

        with open(save_file, "w+") as f:
            for frame_number, type_generals in events_dict.iteritems():
                for type_general, objects in type_generals.iteritems():
                    object_id_strs = [str(o) for o in objects["object_ids"]]
                    object_id_list = ",".join(object_id_strs)
                    line = "%d,%s,%s,%d,%s\n" % (frame_number,
                                                 objects["image_file_prefix"],
                                                 type_general,
                                                 objects["num_objects"],
                                                 object_id_list)
                    f.write(line)
    print "Data written to %s" % (save_file)



if __name__ == "__main__":
    base = '/datasets/BigLearning/ahjiang/bb/urban-tracker/'

    s1 = os.path.join(base, 'rouen/rouen_annotations/rouen_gt_cars.sqlite')
    i1 = os.path.join(base, 'rouen/rouen_frames')
    t1  = 'car'

    s2 = os.path.join(base, 'rouen/rouen_annotations/rouen_gt_pedestrians.sqlite')
    i2 = os.path.join(base, 'rouen/rouen_frames')
    t2 = 'pedestrian'

    save_file = os.path.join(base, 'rouen/rouen_annotations/presence_metadata.csv')

    write_classification_metadata([s1,s2], [t1,t2], [i1,i2], save_file)

    s1 = os.path.join(base, 'stmarc/stmarc_annotations/stmarc_gt_cars.sqlite')
    i1 = os.path.join(base, 'stmarc/stmarc_frames')
    t1  = 'car'

    s2 = os.path.join(base, 'stmarc/stmarc_annotations/stmarc_gt_pedestrians.sqlite')
    i2 = os.path.join(base, 'stmarc/stmarc_frames')
    t2 = 'pedestrian'

    s3 = os.path.join(base, 'stmarc/stmarc_annotations/stmarc_gt_bike.sqlite')
    i3 = os.path.join(base, 'stmarc/stmarc_frames')
    t3 = 'bike'

    save_file = os.path.join(base, 'stmarc/stmarc_annotations/presence_metadata.csv')

    write_classification_metadata([s1,s2,s3], [t1,t2,t3], [i1,i2,i3], save_file)

    s1 = os.path.join(base, 'sherbrooke/sherbrooke_annotations/sherbrooke_gt_cars.sqlite')
    i1 = os.path.join(base, 'sherbrooke/sherbrooke_frames')
    t1  = 'car'

    s2 = os.path.join(base, 'sherbrooke/sherbrooke_annotations/sherbrooke_gt_pedestrians.sqlite')
    i2 = os.path.join(base, 'sherbrooke/sherbrooke_frames')
    t2 = 'pedestrian'

    save_file = os.path.join(base, 'sherbrooke/sherbrooke_annotations/presence_metadata.csv')

    write_classification_metadata([s1,s2], [t1,t2], [i1,i2], save_file)

    s1 = os.path.join(base, 'atrium/atrium_annotations/atrium_gt.sqlite')
    i1 = os.path.join(base, 'atrium/atrium_frames')
    t1 = 'pedestrian'

    save_file = os.path.join(base, 'atrium/atrium_annotations/presence_metadata.csv')

    write_classification_metadata([s1], [t1], [i1], save_file)
