from cobra.io import load_model
from pprint import pprint

# from cobra_practice_rxns_and_met import consumed_fluxes

model = load_model("textbook") # using textbook e. coli model

# global objects
carbon_sources = {}
sugars = {"Sugar" : {}}
amino_acids = {"Amino Acid" : {}}
consumed_fluxes = []
solutions = model.optimize()
#%%

for i in solutions.to_frame().index:
    if solutions.fluxes[i] < 0:
        consumed_fluxes.append(i)

def met_info(reaction):
    """creates a dictionary with rxn values for three categories (exchange rxns, formulas, and fluxes) using a reaction (or list of reactions) as an input parameter"""
    met_info = {}
    for met in reaction.metabolites: # same operation as "model.metabolites"
        # met = specific metabolite
        for i in met.reactions: # same operation as "variable.reactions,"
            # i = specific reaction
            if i in model.exchanges:
                met_info["exchange"] = i.id # reaction id
                met_info["formula"] = met.formula # metabolite formula
                met_info["flux"] = solutions.fluxes[i.id] # solution fluxes indexed at each reaction id
    return met_info, met.id

def get_fluxes(reaction):
    exchange_met = {} # creating a dictionary of metabolite info for only consumed fluxes
    for reaction_id in reaction:
        reaction = model.reactions.get_by_id(reaction_id)
        info = met_info(reaction) # passing function through
        exchange_met[info[1]] = info[0] # info[0] = met_info, info[1] = met.id
    return exchange_met
    #%%

met_info(consumed_fluxes)
get_fluxes(consumed_fluxes)

print("Hi")
# def main():
#     "calls functions"

#
# if __name__ == "__main__":
#     main()

# test