import pprint as pp
import scipy.io as sio
import shutil
import sys
import os

def read_annotations(mat_file):
    # Returns: {class_index: {
    #               "images": [file_prefix1, ...]
    #               }
    #           }
    # annotation[0] is file_name
    # annotation[5] is class_index

    data = {}

    contents = sio.loadmat(mat_file)
    annotations = contents["annotations"]
    for annotation in annotations[0]:
        image_file = str(annotation[0][0])
        class_index = int(annotation[5][0][0])
        if class_index not in data.keys():
            data[class_index] = {"images": []}
        data[class_index]["images"].append(image_file)

    return data

def sort_files(mat_file, src_dir, dest_dir):
    '''
    Creates cars classification datasets
    
    dest_dir /
        0/
            car-image-of-class-0.jpg
        1/
            car-image-of-class-0.jpg
    
    *Will overwrite dest_dir*
    '''

    # Create directory hierarchy
    #if os.path.exists(dest_dir):
    #    shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    data = read_annotations(mat_file)
    for class_index, class_data in data.iteritems():
        class_dir = os.path.join(dest_dir, str(class_index))
        os.mkdir(class_dir)

        for image_file in class_data["images"]:
            image_path = os.path.join(src_dir, image_file)
            shutil.copy(image_path, class_dir)

        
if __name__ == "__main__":
    mat_file = "/datasets/BigLearning/ahjiang/image-data/stanford-car-dataset/cars_annos.mat"
    src_dir = "/datasets/BigLearning/ahjiang/image-data/stanford-car-dataset/"
    dest_dir = "/datasets/BigLearning/ahjiang/image-data/training/cars-stanford"
    sort_files(mat_file, src_dir, dest_dir)

