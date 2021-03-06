
import argparse
import random
import util

random.seed(1337)

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


def main():

    args = get_args()

    util.parse_labeler_output(args.labels_dir, args.labels_out)

    class_mapping = {}
    class_mapping["No Event"] = args.no_event_label
    class_mapping["Event"] = args.event_label

    util.make_dataset(args.labels_out,
                      class_mapping,
                      args.video_path,
                      args.dataset_dir,
                      args.frame_dir,
                      args.frame_prefix,
                      args.frame_name_size)


if __name__ == "__main__":
    main()
