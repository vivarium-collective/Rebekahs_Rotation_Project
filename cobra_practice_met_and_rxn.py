from cobra.io import load_model
from pprint import pprint

from cobra_practice_met_and_rxn import carbon_sources

def load():
    model = load_model("textbook")
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

    return met_info_dict, rxn.id  #innermost dictionary

def find_fluxes(model, solutions):
    "creates and returns a list of consumed fluxes in model organism"

    consumed_fluxes = []
    for i in solutions.to_frame().index:
        if solutions.fluxes[i] < 0:
            consumed_fluxes.append(i)
    return consumed_fluxes

def make_fluxes_dict(model, solutions): # passes met_info through
    "creates a dictinoary with exchange reaction metabolite info"

    consumed_fluxes = find_fluxes(model, solutions)
    exchange_met = {}

    for reaction_id in consumed_fluxes:
        reaction = model.reactions.get_by_id(reaction_id)
        met_info_dict, rxn_id = met_info(reaction, model, solutions)  # passing function through
        exchange_met[rxn_id] = met_info_dict
    # pprint(f"This is what classify_met uses: {exchange_met}") # this dictionary is populating just fine
    return exchange_met

def make_dict(dict_1, dict_2):
    "creates and returns a parent dictionary with two nested dictionaries"
    merged_dict = {**dict_1, **dict_2}
    pprint(f' printing from make_dict function {merged_dict}')
    return merged_dict

def classify_met(model, solutions): # i think the problem is here. Not adding anything to dicts
    "Creates two dictionaries from nested dictionary with exchange rxn metabolite info"
    count = 0
    exchange_met = make_fluxes_dict(model, solutions) # creates exchange_met dictionary

    sugars = {"Sugar": {}}
    amino_acids = {"Amino Acid": {}}

    for key, value in exchange_met.items():
        if "formula" in value:
            pprint(value["formula"])

    for key, value in exchange_met.items():
        if "formula" in value:
            if all(elem in value["formula"] for elem in ['C', 'H', 'O']):
                sugars["Sugar"][key] = value
                count +=1

    for key, value in exchange_met.items():
        if "formula" in value:
            if all(elem in value["formula"] for elem in ['C', 'H', 'O', 'N']):
                amino_acids["Amino Acid"][key] = value
    print(count)
    # carbon_sources = make_dict(amino_acids, sugars)
    return sugars, amino_acids

def main():
    "calls functions"
    model, solutions = load()
    sugars, amino_acids = classify_met(model, solutions)
    # pprint(f'We have {len(sugars)} in nested sugars.')
    # pprint(f'We have {len(amino_acids)} nested amino acids.')
    carbon_sources = make_dict(sugars, amino_acids)
    # return carbon_sources

if __name__ == "__main__":
    main()