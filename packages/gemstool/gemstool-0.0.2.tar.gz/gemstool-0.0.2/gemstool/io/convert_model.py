#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Hao Luo at 2019-06-20

"""io.py
:description : script
:param : 
:returns: 
:rtype: 
"""

def solution2txt(solution,model,outfile):
    # function : convert cobra FBA result to txt file

    need_fluxes =solution.fluxes[abs(solution.fluxes)>1e-10]
    with open(outfile,'w') as outf:
        for need_id in need_fluxes.index:
            rea = model.reactions.get_by_id(need_id)
            #print (need_id,need_fluxes[need_id],rea.reaction,rea.lower_bound,rea.upper_bound,rea.objective_coefficient)
            outline_list = [need_id,str(need_fluxes[need_id]),rea.reaction,str(rea.lower_bound),str(rea.upper_bound),str(rea.objective_coefficient)]
            #print (outline_list)
            outf.write("\t".join(outline_list)+'\n')

def gem2txt(model,outfile,sort=False):
    # function : convert cobra model to a txt file
    with open(outfile, 'w') as outf:
        reaidlist = [i.id for i in model.reactions ]
        if sort == True:
            reaidlist.sort()
        for reaid in reaidlist:
            rea = model.reactions.get_by_id(reaid)
            outline_list = [reaid, rea.reaction, str(rea.objective_coefficient),str(rea.lower_bound), str(rea.upper_bound),rea.gene_reaction_rule,str(rea.notes)]
            outf.write("\t".join(outline_list) + '\n')

def gem2cb(model,outfile,sort=False):
    # function : convert cobra GEM to cybernetic model file

    file = open(outfile,'w')

    file.write('-ENZREV\n\n')

    file.write('-ENZIRREV\n\n')

    file.write('-METEXT\n\n')

    METEXT = []
    for met in model.metabolites:
        if '_e' in met.id:
            METEXT.append(met.id)

    file.write(' '.join(METEXT))

    file.write('\n-CAT\n')

    for rea in model.reactions:
        file.write(rea.id +' : ')
        equ = rea.reaction
        equ = equ.replace('-->','=>')
        equ = equ.replace('<=>','=')
        equ = equ.replace('<--','<=')
        file.write(equ +' .\n')
    file.close()
