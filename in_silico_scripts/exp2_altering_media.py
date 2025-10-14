# Next direction: media change = starvation
## PtsG
# - Phosphorylated PtsG is an intermediate during transport and phosphorylation of glucose
# - Pathways: ptsG expresses right at glycolysis I (from glucose 6-phosphate), superpathway of glycolysis, pyruvate dehydrogenase, TCA, and glyoxylate bypass, and Pathway 'superpathway of glycolysis and the Entner-Doudoroff pathway
# - Enzymes: -6-phosphofructokinase 1 [PfkA]4 6-phosphofructokinase 2 [PfkB]2
# - In the absence of glucose, expression of ptsG is repressed (Question: How do we know if glucose is present in our model?)
# - Thought: If ptsG is naturally repressed in absence of glucose, then cell can survive temporarily w/o expression of ptsG.
# - Should look at exchange fluxes
# - RESEARCH QUESTION: What is it eating??????
# - Before KO - is this eating glucose? Something else? Do this before KO.
# - What is e. coli eating and WHEN is e. coli eating it?
# - Is ptsG eating something other than glucose?
# - Approach: determine what e. coli is eating by plotting exchange reactions (glucose, lactose, O2, etc.)
#           against fluxes. Measure flux levels with diff KOs to determine which pathways are used when


# Pos control: rpos (stress response)


from cobra.io import load_model
from in_silico_functions.flux_analysis import (exchange_fluxes, analyze_fluxes,
                                               plot_fluxes, load_model)

def main():
    model = load_model("iJO1366")
    solution = model.optimize()
    with model:  # do not change model outside of "with" statement
        # alter growth media
        media = model.medium
        media["EX_glc__D_e"] = 0.00 # enter an exchange reaction and flux value to alter growth media
        model.medium = media
        new_solution = model.optimize()
        print(new_solution.fluxes["EX_glc__D_e"])
        print(new_solution.status)
    pos_flux, neg_flux, no_rxn = analyze_fluxes(exchange_fluxes(model, new_solution))
    all_fluxes = {**pos_flux, **neg_flux} # only includes positive and negative fluxes

    plot_fluxes(all_fluxes)

if __name__ == "__main__":
    main()


# result: when the media is changed, metabolite availability changes and the model organism cannot grow (or must find alternative food sources).
