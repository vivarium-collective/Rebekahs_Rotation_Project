from cobra.io import load_model
from in_silico_functions.flux_analysis import (change_media, plot_fluxes)

from in_silico_functions.carbon_sources import (load, classify_met)

from pprint import pprint


def main():
    model, solutions = load("iJO1366")
    # first, change media

    all_fluxes = change_media(model, 0.00, "EX_glc__D_e")

    plot_fluxes(all_fluxes)

    # second, see if carbon source has changed
    carbon_sources = classify_met(model, solutions)
    pprint(carbon_sources)
    return carbon_sources

if __name__ == "__main__":
    main()

# result: when the media is changed, metabolite availability changes and the model organism cannot grow (or must find alternative food sources).
