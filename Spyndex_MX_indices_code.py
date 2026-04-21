import rasterio
from rasterio.plot import show
import numpy as np
import spyndex
import os

# Define the path to your Micasense image and the output directory
image_path = r'G:\\Jodhpur\\Processed\\140224mx.tif'
output_dir = r'G:\\Jodhpur\\indices'
os.makedirs(output_dir, exist_ok=True)

# Open the Micasense image
with rasterio.open(image_path) as src:
    # Read the image bands into numpy arrays
    red = src.read(1)
    green = src.read(2)
    blue = src.read(3)
    nir = src.read(4)
    red_edge = src.read(5)

    # Create a profile for the output files
    profile = src.profile

# List of indices to calculate
index_list = ['ARI', 'ARI2', 'ARVI', 'ATSAVI', 'AVI', 'BCC', 'BNDVI', 'BWDRVI', 'CIG', 'CIRE', 
              'CVI', 'DSWI4', 'DVI', 'EVI', 'EVI2', 'ExG', 'ExGR', 'ExR', 'FCVI', 
              'GARI', 'GBNDVI', 'GCC', 'GDVI', 'GEMI', 'GLI', 'GNDVI', 'GOSAVI', 'GRNDVI', 'GRVI', 
              'GSAVI', 'IAVI', 'IKAW', 'IPVI', 'MCARI', 'MCARI1', 'MCARI2', 'MCARIOSAVI', 'MGRVI', 
              'MNLI', 'MRBVI', 'MSAVI', 'MSR', 'MTVI1', 'MTVI2', 'NDDI', 'NDREI', 'NDVI', 
              'NDYI', 'NGRDI', 'NIRv', 'NLI', 'NormG', 'NormNIR', 'NormR', 'OCVI', 
              'OSAVI', 'RCC', 'RDVI', 'RGBVI', 'RGRI', 'RI', 'SARVI', 'SAVI', 'SAVI2', 'SI', 
              'SR', 'SR2', 'SR3', 'SeLI', 'TCARI', 'TCARIOSAVI', 'TCI', 'TDVI', 'TGI', 'TSAVI', 'TVI', 
              'TriVI', 'VARI', 'VARI700', 'VI700', 'VIG', 'WDRVI', 'WDVI']

# Define parameters for index calculation
params = {
    'N': nir,
    'N1': nir,
    'N2': nir,
    'R': red,
    'RE1': red_edge,
    'RE2': red_edge,
    'RE3': red_edge,
    'B': blue,
    'G': green,   
    'C1': 6.0,
    'C2': 7.5,
    'L': 1.0,
    'alpha': 0.1,
    'beta': 0.05,
    'c': 1.0,
    'cexp': 1.16,
    'g': 2.5,
    'gamma': 1.0,
    'nexp': 2.0,
    'omega': 2.0,
    'p': 2.0,
    'sigma': 0.5,
    'sla': 1.0,
    'slb': 0.5
}

# Function to calculate and save each index
def calculate_and_save_index(index_name, params, profile, output_dir):
    try:
        # Calculate the index
        index_result = spyndex.computeIndex(index=index_name, **params)
        
        # Save the index as a GeoTIFF file
        index_output_path = os.path.join(output_dir, f'{index_name.lower()}.tif')
        profile.update(dtype=rasterio.float32, count=1)
        
        with rasterio.open(index_output_path, 'w', **profile) as dst:
            dst.write(index_result.astype(rasterio.float32), 1)
        
        print(f'{index_name} saved to {index_output_path}')
    except Exception as e:
        print(f'Error calculating {index_name}: {e}')

# Calculate and save each index
for index_name in index_list:
    calculate_and_save_index(index_name, params, profile, output_dir)
