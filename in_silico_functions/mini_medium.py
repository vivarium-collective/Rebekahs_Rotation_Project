from cobra.medium import minimal_medium ## Copy of Edwin's function

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