#Lists and Dictionaries on how to display database table and which columns to select as default
dtypes=["Metabolite or ion concentration","Secretion rates of metabolites or ions","Uptake rates of metabolites or ions", "mRNA abundance","mRNA synthesis rates","mRNA degradation rates","Protein abundance","Protein synthesis rates","Protein degradation rates","Concentrations of lipids","Durations of cell cycle phases","Cell numbers","Cell sizes","Cell volumes","Cell (dry) weights","Information on the composition of the cell dry weight","Culture yields"]
dtypeIdentifier=["ChEBI_ID","ChEBI_ID","ChEBI_ID","Flux type", "ORF (SGD)","ORF (SGD)","ORF (SGD)","ORF (SGD)","ORF (SGD)","ORF (SGD)","Lipid class abberviation and chains","none","none","none","none","none","Cellular component","none"]
ttypes=["metabolite_concentrations","secretion_rates","uptake_rates","mRNA_abundance","mRNA_synthesis","mRNA_degradation","protein_abundance","protein_synthesis","protein_degradation","lipids_abundance","cellcycle_duration","cell_number","cell_size","cell_volume","dry_weight","weight_composition","yield"]
DownloadDict={}
DownloadDict["choices"]=[(i,j) for i,j in zip(ttypes, dtypes)]
DownloadDict["identifier"]={i:j for i,j in zip(ttypes, dtypeIdentifier)}


navigationTabs = {
"metabolic":{"tables":["MET_Concentrations", "MET_EnzymeActivities", "MET_LipidAbundance", "MET_Secretion", "MET_Uptake"],
  "display":["Concentrations", "Enzyme Activities", "Lipid Abundance", "Secretion", "Uptake"], 
  "default":["Author_Year", "Strain_ID", "Medium_ID", "Numerical_Value", "Unit", "Value_Type", "Method"],
  },
"proteomic":{"tables":["GEX_ProteinAbundance", "GEX_ProteinDegradation", "GEX_ProteinSynthesis", "GEX_TranslationEfficiencies", "GEX_mRNAAbundance", "GEX_mRNASynthesis"],
  "display":["Protein Abundance", "Protein Degradation", "Protein Synthesis", "Translation Efficiencies", "mRNA Abundance", "mRNA Synthesis"],
  "default":["Author_Year", "Strain_ID", "Medium_ID", "Numerical_Value", "Unit", "Value_Type", "Method"],
  },
"biophysical":{"tables":["CDC_CCPhases", "General_CellDensity", "General_CellNumber", "General_CellSize", "General_DryWeight", "General_DryWeightComposition", "General_GrowthRates", "General_MacromoleculeAndOrganelleNumbers", "General_Yield", "VOL_BudIndex", "VOL_CellVolumes"],
  "display":["Cell Cycle Phases", "Cell Density", "Cell Number", "Cell Size", "Dry Weight", "Dry Weight Composition", "Growth Rates", "Organelles", "Yield", "Bud Index", "Cell Volumes"],
  "default":["Author_Year", "Strain_ID", "Medium_ID", "Numerical_Value", "Unit", "Value_Type", "Method"],
  }
}

primaryIdentifier={'CDC_CCPhases': ['Stress', 'Phase'], 
'GEX_ProteinAbundance': ['ORF', 'Gene_Name'], 
'GEX_ProteinDegradation': ['ORF', 'Gene_Name'], 
'GEX_ProteinSynthesis': ['ORF', 'Gene_Name'], 
'GEX_TranslationEfficiencies': ['ORF', 'Gene_Name'], 
'GEX_mRNAAbundance': ['ORF', 'Gene_Name'], 
'GEX_mRNASynthesis': ['ORF', 'Gene_Name'], 
'General_CellDensity': [], 
'General_CellNumber': [], 
'General_CellSize': ['Size_Type'], 
'General_DryWeight': ['Dried'], 
'General_DryWeightComposition': ['Compound', 'Compartment'], 
'General_GrowthRates': ["Growth_Phase", "Growth_Rate_Type"], 
'General_MacromoleculeAndOrganelleNumbers': ['Org_MMolec'], 
'General_Yield': ['Compound', 'ChEBI_ID'], 
'MET_Concentrations': ['Compound', 'ChEBI_ID', 'Compartment'], 
'MET_EnzymeActivities': ['Enzyme', 'EC_Nr', 'Compartment'], 
'MET_LipidAbundance': ['Lipid_Class', 'Chains'], 
'MET_Secretion': ['Compound', 'ChEBI_ID', 'Compartment'], 
'MET_Uptake': ['Compound', 'ChEBI_ID', 'Compartment'], 
'VOL_BudIndex': [], 
'VOL_CellVolumes': ['Compartment']
}

displayColumnNames = {'Numerical_Value':'Numerical Value', 'Unit':'Unit', 'Value_Type':'Value Type', 'Author_Year':'Publication',
 'Publication_Link':'PubMed', 'Strain_ID':'Strain', 'Medium_ID':'Medium', 'Growth_Rate':'Growth Rate',
  'Growth_Rate_Type':'Growth Rate (Type)', 'Stress':'Stress', 'Phase':'Phase', 'Value':'Value', 'Average':'Average', 'Std_Dev':'Standard Deviation',
   'N_Replications':'# Replications', 'Median':'Median', 'Min':'Min', 'Max':'Max', 'Synchronisation':'Synchronisation', 'Comment':'Comment',
    'Culture':'Culture', 'Temperature':'Temperature [°C]', 'uniqueID':'ID', 'Method':'Method', 'Growth_Phase':'Growth Phase', 'Aeration':'Aeration',
     'ORF':'ORF', 'Gene_Name':'Gene_Name', 'Time':'Time', 'Time_Unit':'Time Unit', 'Type':'Type', 'Size_Type':'Size_Type', 'Dried':'Dried',
      'Compound':'Compound', 'Compartment':'Compartment', 'Org_MMolec':'Organelle/Macromolecule', 'ChEBI_ID':'ChEBI', 'Uniprot_Name':'Uniprot Name',
       'SwissProt_ID':'SwissProt', 'Uniprot_ID':'Uniprot', 'SGD_ID':'SGD', 'Gene_Description':'Gene Description', 'SGD_Name':'SGD Name',
        'Medium_uniqueID':'Medium', 'Component':'Component', 'PubChem':'PubChem', 'Enzyme':'Enzyme', 'EC_Nr':'EC',
         'Lipid_Class':'Lipid Class', 'Chains':'Chains', 'pH':'pH', 'CDC_CCPhases':'Cell Cycle Phases', 'GEX_ProteinAbundance':'Protein Abundance',
          'GEX_ProteinDegradation':'Protein Degradation', 'GEX_ProteinSynthesis':'Protein Synthesis',
           'GEX_TranslationEfficiencies':'Translation Efficiencies', 'GEX_mRNAAbundance':'mRNA Abundance',
            'GEX_mRNADegradation':'mRNA Degradation', 'GEX_mRNASynthesis':'mRNA Synthesis', 'General_CellDensity':'Cell Density',
             'General_CellNumber':'Cell Number', 'General_CellSize':'Cell Size', 'General_DryWeight':'Dry Weight',
              'General_DryWeightComposition':'Dry Weight Composition', 'General_GrowthRates':'Growth Rates',
               'General_MacromoleculeAndOrganelleNumbers':'Macromolecules & Organelles', 'General_Yield':'Yield',
                'MET_Concentrations':'Concentrations', 'MET_EnzymeActivities':'Enzyme Activities', 'MET_LipidAbundance':'Lipid Abundance',
                 'MET_Secretion':'Secretion', 'MET_Uptake':'Uptake', 'VOL_BudIndex':'Bud Index', 'VOL_CellVolumes':' Cell Volumes',
                  'First_Author':'First Author', 'Year':'Year', 'Title':'Title', 'Authors':'Authors', 'Affiliation':'Affiliation',
                   'Abstract':'Abstract', 'Crossref':'Crossref', 'PublicationInfo':'PublicationInfo', 'MET_AminoAcidUptake':'Amino Acid Uptake',
                    'Closest_Ancestor':'Closest Ancestor', 'Synonyms':'Synonyms', 'Ploidity':'Ploidity', 'Mating_Type':'Mating Type',
                     'Mutations':'Mutations', 'Mutations.1':'Mutations 1', 'Mutations.2':'Mutations 2', 'Mutations.3':'Mutations 3',
                      'Mutations.4':'Mutations 4', 'Mutations.5':'Mutations 5', 'Mutations.6':'Mutations 6', 'Mutations.7':'Mutations 7',
                       'Mutations.8':'Mutations 8', 'Mutations.9':'Mutations 9', 'Mutations.10':'Mutations 10', 'Mutations.11':'Mutations 11',
                        'Mutations.12':'Mutations 12', 'Link':'Link', 'Table_Name':'Table Name', 'Displayed_Name':'Displayed Name',
                         'version_num':'Version'}


TableColumns={'CDC_CCPhases': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Growth_Rate', 'Growth_Rate_Type', 'Stress', 'Phase', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Synchronisation', 'Comment', 'Culture', 'Temperature', 'uniqueID', 'Method'], 
'GEX_ProteinAbundance': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'ORF', 'Gene_Name', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'GEX_ProteinDegradation': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'ORF', 'Gene_Name', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Type', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'GEX_ProteinSynthesis': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'ORF', 'Gene_Name', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'GEX_TranslationEfficiencies': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'ORF', 'Gene_Name', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'GEX_mRNAAbundance': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'ORF', 'Gene_Name', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'GEX_mRNASynthesis': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'ORF', 'Gene_Name', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'General_CellDensity': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'General_CellNumber': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'General_CellSize': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Size_Type', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'General_DryWeight': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Dried', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'General_DryWeightComposition': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Compound', 'Compartment', 'Temperature', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Time', 'Culture', 'uniqueID'], 
'General_GrowthRates': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate_Type', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'uniqueID', 'Numerical_Value', 'Value_Type'], 
'General_MacromoleculeAndOrganelleNumbers': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Org_MMolec', 'Phase', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'General_Yield': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Compound', 'ChEBI_ID', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'META_GeneIDs': ['Uniprot_Name', 'ORF', 'SwissProt_ID', 'Uniprot_ID', 'SGD_ID', 'Gene_Description', 'SGD_Name', 'uniqueID'], 
'META_MediumComposition': ['Medium_uniqueID', 'Component', 'PubChem', 'Value', 'Unit', 'uniqueID'], 
'MET_Concentrations': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Compound', 'ChEBI_ID', 'Compartment', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Max', 'Min', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'MET_EnzymeActivities': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Enzyme', 'EC_Nr', 'Compartment', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'uniqueID'], 
'MET_LipidAbundance': ['Lipid_Class', 'Chains', 'Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Growth_Rate', 'Growth_Rate_Type', 'Temperature', 'Synchronisation', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Aeration', 'Culture', 'uniqueID'], 
'MET_Secretion': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'Compound', 'ChEBI_ID', 'Compartment', 'uniqueID'], 
'MET_Uptake': ['Publication_Link', 'Strain_ID', 'Medium_ID', 'Author_Year', 'Culture', 'Growth_Phase', 'Temperature', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Compound', 'ChEBI_ID', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Unit', 'Method', 'Comment', 'Numerical_Value', 'Value_Type', 'Compartment', 'uniqueID'], 
'RELATION_Medium': ['Publication_Link', 'Medium_ID', 'pH', 'uniqueID', 'CDC_CCPhases', 'GEX_ProteinAbundance', 'GEX_ProteinDegradation', 'GEX_ProteinSynthesis', 'GEX_TranslationEfficiencies', 'GEX_mRNAAbundance', 'GEX_mRNADegradation', 'GEX_mRNASynthesis', 'General_CellDensity', 'General_CellNumber', 'General_CellSize', 'General_DryWeight', 'General_DryWeightComposition', 'General_GrowthRates', 'General_MacromoleculeAndOrganelleNumbers', 'General_Yield', 'MET_Concentrations', 'MET_EnzymeActivities', 'MET_LipidAbundance', 'MET_Secretion', 'MET_Uptake', 'VOL_BudIndex', 'VOL_CellVolumes'], 
'RELATION_Publication': ['Publication_Link', 'First_Author', 'Year', 'uniqueID', 'Title', 'Authors', 'Author_Year', 'Affiliation', 'Abstract', 'Crossref', 'CDC_CCPhases', 'GEX_mRNAAbundance', 'GEX_mRNADegradation', 'GEX_mRNASynthesis', 'GEX_ProteinAbundance', 'GEX_ProteinDegradation', 'GEX_ProteinSynthesis', 'PublicationInfo', 'General_CellNumber', 'General_CellDensity', 'General_DryWeightComposition', 'General_DryWeight', 'General_CellSize', 'General_GrowthRates', 'MET_LipidAbundance', 'MET_AminoAcidUptake', 'MET_EnzymeActivities', 'General_Yield', 'VOL_BudIndex', 'VOL_CellVolumes', 'MET_Concentrations', 'MET_Secretion', 'MET_Uptake', 'General_MacromoleculeAndOrganelleNumbers', 'GEX_TranslationEfficiencies'], 
'RELATION_Strain': ['Strain_ID', 'Closest_Ancestor', 'Synonyms', 'Ploidity', 'Mating_Type', 'Mutations', 'Mutations.1', 'Mutations.2', 'Mutations.3', 'Mutations.4', 'Mutations.5', 'Mutations.6', 'Mutations.7', 'Mutations.8', 'Mutations.9', 'Mutations.10', 'Mutations.11', 'Mutations.12', 'Comment', 'Link', 'uniqueID', 'CDC_CCPhases', 'GEX_mRNAAbundance', 'GEX_mRNADegradation', 'GEX_mRNASynthesis', 'GEX_ProteinAbundance', 'GEX_ProteinDegradation', 'GEX_ProteinSynthesis', 'GEX_TranslationEfficiencies', 'General_CellNumber', 'General_CellDensity', 'General_DryWeightComposition', 'General_DryWeight', 'General_MacromoleculeAndOrganelleNumbers', 'General_CellSize', 'General_GrowthRates', 'MET_LipidAbundance', 'MET_EnzymeActivities', 'General_Yield', 'VOL_BudIndex', 'VOL_CellVolumes', 'MET_Concentrations', 'MET_Secretion', 'MET_Uptake'], 
'Table_Names': ['Table_Name', 'Displayed_Name'], 
'VOL_BudIndex': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'VOL_CellVolumes': ['Numerical_Value', 'Unit', 'Value_Type', 'Author_Year', 'Publication_Link', 'Strain_ID', 'Medium_ID', 'Synchronisation', 'Aeration', 'Growth_Rate', 'Growth_Rate_Type', 'Compartment', 'Phase', 'Time', 'Time_Unit', 'Value', 'Average', 'Std_Dev', 'N_Replications', 'Median', 'Min', 'Max', 'Growth_Phase', 'Method', 'Comment', 'Culture', 'Temperature', 'uniqueID'], 
'alembic_version': ['version_num']}

relTables = ['CDC_CCPhases', 'GEX_ProteinAbundance', 'GEX_ProteinDegradation', 'GEX_ProteinSynthesis', 'GEX_TranslationEfficiencies', 'GEX_mRNAAbundance', 'GEX_mRNASynthesis', 'General_CellDensity', 'General_CellNumber', 'General_CellSize', 'General_DryWeight', 'General_DryWeightComposition', 'General_GrowthRates', 'General_MacromoleculeAndOrganelleNumbers', 'General_Yield', 'MET_Concentrations', 'MET_EnzymeActivities', 'MET_LipidAbundance', 'MET_Secretion', 'MET_Uptake', 'VOL_BudIndex', 'VOL_CellVolumes']
