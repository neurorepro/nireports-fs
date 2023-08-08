from pathlib import Path
from bids import BIDSLayout
from nibabel.freesurfer.mghformat import load
from nireports.assembler.report import Report
import numpy as np
import nibabel as nib
from nilearn import plotting
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from freesurfer_report import generate_report_with_plots

# def gen_subj_fs_report(fs_dir, subj, outdir):
#     subj_fs_dir = Path(fs_dir) / subj
#     hemis = ["lh", "rh"]
#     stypes = ["inflated", "pial", "white", "midthickness"]
#     surfs = {f"{hemi}_{stype}": subj_fs_dir / "surf" / f"{hemi}.{stype}" for hemi in hemis for stype in stypes}
#     print(surfs)



layout = BIDSLayout("bids_testset")
subjects = layout.get(return_type='filename', target='subject', suffix='T1w', extension='nii.gz')

if subjects:
    in_file = layout.get_file(subjects[0])
    
    entities = in_file.get_entities()
    entities.pop("extension", None)


def generate_paths(folder_path):
    """Generate a list of file paths for files named "aseg.stats" within a given folder.

        Parameters
        ----------
        folder_path : str
            The path to the folder to search for files.

        Returns
        -------
        list
            A list of file paths for files named "aseg.stats" within the specified folder.
        """

    file_paths = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file_name in filenames:
            if file_name == "aseg.stats":
                file_path = os.path.join(dirpath, file_name)
                file_paths.append(file_path)

    return file_paths

report_type = entities.pop("datatype", None)
report_type = "fs"
bootstrap_file=f"bootstrap_data/bootstrap-{report_type}.yml"

# fs_dir = "/mnt/projects/nireports/nireports_freesurfer/bids_testset/derivatives/freesurfer"
# subj = "sub-pp001"
# outdir = "/mnt/projects/nireports/nireports_freesurfer/reportlets"
# gen_subj_fs_report(fs_dir, subj, outdir)

generate_paths("bids_testset")


bootstrap_file="bootstrap_data/bootstrap-fs.yml"
prov = {}

prov["Freesurfer build stamp"] = f"freesurfer-linux-ubuntu22_x86_64-7.3.2-20220804-6354275"
prov["Execution environment"] = f"Linux d4ef45c6cca2 5.14.0-1057-oem #64-Ubuntu"

fs_metrics = {'vol_mm3_region3rd-Ventricle': '805.0', 'vol_mm3_region4th-Ventricle': '1439.9', 'vol_mm3_region5th-Ventricle': '0.0', 'vol_mm3_regionBrain-Stem': '19420.3', 'vol_mm3_regionCC_Anterior': '985.3', 'vol_mm3_regionCC_Central': '712.0', 'vol_mm3_regionCC_Mid_Anterior': '880.1', 'vol_mm3_regionCC_Mid_Posterior': '639.3', 'vol_mm3_regionCC_Posterior': '1024.8', 'vol_mm3_regionCSF': '1036.4', 'vol_mm3_regionLeft-Accumbens-area': '448.2', 'vol_mm3_regionLeft-Amygdala': '1590.8', 'vol_mm3_regionLeft-Caudate': '3564.4', 'vol_mm3_regionLeft-Cerebellum-Cortex': '56219.8', 'vol_mm3_regionLeft-Cerebellum-White-Matter': '12602.0', 'vol_mm3_regionLeft-Hippocampus': '3536.5', 'vol_mm3_regionLeft-Inf-Lat-Vent': '485.5', 'vol_mm3_regionLeft-Lateral-Ventricle': '7887.5', 'vol_mm3_regionLeft-Pallidum': '1827.0', 'vol_mm3_regionLeft-Putamen': '4689.9', 'vol_mm3_regionLeft-Thalamus': '7665.0', 'vol_mm3_regionLeft-VentralDC': '3840.2', 'vol_mm3_regionLeft-WM-hypointensities': '0.0', 'vol_mm3_regionLeft-choroid-plexus': '512.2', 'vol_mm3_regionLeft-non-WM-hypointensities': '0.0', 'vol_mm3_regionLeft-vessel': '29.0', 'vol_mm3_regionOptic-Chiasm': '105.7', 'vol_mm3_regionRight-Accumbens-area': '463.9', 'vol_mm3_regionRight-Amygdala': '1612.5', 'vol_mm3_regionRight-Caudate': '3432.6', 'vol_mm3_regionRight-Cerebellum-Cortex': '57641.0', 'vol_mm3_regionRight-Cerebellum-White-Matter': '11853.5', 'vol_mm3_regionRight-Hippocampus': '3959.4', 'vol_mm3_regionRight-Inf-Lat-Vent': '160.2', 'vol_mm3_regionRight-Lateral-Ventricle': '5654.4', 'vol_mm3_regionRight-Pallidum': '1825.9', 'vol_mm3_regionRight-Putamen': '4690.0', 'vol_mm3_regionRight-Thalamus': '7954.8', 'vol_mm3_regionRight-VentralDC': '3562.0', 'vol_mm3_regionRight-WM-hypointensities': '0.0', 'vol_mm3_regionRight-choroid-plexus': '400.7', 'vol_mm3_regionRight-non-WM-hypointensities': '0.0', 'vol_mm3_regionRight-vessel': '16.0', 'vol_mm3_regionWM-hypointensities': '343.6', 'vol_mm3_regionnon-WM-hypointensities': '0.0'}

metadata={
    "dataset": "Test dataset Freesurfer report",
    "fs-metadata": {
        "Provenance Information": prov,
        "Metrics": fs_metrics,
    }
}

output_dir = "fs_report"
uuid = "random_uuid"
reportlets_dir = "reportlets/sub-s05/ses-01/figures"

# robj = Report(output_dir, uuid, reportlets_dir=reportlets_dir,
#               bootstrap_file=bootstrap_file, metadata=metadata,
#               plugin_meta={}, **entities)

# robj.generate_report()



test_meta = {}

metadata={
    "dataset": "test name",
    "about-metadata": {
        "Provenance Information": prov,
        "Dataset Information": test_meta,
    }
}
output_dir = "bids_testset/derivatives/testreport"
reportlets_dir = "bids_testset/derivatives/fmriprep/sub-s05/figures/"

report_filename = generate_report_with_plots(
    output_dir=output_dir, 
    run_uuid=uuid.uuid4(), 
    reportlets_dir=reportlets_dir,
    bootstrap_file=bootstrap_file,
    metadata=metadata,
    plugin_meta={}
)

dir_FS ="bids_testset/derivatives/fmriprep/sourcedata/freesurfer/sub-s05"