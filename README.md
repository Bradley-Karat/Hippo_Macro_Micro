# Code for "Mapping the macrostructure and microstructure of the in vivo human hippocampus using diffusion MRI"

Karat, B. G., DeKraker, J., Hussain, U., Köhler, S., & Khan, A. R. (2023). Mapping the macrostructure and microstructure of the in vivo human hippocampus using diffusion MRI. Human Brain Mapping. https://doi.org/10.1002/hbm.26461

Includes the following files:

cosine_similarities.py --> Cosine similarities/inner product between microstructural vectors and hippocampus axis vectors

gradient_maker.py --> Create the hippocampus axis vectors from laplace coordinates from Hippunfold

orthogonal_NMF.m --> Perform Orthogonally-projective non-negative matrix factorization using an existing MATLAB toolbox

plot_2k_flatmap.m --> Plot any metric on the midthickness surface using the GIFTI file format

MDT folder --> Code for running the microstructure models using diffusion MRI data

