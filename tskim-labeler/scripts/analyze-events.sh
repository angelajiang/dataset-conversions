# Don't use relative paths!
-X

HOME_DIR="/users/ahjiang/"


EVENT_LABEL="schoolbus"
NO_EVENT_LABEL="no-schoolbus"
LABELS_DIR=$HOME_DIR"src/labeler/iii_01_schoolbus/iii_01_7"
LABELS_OUT=$HOME_DIR"src/dataset-conversions/tskim-labeler/labels/iii_01_7.out"

echo $EVENT_LABEL
python analyze_dataset.py -ld $LABELS_DIR \
                          -lo $LABELS_OUT \
                          -ne $NO_EVENT_LABEL \
                          -e  $EVENT_LABEL

EVENT_LABEL="redcar"
NO_EVENT_LABEL="no-redcar"
LABELS_DIR=$HOME_DIR"src/labeler/iii_01_redcar/iii_01_7"
LABELS_OUT=$HOME_DIR"src/dataset-conversions/tskim-labeler/labels/iii_01_7.out"

echo $EVENT_LABEL
python analyze_dataset.py -ld $LABELS_DIR \
                          -lo $LABELS_OUT \
                          -ne $NO_EVENT_LABEL \
                          -e  $EVENT_LABEL

EVENT_LABEL="scramble"
NO_EVENT_LABEL="no-scramble"
LABELS_DIR=$HOME_DIR"src/labeler/iii_01_scramble/iii_01_7"
LABELS_OUT=$HOME_DIR"src/dataset-conversions/tskim-labeler/labels/iii_01_7.out"

echo $EVENT_LABEL
python analyze_dataset.py -ld $LABELS_DIR \
                          -lo $LABELS_OUT \
                          -ne $NO_EVENT_LABEL \
                          -e  $EVENT_LABEL

EVENT_LABEL="bus"
NO_EVENT_LABEL="no-bus"
LABELS_DIR=$HOME_DIR"src/labeler/iii_01_buses/iii_01_7"
LABELS_OUT=$HOME_DIR"src/dataset-conversions/tskim-labeler/labels/iii_01_7.out"

echo $EVENT_LABEL
python analyze_dataset.py -ld $LABELS_DIR \
                          -lo $LABELS_OUT \
                          -ne $NO_EVENT_LABEL \
                          -e  $EVENT_LABEL

