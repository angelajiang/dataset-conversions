
import pprint as pp
import parse_tskim_labels
import random


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
    # data = {"train": [frame_id, ...], "test": []}
    # Try to give train percent_train% of _events_
    # Sample max_event_sample frames from each event at max
    # TODO: Take event length into account
    # TODO: Take class frequency into account

    data = {"train": [], "test": []}
    assert percent_train < 1

    for c, class_data in event_data.iteritems():
        event_ids = class_data.keys()
        num_train_events = int(len(event_ids) * percent_train)
        num_test_events = len(event_ids) - num_train_events

        train_events = random.sample(event_ids, num_train_events)
        test_events = list(set(event_ids) - set(train_events))

        for train_event in train_events:
            frame_ids = event_data[c][train_event]
            random.shuffle(frame_ids)
            data["train"] += frame_ids[:max_event_sample]
            event_fraction = min(1, max_event_sample / float(len(frame_ids)))
            print "Adding {}% of event {}".format(round(event_fraction, 2) * 100,
                                                  train_event)

        for test_event in test_events:
            frame_ids = event_data[c][test_event]
            random.shuffle(frame_ids)
            data["test"] += frame_ids[:max_event_sample]
            event_fraction = min(1, max_event_sample / float(len(frame_ids)))
            print "Adding {}% of event {}".format(round(event_fraction, 2) * 100,
                                                  test_event)

        print "Class: {}, # train events:{}, # test events: {}".format(c,
                                                                       num_train_events,
                                                                       num_test_events)

    print "# train frames: {}, # test frames: {}".format(len(data["train"]),
                                                         len(data["test"]))

    return data


def make_dataset(labels_file, class_mapping, mp4_path, images_out_dir):
    # Get event-based information from labels_file and class_mapping
    event_data = _get_event_data(labels_file, class_mapping)

    # Sort events into train and test
    sorted_events = _sort_frames(event_data, 0.8)

    # Explode mp4 into frames into tmp dir

    # Copy subset of frames from events into train and test dir


def parse_labeler_output(labels_dir, labels_out):
    data_points, full_labels = parse_tskim_labels.main(labels_dir)
    parse_tskim_labels.write_file(labels_out, full_labels)

def main():

    # III Bus presence dataset

    labels_dir = "./labels/iii_01_buses"
    labels_out = "./labels/iii_01_buses.out"
    parse_labeler_output(labels_dir, labels_out)

    class_mapping = {"No Event": "no-bus", "Event": "bus"}
    mp4_path = "~/src/data/videos/iii/iii-01/vimba_iii_1_2018-3-21_7.mp4"
    images_out_dir = "~/src/data/image-data/iii-buses"
    make_dataset(labels_out, class_mapping, mp4_path, images_out_dir)


if __name__ == "__main__":
    main()
