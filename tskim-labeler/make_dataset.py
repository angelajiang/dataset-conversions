
import argparse
import pprint as pp
import parse_tskim_labels
import random
import shutil
import os

def get_args(simulator=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-ld", "--labels_dir", required=True)
    parser.add_argument("-lo", "--labels_out", required=True)
    parser.add_argument("-ne", "--no_event_label", required=True)
    parser.add_argument("-e", "--event_label", required=True)
    parser.add_argument("-v", "--video_path", required=True)
    parser.add_argument("-o", "--dataset_dir", required=True)
    parser.add_argument("-fd", "--frame_dir", required=True)
    parser.add_argument("-fp", "--frame_prefix", required=True)
    parser.add_argument("-fs", "--frame_name_size", required=True, type=int)
    return parser.parse_args()

def get_event_length():
    pass

def get_event_frequency():
    pass

def _get_event_data(labels_file, class_mapping):
    # data = {class_name: {event_id: [frame_ids...]}}
    data = {}
    for c in class_mapping.values():
        data[c] = {}

    cur_event_label  = ""
    cur_event_id = -1
    with open(labels_file, "r") as f:
        for line in f:
            vals = line.split(",")
            frame_id = int(vals[0])
            generic_label = vals[1].rstrip()
            if generic_label == "Unknown":
                continue

            label = class_mapping[generic_label]
            if label != cur_event_label:
                # New event
                cur_event_label = label
                cur_event_id += 1
                data[label][cur_event_id] = []
            data[label][cur_event_id].append(frame_id)

    return data

def _sort_frames(event_data, percent_train, max_event_sample=50):
    # data = {"train": {"class_name": [frame_id, ...]}, "test": {}}
    # Try to give train percent_train% of _events_
    # Sample max_event_sample frames from each event at max
    # TODO: Take event length into account
    # TODO: Take class frequency into account

    data = {"train": {}, "test": {}}
    assert percent_train < 1

    for c, class_data in event_data.iteritems():
        data["train"][c] = []
        data["test"][c] = []
        event_ids = class_data.keys()
        num_train_events = int(len(event_ids) * percent_train)
        num_test_events = len(event_ids) - num_train_events

        train_events = random.sample(event_ids, num_train_events)
        test_events = list(set(event_ids) - set(train_events))

        for train_event in train_events:
            frame_ids = event_data[c][train_event]
            random.shuffle(frame_ids)
            data["train"][c] += frame_ids[:max_event_sample]
            event_fraction = min(1, max_event_sample / float(len(frame_ids)))
            print "Adding {}% of event {}".format(round(event_fraction, 2) * 100,
                                                  train_event)

        for test_event in test_events:
            frame_ids = event_data[c][test_event]
            random.shuffle(frame_ids)
            data["test"][c] += frame_ids[:max_event_sample]
            event_fraction = min(1, max_event_sample / float(len(frame_ids)))
            print "Adding {}% of event {}".format(round(event_fraction, 2) * 100,
                                                  test_event)

        print "Class: {}, # train events:{}, # test events: {}".format(c,
                                                                       num_train_events,
                                                                       num_test_events)

    return data


def make_dataset(labels_file,
                 class_mapping,
                 video_path,
                 dataset_dir,
                 frame_dir,
                 frame_prefix,
                 frame_name_size):

    # Get event-based information from labels_file and class_mapping
    event_data = _get_event_data(labels_file, class_mapping)

    # Sort events into train and test
    sorted_events = _sort_frames(event_data, 0.8)

    # Copy subset of frames from events into train and test dir
    written_images = 0
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    for split, frame_ids_by_class in sorted_events.iteritems():
        split_dir = os.path.join(dataset_dir, split)
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)
        for class_name, frame_ids in frame_ids_by_class.iteritems():
            class_dir = os.path.join(split_dir, class_name)
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
            for frame_id in frame_ids:
                frame_id_str = str(frame_id)
                buffer_size = frame_name_size - len(frame_id_str)
                zeros = '0' * buffer_size
                frame_name = frame_prefix + zeros + frame_id_str + ".jpg"
                frame_path = os.path.join(frame_dir,
                                          frame_name)
                if os.path.isfile(frame_path):
                    written_images += 1
                    shutil.copyfile(frame_path, os.path.join(class_dir, frame_name))
                else:
                    print "Warning: Could not find file {}".format(frame_path)
    print "{} images written to {}".format(written_images, dataset_dir)

def parse_labeler_output(labels_dir, labels_out):
    data_points, full_labels = parse_tskim_labels.main(labels_dir)
    parse_tskim_labels.write_file(labels_out, full_labels)

def main():

    args = get_args()

    parse_labeler_output(args.labels_dir, args.labels_out)

    class_mapping = {}
    class_mapping["No Event"] = args.no_event_label
    class_mapping["Event"] = args.event_label

    make_dataset(args.labels_out,
                 class_mapping,
                 args.video_path,
                 args.dataset_dir,
                 args.frame_dir,
                 args.frame_prefix,
                 args.frame_name_size)


if __name__ == "__main__":
    main()
