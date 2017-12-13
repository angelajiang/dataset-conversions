import cv2 
import os
import sys

def convert(src_dir, dest_dir, mask_file):
    for f in os.listdir(src_dir):
        if f.endswith(".jpg"):
            filename = os.path.join(src_dir, f)
            img = cv2.imread(filename)
            mask = cv2.imread(mask_file)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            res = cv2.bitwise_and(img, img, mask = mask)
            out_filename = os.path.join(dest_dir, f)
            cv2.imwrite(out_filename, res)

if __name__ == "__main__":
    base = "/datasets/BigLearning/ahjiang/bb/urban-tracker/"

    for ds in ["rene", "sherbrooke"]:
        src = os.path.join(base, ds+"/"+ds+"_frames")
        dest = os.path.join(base, ds+"/"+ds+"_masked_frames")
        mask_file = os.path.join(base, ds+"/"+ds+"_mask.png")
        print src, dest, mask_file
        convert(src, dest, mask_file)
