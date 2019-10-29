#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import rnaseq_barcode as rnaseq

#%%
# Set plotting style
rnaseq.viz.pboc_style_mpl()
colors = sns.color_palette('colorblind', n_colors=6)

# Set the experiment constants.
DATE = 20191022
RUN_NO = 1

# Load the data set.
fc_file = glob.glob('output/*fold_change.csv')[0]
data = pd.read_csv(fc_file)

#%%
# Compute theoretical fold-change

# Import constants
constants = rnaseq.thermo.load_constants()

# Define unique repressors
rep = np.sort(data.repressors.unique())
rep = rep[rep > 0]

# Define range of IPTG
iptg = np.logspace(-1, np.log10(5000), 50)

# Define binding energy of operator
era = constants['O2']

# Generate meshgrid to feed into function
rr, ii = np.meshgrid(rep, iptg)
ee = np.ones_like(rr) * era

# Instantiate simple repression class
theory = rnaseq.thermo.SimpleRepression(rr, ee, effector_conc=ii, 
                                        ka=constants['Ka'], ki=constants['Ki'],
                                        ep_ai=constants['ep_AI'])

# Compute fold-change
fc_theory = theory.fold_change().T
#%%
# Instantiate the figure canvas
fig, ax = plt.subplots(1, 1)

# Add labels and scaling
ax.set_xlabel('IPTG (M)')
ax.set_ylabel('fold-change')
ax.set_xscale('log')

# Group the data by operator
# Remove auto and delta.
fc = data.loc[(data['strain'] != 'auto') & (data['strain'] != 'delta')]
grouped = fc.groupby(['strain', 'repressors', 'operator'])

# Plot the inensity curves.
for i, (g, d) in enumerate(grouped):
    # Plot theoretical fold-change
    _ = ax.plot(iptg / 1E6, fc_theory[i, :], '-',
                color=colors[i], label='')
    # Plot data
    _ = ax.plot(d['IPTGuM'] / 1E6, d['fold_change'], '--o',
                color=colors[i], label=g, markersize=5)

# Add a legend.
_ = ax.legend(loc='upper left', title='operator')
ax.set_ylim([-0.1, 2])
# Save the figure.
plt.savefig('output/fold_change_curve.png')


# %%