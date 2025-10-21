from cobra.io import load_model
from pprint import pprint

def load(s):
    model = load_model(s)
    solutions = model.optimize()
    return model, solutions

def met_info(reaction, model, solutions): # this function is not successfully creating a dict
    """creates a dictionary with rxn values for three categories (exchange rxns, formulas, and fluxes) using a reaction (or list of reactions) as an input parameter"""
    met_info_dict = {}
    for met in reaction.metabolites:  # same operation as "model.metabolites"
        # met = specific metabolite
        for rxn in met.reactions:  # same operation as "variable.reactions,"
            # rxn = specific reaction
            if rxn.id in model.exchanges:
                met_info_dict["exchange"] = rxn.id  # reaction id
                met_info_dict["formula"] = met.formula  # metabolite formula
                met_info_dict["flux"] = solutions.fluxes[rxn.id]  # solution fluxes indexed at each reaction id
    return met_info_dict, rxn.id, met.formula  #innermost dictionary

def find_fluxes(solutions):
    "creates and returns a list of consumed fluxes in model organism"
    # Perhaps there is only one relevant exchange rxn here.
    consumed_fluxes = []
    for i in solutions.to_frame().index:
        if solutions.fluxes[i] < 0:
            consumed_fluxes.append(i)
    return consumed_fluxes

def make_fluxes_dict(model, solutions): # passes met_info through
    "creates a dictionary with exchange reaction metabolite info"
    consumed_fluxes = find_fluxes(solutions)
    exchange_met = {}
    for reaction_id in consumed_fluxes:
        reaction = model.reactions.get_by_id(reaction_id)
        met_info_dict, rxn_id, met_formula = met_info(reaction, model, solutions)  # passing function through
        exchange_met[rxn_id] = met_info_dict
    # pprint(f"This is what classify_met uses: {exchange_met}") # this dictionary is populating just fine
    return exchange_met

def make_dict(dict_1, dict_2):
    "creates and returns a parent dictionary with two nested dictionaries"
    merged_dict = {**dict_1, **dict_2}
    return merged_dict

def classify_met(model, solutions): # the problem is that we're overwriting sugars somewhere
    "Creates two dictionaries from nested dictionary with exchange rxn metabolite info"
    exchange_met = make_fluxes_dict(model, solutions) # creates exchange_met dictionary

    sugars = {"Sugars": {}}
    amino_acids = {"Amino Acids": {}}

    for key, value in exchange_met.items():
        if "formula" in value:
            formula = value["formula"]
            if "formula" in value:
                if all(elem in formula for elem in ['C', 'H', 'O']):
                    sugars["Sugars"][key] = value
            if "formula" in value:
                if all(elem in formula for elem in ['C', 'H', 'O', 'N']):
                    amino_acids["Amino Acids"][key] = value
    carbon_sources = make_dict(amino_acids, sugars)
    return carbon_sources

def main():
    "calls functions"

    model, solutions = load("textbook")
    carbon_sources = classify_met(model, solutions)
    pprint(carbon_sources)
    return carbon_sources

if __name__ == "__main__":
    main()

# Results
# There is only one relevant carbon sources involved in an exchange reaction in this organism.
# It is a sugar.
# There are no amino acids involved in exchange reactions in this organism.