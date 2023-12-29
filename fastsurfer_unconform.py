import os
import yaml
import logging
import torchio as tio
from typing import Mapping, Union, Set, List
from enum import Enum
from pathlib import Path
from pyprojroot import here


class TorchIOImageTypes(Enum):
    SCALAR = tio.ScalarImage
    LABEL = tio.LabelMap


def remove_suffixes(filename: Union[str, Path]) -> str:
    """
    Remove sufixes from filename.

    Args:
        filename: a filename.

    Returns:
        Filename witout suffixes.
    """
    filename_ = Path(filename)
    return str(filename_).rstrip(''.join(filename_.suffixes))


def get_subject_files_by_name(
    dirpath: Union[Path, str],
    filenames: Set[str],
    filenames_type: Mapping[str, str]
) -> List[Mapping[str, Path]]:
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
                    file_type = filenames_type[name]
                    tio_image_type = TorchIOImageTypes[file_type].value

                    filepath = Path(root).joinpath(name)
                    file_key = remove_suffixes(filepath.name)
                    subj[file_key] = tio_image_type(filepath)

            if subj:
                subjects.append(tio.Subject(subj))

    return subjects


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            here().joinpath("logs/fastsurfer_unconform.log"), mode='w')
    ]
)

cfg_file = here().joinpath("configs/fastsurfer_unconform.yaml")

with open(cfg_file.resolve(), 'r') as file:
    cfg = yaml.safe_load(file)

data = cfg["data"]
ref_image_name = cfg["ref_image_name"]
tf_image_name = cfg["tf_image_name"]
ref_image_type = cfg["ref_image_type"]
tf_image_type = cfg["tf_image_type"]
new_tf_image_prefix = cfg["new_tf_image_prefix"]

filenames = {ref_image_name, tf_image_name}
filetypes = {
    ref_image_name: ref_image_type,
    tf_image_name: tf_image_type
}
ref_image_key = remove_suffixes(ref_image_name)
tf_image_key = remove_suffixes(tf_image_name)

pipeline = tio.transforms.Compose([
    tio.transforms.Resample(
        target=ref_image_key,
        include=[tf_image_key],
        label_interpolation="label_gaussian"
    )
])

subjects = get_subject_files_by_name(data, filenames, filetypes)
subjects = [pipeline(subj) for subj in subjects]

for subj in subjects:
    tf_image = subj[tf_image_key]
    tf_image_path = tf_image.path
    tf_image_new_path = tf_image_path.with_name(
        f"{new_tf_image_prefix}_{tf_image_path.name}")
    tf_image.save(tf_image_new_path)

logging.info("FastSurfet uncorforming completed.")
