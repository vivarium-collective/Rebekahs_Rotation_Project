from cobra.io import load_model
from pprint import pprint
from in_silico_functions.carbon_sources import (load, met_info, find_fluxes,
                                                make_fluxes_dict, make_dict,
                                                classify_met)

def main():
    "calls functions"
    print("stopping right before the breakpoint")
    model, solutions = load()
    carbon_sources = classify_met(model, solutions)
    pprint(carbon_sources)
    return carbon_sources

if __name__ == "__main__":
    main()