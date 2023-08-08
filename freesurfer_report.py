from pathlib import Path
from bids import BIDSLayout
from nibabel.freesurfer.mghformat import load
from brainspace.plotting import plot_hemispheres
from brainspace.mesh.mesh_io import read_surface
from nireports.assembler.report import Report
import numpy as np
import nibabel as nib
from nilearn import plotting
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

report_type = entities.pop("datatype", None)
report_type = "fs"
bootstrap_file=f"bootstrap_data/bootstrap-{report_type}.yml"
print(entities)

def generate_report_with_plots(
    output_dir,
    run_uuid,
    reportlets_dir,
    bootstrap_file,
    metadata,
    plugin_meta,
    **entities
):
    robj = Report(
        output_dir,
        run_uuid,
        reportlets_dir=reportlets_dir,
        bootstrap_file=bootstrap_file,
        metadata=metadata,
        plugin_meta=plugin_meta,
        **entities,
    )
    robj.generate_report()
    return robj.out_filename.absolute()



dir_FS ="bids_testset/derivatives/fmriprep/sourcedata/freesurfer/sub-s05"

# Load native pial surface
pial_lh = read_surface(dir_FS+'/surf/lh.pial', itype='fs')
pial_rh = read_surface(dir_FS+'/surf/rh.pial', itype='fs')

# Load native mid surface
mid_lh = read_surface(dir_FS+'/surf/lh.midthickness', itype='fs')
mid_rh = read_surface(dir_FS+'/surf/rh.midthickness', itype='fs')

# Load native white matter surface
wm_lh = read_surface(dir_FS+'/surf/lh.white', itype='fs')
wm_rh = read_surface(dir_FS+'/surf/rh.white', itype='fs')

# Load native inflated surface
inf_lh = read_surface(dir_FS+'/surf/lh.inflated', itype='fs')
inf_rh = read_surface(dir_FS+'/surf/rh.inflated', itype='fs')

th_lh = dir_FS + '/surf/lh.thickness'
th_rh = dir_FS + '/surf/rh.thickness'
ths = [nib.freesurfer.read_morph_data(th_lh), nib.freesurfer.read_morph_data(th_rh)]
th_nat = np.hstack(np.concatenate((nib.freesurfer.read_morph_data(th_lh),
                                   nib.freesurfer.read_morph_data(th_rh)), axis=0))

if th_nat.shape[0] == inf_lh.n_points + inf_rh.n_points:
    print("Number of cortices and values matching")

# # plot_hemispheres(inf_lh, inf_rh, array_name=th_nat, size=(1200, 400), cmap='viridis_r',
# #                  color_bar=True, zoom=1.5)

# # Plot the surface
# # plot_hemispheres(inf_lh, inf_rh, array_name=th_nat, size=(900, 250), color_bar='bottom', zoom=1.25, embed_nb=True, 
# #                  interactive=False, share='both', nan_color=(0, 0, 0, 1), color_range=(1.5, 4), cmap="inferno", 
# #                  transparent_bg=False)

import plotly.graph_objects as go # noqa: F401

fig = plotting.plot_surf_stat_map(
    dir_FS+'/surf/lh.inflated', dir_FS+'/surf/lh.thickness', hemi='left',
    title='Surface left hemisphere', colorbar=True,
    threshold=1., #bg_map=curv_right_sign, bg_on_data=True,
    engine="plotly"  # Specify the plotting engine here
)

fig_lh = plotting.plot_surf_stat_map(
    dir_FS+'/surf/lh.inflated', dir_FS+'/surf/lh.sulc', hemi='left',
    title='Sulc left hemisphere', colorbar=True, threshold=1.,
    cmap="copper", engine="matplotlib"
)

fig_rh = plotting.plot_surf_stat_map(
    dir_FS+'/surf/rh.inflated', dir_FS+'/surf/rh.sulc', hemi='right',
    title='Sulc right hemisphere', colorbar=True, threshold=1.,
    cmap="copper", engine="matplotlib"
)

# Save the left hemisphere plot to a file
lh_filename = dir_FS + '/surf/lh_plot.png'
fig_lh.savefig(lh_filename)
plt.close(fig_lh)

# Save the right hemisphere plot to a file
rh_filename = dir_FS + '/surf/rh_plot.png'
fig_rh.savefig(rh_filename)
plt.close(fig_rh)

# # Now you have two images you can display
# filenames = [lh_filename, rh_filename]

# # fig, axs = plt.subplots(2, 2)
# # for i, ax in enumerate(axs.flat):
# #     if i < len(filenames):  # Avoid trying to load more images than you have
# #         img = mpimg.imread(filenames[i])
# #         ax.imshow(img)
# #     ax.set_axis_off()
# # plt.show()

# # dir(fig)

# # fig.savefig("test.html")

# # fig.write_html("sub-s05_ses-01_desc-thickleft_fs.html")

# import plotly.graph_objects as go  # noqa: F401

# fig = plotting.plot_surf_stat_map(
#     dir_FS+'/surf/lh.inflated', dir_FS+'/surf/lh.thickness', hemi='left',
#     title='Surface left hemisphere', colorbar=True,
#     threshold=1., #bg_map=curv_right_sign, bg_on_data=True,
#     engine="plotly"  # Specify the plotting engine here
# )
# fig.show() 
