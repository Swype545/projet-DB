
# -*- coding: ascii -*-
#Liaison avec la db MongoDB
import pymongo
from pymongo import MongoClient
client = MongoClient ('localhost', 27017)
db = client['laboDB']


#Creation de la premiere collection: les Mages
mageColl = db['mage']
magus = {"nom":"Magus",
		"niveau":110,
		"specialisation":"Feu",
		"baguette":"Felo'Melorn",
		"robe":"Grande Robe de Magie Superieure",
		"metier":{"nom":"alchimiste",
			"patron": ["fiole de soin", "potion de mana","potion d'invisibilite mineure"]
			},
		"competenceVol":"true",
		"argent":2675
		}

antonin = {"nom":"Antonin",
		"niveau":87,
		"specialisation":"Givre",
		"baguette":"Baton de magie inferieure",
		"robe":"Robe du Dragon Noir",
		"guilde":"Les rapiats",
		"competenceVol":"false",
		"argent":27.3
		}

db.mage.insert(magus)
db.mage.insert(antonin)

#Creation de la seconde collection: les Guerriers

yassinus = {"nom":"Yassinus",
		"niveau":110,
		"specialisation":"arme",
		"epeeG":"Lame du prince dechu",
		"epeeD":"Lame de guerre d'ebene glaciale",
		"armure":"Armure du Tueur de Dragons",
		"guilde":"Les reveurs du Dimanche",
		"metier":{"nom":"Mineur"},
		"competenceVol":"false",
		"argent":17523
		}

zakkarioum = {"nom":"Zakkarioum",
		"niveau":25,
		"specialisation":"protection",
		"epee":"Cure dent du templier",
		"bouclier":"Targe ebrechee",
		"Armure":"Armure du Tueur de Dragons",
		"competenceVol":"false",
		"argent":1.17
		}

db.guerrier.insert(yassinus)
db.guerrier.insert(zakkarioum)

#Creation de la troisieme collection: les Pretres
pretreColl = db['pretre']
moiselium = {"nom":"Moiselium",
		"niveau":108,
		"specialisation":"Sacre",
		"baton":"Branche de l'Arbre Monde",
		"robe":"Robe du soigneur indecis",
		"guilde":"Les reveurs du Dimanche",
		"competenceVol":"true",
		"argent":124
		}
db.pretre.insert(moiselium)



#Creation de la quatrieme collection: les voleur


abdelicieux = {"nom":"Abdelicieux",
		"niveau":110,
		"specialisation":"finesse",
		"dagueG":"Dent de Mannoroth",
		"dagueD":"Dent de Mannoroth",
		"armure":"Ensemble du gladiateur farouche en Cuir",
		"guilde":"Les reveurs du Dimanche",
		"metier":{"name":"Cuisinier",
			"patron":["omelette d'autruche","Salade azshari", "Salade azshari"]
			},
		"competenceVol":"true",
		"argent":2750
		}
db.voleur.insert(abdelicieux)
