from flask import current_app
from app import db

class CDC_CCPhases(db.Model):
	__bind_key__='data'	
	__table__ = db.Model.metadata.tables['CDC_CCPhases']


class GEX_ProteinAbundance(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['GEX_ProteinAbundance']


class GEX_ProteinDegradation(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['GEX_ProteinDegradation']


class GEX_ProteinSynthesis(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['GEX_ProteinSynthesis']


class GEX_TranslationEfficiencies(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['GEX_TranslationEfficiencies']


class GEX_mRNAAbundance(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['GEX_mRNAAbundance']


class GEX_mRNASynthesis(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['GEX_mRNASynthesis']


class General_CellDensity(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_CellDensity']


class General_CellNumber(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_CellNumber']


class General_CellSize(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_CellSize']


class General_DryWeight(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_DryWeight']


class General_DryWeightComposition(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_DryWeightComposition']


class General_GrowthRates(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_GrowthRates']


class General_MacromoleculeAndOrganelleNumbers(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_MacromoleculeAndOrganelleNumbers']


class General_Yield(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['General_Yield']


class META_GeneIDs(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['META_GeneIDs']


class META_MediumComposition(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['META_MediumComposition']


class MET_Concentrations(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['MET_Concentrations']


class MET_EnzymeActivities(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['MET_EnzymeActivities']


class MET_LipidAbundance(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['MET_LipidAbundance']


class MET_Secretion(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['MET_Secretion']


class MET_Uptake(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['MET_Uptake']


class RELATION_Medium(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['RELATION_Medium']


class RELATION_Publication(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['RELATION_Publication']


class RELATION_Strain(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['RELATION_Strain']

class VOL_BudIndex(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['VOL_BudIndex']


class VOL_CellVolumes(db.Model):
	__bind_key__='data'
	__table__ = db.Model.metadata.tables['VOL_CellVolumes']