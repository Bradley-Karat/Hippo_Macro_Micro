import nibabel as nib
import numpy as np
from gradient_maker import gradient_maker
from interp_darkband import interp_darkband
import os
import pandas as pd
import subprocess
import scipy.io as sp

#calculate cosine similarities between NODDI vectors and hippocampal gradient vectors

def macro_micro_compare(in_dir,subject_txt):

	c = pd.read_csv(subject_txt)
	subject_list = c.participant_id.to_list()

	hemi = ['L','R']

	for ii in range(len(subject_list)):

		if not os.path.exists(f'{in_dir}/results/{subject_list[ii]}/macro_out'):
			os.mkdir(f'{in_dir}/results/{subject_list[ii]}/macro_out')
			os.mkdir(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-L')
			os.mkdir(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-R')

		for jj in range(len(hemi)):
			current_sub = subject_list[ii]
			current_hemi = hemi[jj]

			cmd = ['echo running: ' + current_sub + ' hemi: ' + current_hemi]  
			subprocess.call(cmd, shell=True)			

			nod_vec = nib.load(f'{in_dir}/results/{subject_list[ii]}/Diffusion/MDT_NODDI/hemi-{hemi[jj]}/NODDI_IC_corobl.vec0.nii.gz') #NODDI vectors in corobl space
			nod_vecdat = nod_vec.get_fdata()

			#Load in AP, PD, and IO laplace coordinates
			AP_lap = nib.load(f'{in_dir}/work/{subject_list[ii]}/{subject_list[ii]}_hemi-{hemi[jj]}_space-corobl_desc-cropped_modality-T2w_autotop/coords-AP.nii.gz')
			affine = AP_lap.affine
			AP_lap_dat = AP_lap.get_fdata()

			PD_lap = nib.load(f'{in_dir}/work/{subject_list[ii]}/{subject_list[ii]}_hemi-{hemi[jj]}_space-corobl_desc-cropped_modality-T2w_autotop/coords-PD.nii.gz')
			PD_lap_dat = PD_lap.get_fdata()

			IO_lap = nib.load(f'{in_dir}/work/{subject_list[ii]}/{subject_list[ii]}_hemi-{hemi[jj]}_space-corobl_desc-cropped_modality-T2w_autotop/coords-IO.nii.gz')
			IO_lap_dat = IO_lap.get_fdata()

			labmap = nib.load(f'{in_dir}/work/{subject_list[ii]}/seg_T2w/{subject_list[ii]}_hemi-{hemi[jj]}_space-corobl_desc-subfields_dseg.nii.gz')
			labelmap = labmap.get_fdata()

			coordarr = np.stack((AP_lap_dat, PD_lap_dat, IO_lap_dat), axis = -1)
			dirstring = ['AP','PD','IO']

			#Will save all gradient vectors here

			#make gradients if they don't exist
			if not os.path.isfile(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/APgradient_norm.nii.gz'):
				cmd = ['echo making normalized vectors ...']  
				subprocess.call(cmd, shell=True)

				graddir = np.zeros((AP_lap_dat.shape[0],AP_lap_dat.shape[1],AP_lap_dat.shape[2],3,3))

				for kk in range(3):

					dx,dy,dz = gradient_maker(coordarr[:,:,:,kk])

					x = np.stack((dx, dy, dz), axis = -1)

					normgradvec = np.empty((x.shape))
					normnodvec = np.empty((x.shape))
				
					for aa in range(x.shape[0]):
						for bb in range(x.shape[1]):
							for cc in range(x.shape[2]):
								for dd in range(x.shape[3]):
									if nod_vecdat[aa,bb,cc,dd] != 0:
										normnod = np.linalg.norm(nod_vecdat[aa,bb,cc,:])
										normnodvec[aa,bb,cc,dd] = nod_vecdat[aa,bb,cc,dd]/normnod    
									else:
										normnodvec[aa,bb,cc,dd] = 0
									if x[aa,bb,cc,dd] != 0:
										normvec = np.linalg.norm(x[aa,bb,cc,:])
										normgradvec[aa,bb,cc,dd] = x[aa,bb,cc,dd]/normvec        
									else:
										normgradvec[aa,bb,cc,dd] = 0

					graddir[:,:,:,:,kk] = normgradvec[:,:,:,:]

					#Save normalized gradient and NODDI vectors
					newer = nib.Nifti1Image(normgradvec, affine)
					nib.save(newer,(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/{dirstring[kk]}gradient_norm.nii.gz'))

					newer1 = nib.Nifti1Image(normnodvec, affine)
					nib.save(newer1,(f'{in_dir}/results/{subject_list[ii]}/NODDI/hemi-{hemi[jj]}/NODDI_IC_corobl_norm.vec0.nii.gz'))
			
			#if gradient vectors already exist load them in here
			else:
				APnorm = nib.load(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/APgradient_norm.nii.gz')
				APnorm = APnorm.get_fdata()
				PDnorm = nib.load(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/PDgradient_norm.nii.gz')
				PDnorm = PDnorm.get_fdata()
				IOnorm = nib.load(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/IOgradient_norm.nii.gz')
				IOnorm = IOnorm.get_fdata()
				graddir = np.empty((AP_lap_dat.shape[0],AP_lap_dat.shape[1],AP_lap_dat.shape[2],3,3))
				graddir[:,:,:,:,0] = APnorm
				graddir[:,:,:,:,1] = PDnorm
				graddir[:,:,:,:,2] = IOnorm

				normnodvec = nib.load(f'{in_dir}/results/{subject_list[ii]}/NODDI/hemi-{hemi[jj]}/NODDI_IC_corobl_norm.vec0.nii.gz')
				normnodvec= normnodvec.get_fdata()

			APcoshold = np.zeros((normnodvec.shape[0],normnodvec.shape[1],normnodvec.shape[2]))
			PDcoshold = np.zeros((normnodvec.shape[0],normnodvec.shape[1],normnodvec.shape[2]))
			IOcoshold = np.zeros((normnodvec.shape[0],normnodvec.shape[1],normnodvec.shape[2]))
			
			if not os.path.isfile(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/combined_cos_similarity_corobl.nii.gz'):
				cmd = ['echo calculating cosine similarities ...']  
				subprocess.call(cmd, shell=True)

				#Calculate cosine similarities
				for aa in range(graddir.shape[0]):
					for bb in range(graddir.shape[1]):
						for cc in range(graddir.shape[2]):
							APcoshold[aa,bb,cc] = np.abs(graddir[aa,bb,cc,:,0] @ normnodvec[aa,bb,cc,:])
							PDcoshold[aa,bb,cc] = np.abs(graddir[aa,bb,cc,:,1] @ normnodvec[aa,bb,cc,:])
							IOcoshold[aa,bb,cc] = np.abs(graddir[aa,bb,cc,:,2] @ normnodvec[aa,bb,cc,:])

				#Save cosine similarities
				newer2 = nib.Nifti1Image(APcoshold, affine)
				nib.save(newer2,(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/AP_cos_similarity_corobl.nii.gz'))

				newer3 = nib.Nifti1Image(PDcoshold, affine)
				nib.save(newer3,(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/PD_cos_similarity_corobl.nii.gz'))

				newer4 = nib.Nifti1Image(IOcoshold, affine)
				nib.save(newer4,(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/IO_cos_similarity_corobl.nii.gz'))

				combcorobl = np.stack((APcoshold[:,:,:], PDcoshold[:,:,:], IOcoshold[:,:,:]), axis = -1)
				newer5 = nib.Nifti1Image(combcorobl, affine)
				nib.save(newer5,(f'{in_dir}/results/{subject_list[ii]}/macro_out/hemi-{hemi[jj]}/combined_cos_similarity_corobl.nii.gz'))

