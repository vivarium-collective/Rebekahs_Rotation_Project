import cobra
from cobra.io import read_sbml_model
from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from cobra.medium import minimal_medium

from process_bigraph import Composite
from process_bigraph import ProcessTypes
from process_bigraph.emitter import gather_emitter_results

from cdFBA import register_types
from cdFBA.processes.dfba import dFBA, UpdateEnvironment, StaticConcentration, Injector, WaveFunction

from cdFBA.utils import make_cdfba_composite, get_injector_spec, get_wave_spec, get_static_spec, set_concentration, set_kinetics, get_exchanges

from in_silico_functions.carbon_sources import (load, met_info, find_fluxes, make_fluxes_dict, make_dict,main, classify_met)
from in_silico_functions.mini_medium import get_mini_medium

#%%
# load models

gut_models = {
        "B_thetaiotaomicron": "/Users/rebekahsheih/PycharmProjects/Rebekahs_Rotation_Project/in_silico_scripts/sbml/Bacteroides_thetaiotaomicron_VPI_5482.xml",
        "E_rectale": "/Users/rebekahsheih/PycharmProjects/Rebekahs_Rotation_Project/in_silico_scripts/sbml/Eubacterium_rectale_ATCC_33656.xml",
        "Methanobrevibacter_smithii": "/Users/rebekahsheih/PycharmProjects/Rebekahs_Rotation_Project/in_silico_scripts/sbml/Methanobrevibacter_smithii_ATCC_35061.xml"
    }

models = {k: read_sbml_model(v) for k, v in gut_models.items()}

BT = models["B_thetaiotaomicron"]
ER = models["E_rectale"]
MS = models["Methanobrevibacter_smithii"]

#%%
# Create minimal media
medium_bt = get_mini_medium(BT)[0]
medium_bt["EX_MGlcn175_rl(e)"] = 0.00
medium_bt["EX_cholate(e)"] = 0.00
# medium_bt["EX_hspg(e)"] = 0.00  # kill switch
BT.medium = medium_bt

medium_er = get_mini_medium(ER)[0]
medium_er["EX_ac(e)"] = 0 # bacteria must consume acetate from another bacteria, not environment
ER.medium = medium_er


medium_ms = get_mini_medium(MS)[0]
MS.medium = medium_ms

#%%
# optimize solution
BT.optimize()
ER.optimize()
MS.optimize()

#%%
# make spec
exchanges = ['EX_ac(e)', 'EX_but(e)', 'EX_ch4(e)','EX_cholate(e)', 'EX_pullulan1200(e)', 'EX_co2(e)', 'EX_h(e)'] # acetate, butyrate, H2, methane, cholate, pullulan, reaction intermediates (CO2, H)

volume = 2

#%%
# dFBA model
spec = make_cdfba_composite(gut_models, medium_type=None, exchanges=exchanges, volume=volume, interval=0.1)

pprint(spec)

#%%
# add mini media to spec
mini_media = {"B_thetaiotaomicron" : medium_bt,
              "E_rectale" : medium_er,
              "Methanobrevibacter_smithii" : medium_ms}

for species, medium in mini_media.items():
    spec["Species"][species]["config"]["medium"] = medium

#Set reaction bounds (constrain bounds here to make it so that the exchange reactions can't take place)
spec['Species']['B_thetaiotaomicron']['config']['bounds'] = {
            "EX_o2(e)": {"lower": -2, "upper": None},
            "DM_atp_c_": {"lower": 1, "upper": 1},
        }
spec['Species']['E_rectale']['config']['bounds'] = {
            "EX_o2(e)": {"lower": -2, "upper": None},
            "DM_atp_c_": {"lower": 1, "upper": 1}
        }
#%%
#set external substrate concentrations
concentrations = {
    'acetate': 0,       # limit acetate
    'butyrate': 0,
    'Cholate' : 10, # give cholate so that BT can grow and produce acetate for ER
    'pullulan (n=1200 repeat units, alpha-1,4 and alph-1,6 bounds)' : 10, # ER uses in tandem w/acetate
    'Methane' : 0,
    'carbon dioxide' : 0,
    'proton' : 0

}
set_concentration(spec, concentrations)
#%%
#set kinetics
kinetics = {
    'acetate': (0.5, 5), # reduce km, increase Vmax
    'butyrate': (0.5, 5),
    'Cholate': (0.5, 5),
    'pullulan (n=1200 repeat units, alpha-1,4 and alph-1,6 bounds)' : (0.5, 5),
    'Methane' : (0.5, 5),
    'carbon dioxide' : (0.5, 5),
    'proton' : (0.5, 5)
}
for species in gut_models.keys():
    set_kinetics(species, spec, kinetics)
pprint(spec)
#%%
#set emitter specs
spec['emitter'] = {
        "_type": "step",
        "address": "local:ram-emitter",
        "config": {
            "emit": {
                "shared_environment": "any",
                "global_time": "any",
            }
        },
        "inputs": {
            "shared_environment": ["Shared Environment"],
            "global_time": ["global_time"]
        }
    }
#%%
#create the core object
core = ProcessTypes()
#register data types
core = register_types(core)
#register all processes and steps
core.register_process('dFBA', dFBA)
core.register_process('UpdateEnvironment', UpdateEnvironment)
core.register_process('StaticConcentration', StaticConcentration)
core.register_process('WaveFunction', WaveFunction)
core.register_process('Injector', Injector)
#%%
# KO all reactions for one species
#%%
sim = Composite({
        "state": spec,
        },
        core=core
    )
#%%
#run simulation
sim.run(20)
#%%
#gather results
results = gather_emitter_results(sim)[('emitter',)]
#%%
#extract time-series data
timepoints = []
for timepoint in results:
    time = timepoint.pop('global_time')
    timepoints.append(time)
env = [timepoint['shared_environment']['concentrations'] for timepoint in results]
env_combined = {}
for d in env:
    for key, value in d.items():
        if key not in env_combined:
            env_combined[key] = []
        env_combined[key].append(value)
#%%
# results
#%%
#plot results for biomass
fig, ax = plt.subplots(dpi=300)
for key, value in env_combined.items():
    if key not in ['acetate', 'butyrate', 'Cholate', 'pullulan (n=1200 repeat units, alpha-1,4 and alph-1,6 bounds)', 'Methane', 'carbon dioxide', 'proton']:
        ax.plot(timepoints, env_combined[key], label=key)
        ax.set_yscale('log')
# plt.ylim(1, 10e3) # zoomed in
plt.xlabel('Time (h)')
plt.ylabel('Biomass (gDW)')
plt.legend()
plt.tight_layout()
plt.show()
#%%
#plot substrates
fig, ax = plt.subplots(dpi=300)
for key, value in env_combined.items():
    if key in ['acetate', 'Cholate', 'butyrate', 'Methane', 'pullulan (n=1200 repeat units, alpha-1,4 and alph-1,6 bounds)']:
        ax.plot(timepoints, env_combined[key], label=key)
        ax.set_yscale('log')
# plt.ylim(1, 10e4) # zoomed in
plt.xlabel('Time (h)')
plt.ylabel('Substrate Concentration (mM)')
plt.legend()
plt.tight_layout()
plt.show()