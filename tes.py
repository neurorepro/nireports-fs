from bids.layout import BIDSLayout
from freesurfer_report import generate_report_with_plots
import uuid


layout = BIDSLayout("bids_testset")
in_file = layout.get_file("sub-s05/ses-01/anat/sub-s05_ses-01_T1w.nii.gz")
entities = in_file.get_entities()
entities.pop("extension", None)
report_type = entities.pop("datatype", None)
report_type = "fs"
bootstrap_file=f"bootstrap_data/bootstrap-{report_type}.yml"
print(entities)

prov = {}
prov["Input filename"] = f"Test filename"
prov["Version Freesurfer"] = f"Version X.Y"
prov["Execution environment"] = f"Test environment"
bids_meta = layout.get_file(in_file).get_metadata()

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
