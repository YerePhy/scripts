import monai
import yaml
import nibabel as nib
from typing import List, Dict
from pathlib import Path
from pyprojroot import here


def read_subjects(
    dataset_path: Path,
    ref_filename: str,
    mod_filename: str
) -> List[Dict[str, Path]]:
    """
    Read files from a subject-like
    directory:

    .. code-block::

    dataset_path
    ├── subject_0
    │   ├── <ref_filename>
    │   └── <mod_filename>
    ├── subject_1
    │   ├── <ref_filename>
    │   └── <mod_filename>
    .
    .
    .
    └── subject_N
       ├── <ref_filename>
       └── <mod_filename>

    Args:
        dataset_path: path to the dataset.
        ref_filename: name (with extension) of the reference filename.
        mod_filename: name (with extension) of the file to be modified.

    Returns:
        A ``list`` of ``dict``s where each
        ``dict`` has two keys ``"REF"`` and
        ``"MOD"``. The former for the activity
        map and the latter for the FastSurfer
        segmentation.
    """
    subjects = []

    for subjdir in Path(dataset_path).iterdir():
        subj = {}
        ref_file = subjdir.joinpath(ref_filename)
        mod_file = subjdir.joinpath(mod_filename)

        if ref_file.is_file():
            subj["REF"] = ref_file

        if mod_file.is_file():
            subj["MOD"] = mod_file

        subjects.append(subj)

    return subjects


cfg_file = here().joinpath("configs/resample_monai.yaml")

with open(cfg_file.resolve(), 'r') as file:
    cfg = yaml.safe_load(file)

data_root_dir = Path(cfg["data_root_dir"])
apply_to_subject = bool(cfg["apply_to_subject"])
output_postfix_mod = str(cfg["output_postfix_mod"])
ref_image = str(cfg["ref_image"])
mod_image = str(cfg["mod_image"])

if apply_to_subject:
    if cfg["subject_id"] is not None:
        subject_id = str(cfg["subject_id"])
        data_root_dir_id = data_root_dir.joinpath(cfg["subject_id"])
        ref_image = data_root_dir_id.joinpath(ref_image)
        mod_image = data_root_dir_id.joinpath(mod_image)
        subjects = [{
            "REF": ref_image,
            "MOD": mod_image
        }]
    else:
        raise ValueError(
            f"apply_to_subject is {apply_to_subject} and found subject_id: {subject_id}.")
else:
    subjects = read_subjects(data_root_dir, ref_image, mod_image)

for subj in subjects:
    target_shape = nib.load(subj["REF"]).get_fdata().shape

    pipe = monai.transforms.Compose([
        monai.transforms.LoadImaged(keys=["REF", "MOD"]),
        monai.transforms.EnsureChannelFirstd(
            keys=["REF", "MOD"], channel_dim="no_channel"),
        monai.transforms.ResampleToMatchd(keys=["MOD"], key_dst="REF"),
        monai.transforms.CenterSpatialCropd(
            keys=["MOD"], roi_size=target_shape),
        monai.transforms.SaveImaged(
            keys=["MOD"], separate_folder=False,
            output_postfix=output_postfix_mod, data_root_dir=data_root_dir,
            output_dir=data_root_dir, output_ext=".nii")
    ])

    pipe(subj)
