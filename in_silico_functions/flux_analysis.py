from cobra.io import load_model
import matplotlib.pyplot as plt

def exchange_fluxes(model, solution):
    """Makes a dictionary of exchange reactions and fluxes"""
    exchange_fluxes = {}
    for met in model.metabolites:  # same operation as "model.metabolites"
        # met = specific metabolite
        for rxn in met.reactions:  # same operation as "variable.reactions,"
            exchange_fluxes[rxn.id] = solution.fluxes[rxn.id]
    return exchange_fluxes

def analyze_fluxes(exchange_fluxes):
    """Creates a dictionary of exchange reactions and fluxes sorted by flux direction"""
    neg_flux = {}
    pos_flux = {}
    no_rxn = {}
    for rxn, flux in exchange_fluxes.items():
        if flux > 0:
            pos_flux[rxn] = flux
        if flux < 0:
            neg_flux[rxn] = flux
        if flux == 0:
            no_rxn[rxn] = flux
    return pos_flux, neg_flux, no_rxn

def plot_fluxes(d):
    """Plots fluxes for exchange reactions"""
    fluxes = list(d.values())
    exchange_rxns = list(d.keys())
    plt.bar(range(len(d)), fluxes, tick_label = exchange_rxns)
    plt.show()

def change_media(model, value = float, ex_rxn = str):
    """Changes the media for model. User specifies exchange reaction type and value."""
    with model:  # do not change model outside of "with" statement
        # alter growth media
        media = model.medium
        media["EX_glc__D_e"] = value  # enter an exchange reaction and flux value to alter growth media
        model.medium = media
        new_solution = model.optimize()
        print(new_solution.fluxes[ex_rxn])
        print(new_solution.status)
    pos_flux, neg_flux, no_rxn = analyze_fluxes(exchange_fluxes(model, new_solution))
    all_fluxes = {**pos_flux, **neg_flux}  # only includes positive and negative fluxes
    return all_fluxes

def main():
    model = load_model("iJO1366")
    solution = model.optimize()
    pos_flux, neg_flux, no_rxn = analyze_fluxes(exchange_fluxes(model, solution))

    plot_fluxes(pos_flux)

    return pos_flux, neg_flux, no_rxn

if __name__ == "__main__":
    main()


# tomorrow, plot exchange reactions against values so that we can identify how gene KOs change flux values for diff exchanges

