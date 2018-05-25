
import argparse
import random
import numpy as np
import util

random.seed(1337)

def get_args(simulator=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-ld", "--labels_dir", required=True)
    parser.add_argument("-lo", "--labels_out", required=True)
    parser.add_argument("-ne", "--no_event_label", required=True)
    parser.add_argument("-e", "--event_label", required=True)
    return parser.parse_args()


def main():

    args = get_args()

    util.parse_labeler_output(args.labels_dir, args.labels_out)

    class_mapping = {}
    class_mapping["No Event"] = args.no_event_label
    class_mapping["Event"] = args.event_label

    event_lengths = util.get_event_lengths(args.labels_out,
                                           class_mapping,
                                           "Event")

    frequency = util.get_event_frequency(args.labels_out,
                                         class_mapping)

    s = "Avg event length: {} frames\n" + \
        "Min event frequency: {}\n" + \
        "Event frequency: {}\n"
    print s.format(int(np.average(event_lengths)),
                   min(event_lengths),
                   frequency)


if __name__ == "__main__":
    main()
