from glob import glob
from pathlib import Path
import argparse
import shutil

from cad2cosypose import read_config_file

# Import env variables
cfg = read_config_file()

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str,
                    default=cfg["dataset_name"],
                    help="Name of the dataset")
parser.add_argument('--rendered-batch-path', dest='rendered_batch_path', type=str,
                    default=cfg["output_dir"],
                    help="Path to where the batch of images was generated by BlenderProc")
args = parser.parse_args()

rendered_batch_path = Path(args.rendered_batch_path)

paths = rendered_batch_path / "**" / args.dataset / "train_pbr" / "**"

print("paths")
print(paths)

all_generated_dirs = glob(paths.as_posix())
all_generated_dirs.sort()

print("all_generated_dirs")
print(all_generated_dirs)
batch_dirs = glob((rendered_batch_path / "**").as_posix())


def format_dir_name(dir, new_idx):
    frags = [f for f in dir.split("/") if "batch" not in f]
    frags[-1] = f"{new_idx:06d}"
    dest = "/".join(frags)
    return dest


# Move all the dirs into a single one for the dataset
for idx, dir in enumerate(all_generated_dirs):
    if idx == 0:
        dir = "/".join(dir.split("/")[:-2])
        frags = [f for f in dir.split("/") if "batch" not in f]
        dest = "/".join(frags)
        print(dir, frags, dest)
    else:
        dest = format_dir_name(dir, idx)
        print(dest)

    if idx == 0 or "batch0" not in dir:
        shutil.move(dir, dest)

# Remove previous dirs
for dir in batch_dirs:
    shutil.rmtree(dir)

# Move dataset/dataset to dataset
subdir = rendered_batch_path / args.dataset
for dir in glob((subdir / "**").as_posix()):
    frags = dir.split("/")
    dest = "/".join(frags[:-2] + [frags[-1]])
    shutil.move(dir, dest)
shutil.rmtree(subdir)

print(f"Finished gathering all the data in {args.rendered_batch_path}")