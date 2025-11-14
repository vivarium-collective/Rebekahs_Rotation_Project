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

def get_mini_medium(model, target_growth=10e-4):
    ## make a copy of the model
    try_model = model.copy()

    ## compute the minimum media neccessary for growth at targeted_growth
    mini_growth = minimal_medium(try_model, target_growth, minimize_components=10, open_exchanges=True)

    ## set minimal medium
    mini_medium = {}
    for i in mini_growth.index:
        mini_medium[i] = try_model.medium[i]

    ## get all other metabolites that can be added to the medium
    additional_medium = try_model.medium
    for i in mini_medium.keys():
        del additional_medium[i]
    return mini_medium, additional_medium


gut_models = {
        "B_thetaiotaomicron": "/Users/rebekahsheih/PycharmProjects/Rebekahs_Rotation_Project/Vivarium/cdFBA-main/Notebooks/sbml/Bacteroides_thetaiotaomicron_VPI_5482.xml",
        "E_rectale": "/Users/rebekahsheih/PycharmProjects/Rebekahs_Rotation_Project/Vivarium/cdFBA-main/Notebooks/sbml/Eubacterium_rectale_ATCC_33656.xml"
    }

models = {k: read_sbml_model(v) for k, v in gut_models.items()}

BT = models["B_thetaiotaomicron"]
ER = models["E_rectale"]

medium_bt = get_mini_medium(BT)[0]
medium_bt["EX_MGlcn175_rl(e)"] = 0.00
medium_bt["EX_cholate(e)"] = 1000.00 # want bt to consume cholate and produce acetate for er to eat

BT.medium = medium_bt

medium_er = get_mini_medium(ER)[0]
medium_er["EX_pullulan1200(e)"] = 10e-6 # if this number is small enough, er produces more butyrate
medium_er["EX_ac(e)"] = 0 # want ER to consume acetate from bt, so don't give it acetate.
# I am seeing that organism consumes acetate and pullulan together, but does not consume acetate unless there is enough pullulan in media.
# w/o acetate, uses more pullulan1200, w/acetate, consumes both
ER.medium = medium_er


cobra.io.write_sbml_model(BT, "sbml/bt.xml")
bt_try = read_sbml_model("sbml/bt.xml")
bt_try.optimize()
print(bt_try.summary())

cobra.io.write_sbml_model(ER, "sbml/er.xml")
er_try = read_sbml_model("sbml/er.xml")
er_try.optimize()
print(er_try.summary())
