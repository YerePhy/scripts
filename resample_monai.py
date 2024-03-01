import monai
import yaml
import nibabel as nib
from pathlib import Path
from pyprojroot import here


cfg_file = here().joinpath("configs/resample_monai.yaml")

with open(cfg_file.resolve(), 'r') as file:
    cfg = yaml.safe_load(file)

data_root_dir = Path(cfg["data_root_dir"])
ref_image = data_root_dir.joinpath(cfg["ref_image"])
mod_image = data_root_dir.joinpath(cfg["mod_image"])
output_postfix_mod = str(cfg["output_postfix_mod"])

subject = {
    "REF": ref_image,
    "MOD": mod_image
}
target_shape = nib.load(subject["REF"]).get_fdata().shape

pipe = monai.transforms.Compose([
    monai.transforms.LoadImaged(keys=["REF", "MOD"]),
    monai.transforms.EnsureChannelFirstd(
        keys=["REF", "MOD"], channel_dim="no_channel"),
    monai.transforms.CenterSpatialCropd(keys=["MOD"], roi_size=target_shape),
    monai.transforms.ResampleToMatchd(keys=["MOD"], key_dst="REF"),
    monai.transforms.SaveImaged(
        keys=["MOD"], separate_folder=False,
        output_postfix=output_postfix_mod, data_root_dir=data_root_dir,
        output_dir=data_root_dir, output_ext=".nii")
])

pipe(subject)
