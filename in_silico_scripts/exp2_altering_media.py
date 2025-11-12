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
