import os
import logging
import yaml
import torchio as tio
from typing import Union, Set, List, Mapping
from pathlib import Path
from pyprojroot import here


cfg_file = here().joinpath("configs/resample_maps.yaml")

with open(cfg_file.resolve(), 'r') as file:
    cfg = yaml.safe_load(file)

DATA = cfg["data"]
ACT_NAME = cfg["act_name"]
ATT_NAME = cfg["att_name"]
TARGET_VOXEL_SIZE = cfg["target_voxel_size"]

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(here().joinpath("logs/resample_maps.log"), mode='w')
    ]
)

def get_subject_files_by_name(dirpath: Union[Path, str], filenames: Set[str]) -> List[Mapping[str, Path]]:
    """
    Finds all files matching several names recursively.

    Args:
        dirpath: root dir.
        filenames: filenames to find.

    Returns:
        List of ``Dict`` having as keys the filenames without extension
        and having as value the full path of the found files.
    """
    dirpath = Path(dirpath)

    assert dirpath.is_dir()

    subjects = []

    for root, dirs, files in os.walk(dirpath):
        if bool(files):
            subj = {}
            for name in files:
                if name in filenames:
                    filepath = Path(root).joinpath(name)
                    subj[filepath.stem] = filepath
            subjects.append(subj)

    return subjects


def apply_pipeline(subject: tio.Subject, act_map_key: str, att_map_key: str) -> tio.Compose:
    """
    Build a torchIO pipeline to resample images
    in order be square-like in X, Y dims. The image
    may be padded or cropped in Y to match X shape. Thus,
    it is recommended for Y dim to be close to X dim in order
    to avoid excesive crops or pads.

    Args:
        subject: a ``torchio.Subject``.
        act_map_key: key pointing to activity map in ``subject``.
        att_map_key: key pointing to attenuation map in ``subject``.

    Returns:
        Subject having the resampled images.
    """
    z_shape = subject[act_map_key].shape[-1]
    x_shape = subject[act_map_key].shape[-3]
    target_shape = [x_shape, x_shape, z_shape]
    keys = [act_map_key, att_map_key]
    pipeline = tio.Compose([
        tio.Resample(target=act_map_key, include=[att_map_key]),
        tio.Resample(include=keys, target=TARGET_VOXEL_SIZE, label_interpolation="label_gaussian"),
        tio.CropOrPad(include=keys, target_shape=target_shape, padding_mode='constant')
    ])
    return pipeline(subject)


def save_images(subject: tio.Subject, prefix: str) -> None:
    """
    Save images following torchIO interface.

    Args:
        subject: a ``torchio.Subject``.
        prefix: prefix to insert to the new filename.

    """
    for img in subject.values():
        shape = img.shape
        assert img.shape[1] == img.shape[2], f"Image X, Y dims must be equal, found shape {shape}"
        new_filepath = img.path.with_name(f"{prefix}_{img.path.name}")
        img.save(new_filepath)
        logging.info(f"{str(img.path)} {str(new_filepath)} {shape} {img.spacing}")


subjects = get_subject_files_by_name(DATA, {ACT_NAME, ATT_NAME})
subjects = [tio.Subject({k: tio.LabelMap(img) for k, img in subj.items()}) for subj in subjects]

act_map_key = Path(ACT_NAME).stem
att_map_key = Path(ATT_NAME).stem

for subj in subjects:
    transformed_subj = apply_pipeline(subj, act_map_key, att_map_key)
    save_images(transformed_subj, "resampled")
