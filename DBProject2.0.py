
# -*- coding: ascii -*-
#Liaison avec la db MongoDB
import pymongo
import pprint
from pymongo import MongoClient
client = MongoClient ('localhost', 27017)
db = client['laboDB']


#Premiere requete: recuperer une liste de joueur avec plus de "limitPO" de pieces d'or
def playerGoldOver(limitPO):
	#erreurs
	if((type(limitPO) == float) or (type(limitPO) == int)):
		i = 0
	else:
		return "Les parametres entres doivent etre des floats."


	#On recupere l'ensemble des connections
	try:
		collections = db.collection_names(include_system_collections=False)
	except:
		return "Impossible de trouver les collections."
	playersList = []

	#On boucle sur toutes les collections
	try:
		for collection in collections:
			#On boucle sur tout les joueurs dans la collection donnee
			for player in db[collection].find({"argent":{ "$gt": limitPO} }):
				playersList.append(player)
	except:
		return "Erreur lors de la requete de connection aux collections"

	if(len(playersList) > 0):
		return playersList
	else:
		return "Aucun joueur ne possede plus de cette somme."


#Seconde requete: recuperer une liste de personnage qui ont le metier "job" et qui peuvent creer "recipe"
def hasRecipeInJob(job, recipe):
	
	#erreurs
	if((type(job) != str) or (type(job) != str)):
		return "Le metier et la recette enregistree doivent etre des strings."

	#On recupere l'ensemble des connections
	try:
		collections = db.collection_names(include_system_collections=False)
	except:
		return "Impossible de trouver les collections."
	playersList = []

	#On boucle sur toutes les collections
	try:
		for collection in collections:
			#On boucle sur tout les joueurs dans la collection
			for player in db[collection].find({"$and": [{"metier.nom":job}, {"metier.patron":recipe}]}):
				playersList.append(player)
				
	except:
		return "Erreur lors de la requete de connection aux collections"

	if(len(playersList) > 0):
		return playersList
	else:
		return "Aucun joueur ne possede cette recette."

#Troisieme requete: constituer un groupe ayant un ilvl plus grand que "sommeilvl" avec des pourcentage donnes
'''def findGroup5(sommeilvl, pourcentmage, pourcentguerrier,pourcentpretre, pourcentvoleur):
	
	if(pourcentmage+pourcentguerrier+pourcentpretre+pourcentvoleur != 1):
		return "Il faut que la somme des pourcentage donne 1."

	if((type(sommeilvl) == float) or (type(sommeilvl) == int)):
		i = 0
	else:
		return "Les parametres entres doivent etre des floats."

	if((type(pourcentmage) != float) or (type(pourcentguerrier) != float) or (type(pourcentpretre) != float) or (type(pourcentvoleur) != float)):
		return "Les parametres entres doivent etre des floats."

	#On cree la liste qui comprendra le groupe
	party_mage = []
	party_guerrier = []
	party_pretre = []
	party_voleur = []
	#On cree une variable ilvl du groupe. De base, elle est initialisee a 0.
	ilvl_party= 0

	mages = []
	guerriers = []
	pretres = []
	voleurs = []
	
	try:
		collections = db.collection_names(include_system_collections=False)
	except:
		return "Impossible de trouver les collections."


	try:
		for collection in collections:
			#On boucle sur tout les joueurs dans la collection donnee
			print(collection)
			for player in db[collection].find({"niveau":110}):
				if(collection == "mage"):
					mages.append(player)
				if(collection == "guerrier"):
					guerriers.append(player)
				if(collection == "pretre"):
					pretres.append(player)
				if(collection == "voleur"): 
					voleurs.append(player)
	except:
		return "Erreur lors de la requete de connection aux collections"

	for player in mages:
		if(pourcentmage*5 > len(party_mage)):
			party_mage.append(player)
			ilvl_party += player["ilvl"]
			print(ilvl_party)
			mages.remove(player)


	#print(mages, guerriers, pretres, voleurs)


	db.mage.find_one({"ilvl": {"$gt":800}})
	db.guerrier.find_one({"ilvl":{"$gt":((800+"$ilvl")/2)}})



	db.guerrier.aggregate({
		"$project":{
			"moyenne":{
				"$multiply":[("$add":[800, "$ilvl"]), (1/2)]
			}
		}
	})'''

	
#Troisieme fonction: realiser un groupe constitué de tanks, de dps, de heal avec un niveau d'objet (ilvl) minimum donne en parametres
def createGroup(limitTank, limitHeal, limitDps):
	
	#Gestion d'erreur
	if((type(limitTank) == float) or (type(limitTank) == int)):
		i = 0
	else:
		return "Les parametres entres doivent etre des floats."
	
	if((type(limitHeal) == float) or (type(limitHeal) == int)):
		i = 0
	else:
		return "Les parametres entres doivent etre des floats."
	
	if((type(limitDps) == float) or (type(limitDps) == int)):
		i = 0
	else:
		return "Les parametres entres doivent etre des floats."
	
	#On recupere l'ensemble des collections de la db
	try:
		collections = db.collection_names(include_system_collections=False)
	except:
		return "Impossible de trouver les collections."
	
	#On initialise le groupe
	party = {
		"tank":[],
		"heal":[],
		"dps":[],
		
		"tankTotilvl" = 0,
		"healTotilvl" = 0,
		"dpsTotilvl" = 0
	}
	
	#On realise les requetes pour recuperer les infos
	#Recuperer les TANKS
	
	for player in db[guerriers].find({"$and": [{"specialisation":"protection"}, {"niveau":110}):

		#Si la limite de niveau d'objet n'est pas atteinte
		if(party['tankTotilvl'] < limitTank):
			party['tank'].append(player)
			party['tankTotilvl'] += player["ilvl"]
		
	if(party['tankTotilvl'] < limitTank):
		return "pas assez de tank disponible dans la DB"

	
	#Recupere les HEALS
	for player in db[pretre].find({"$and": [{"specialisation":"Sacre"}, {"niveau":110}):	
		#Si la limite de niveau d'objet n'est pas atteinte
		if(party['healTotilvl'] < limitHeal):
			party['heal'].append(player)
			party['healTotilvl'] += player["ilvl"]
	
	if(party['healTotilvl'] < limitHeal):
		return "pas assez de heal disponible dans la DB"
	
	#Recupere les DPS (soit guerrier arme, soit mage, soit voleur)
	#Array tampon
	guerriersDPS = []
	magesDPS = []
	voleursDPS = []
	
	for player in db[guerrier].find({"$and": [{"specialisation":"arme"}, {"niveau":110}):
		guerriersDPS.append(player)
		
	for player in db[mage].find({"niveau":110}):
		magesDPS.append(player)
	
	for player in db[voleur].find({"niveau":110}):
		voleursDPS.append(player)
	
	while(party['dpsTotilvl'] < limitDps):
		add = 0
		if(len(guerriersDPS) >= add+1):
			if(party['dpsTotilvl'] < limitDps):
				party['dps'].append(guerriersDPS[add])
			else:
				break
		
		if(len(magesDPS) >= add+1):
			if(party['dpsTotilvl'] < limitDps):
				party['dps'].append(magesDPS[add])
			else:
				break
				
		if(len(voleursDPS) >= add+1):
			if(party['dpsTotilvl'] < limitDps):
				party['dps'].append(voleursDPS[add])
			else:
				break
		
		add += 1
	
	if(party['dpsTotilvl'] < limitDps):
		return "pas assez de DPS disponible dans la DB"
	
	
	return party
		
def populate():
	#Creation de la premiere collection: les Mages
	mageColl = db['mage']
	magus = {
				"nom":"Magus",
				"niveau":110,
				"ilvl":850,
				"label":"DPS",
				"specialisation":"Feu",
				"baguette":"Felo'Melorn",
				"robe":"Grande Robe de Magie Superieure",
				"metier":[
					{
						"nom":"alchimiste",
						"patron": ["fiole de soin", "potion de mana","potion d'invisibilite mineure"]
					}
				],
				"competenceVol":"true",
				"argent":2675
			}

	antonin = {
				"nom":"Antonin",
				"niveau":87,
				"ilvl":613,
				"label":"DPS",
				"specialisation":"Givre",
				"baguette":"Baton de magie inferieure",
				"robe":"Robe du Dragon Noir",
				"guilde":"Les rapiats",
				"competenceVol":"false",
				"argent":27.3
			}

	db.mage.update(magus, magus, upsert=True)
	db.mage.update(antonin, antonin, upsert=True)

	#Creation de la seconde collection: les Guerriers

	yassinus = {
				"nom":"Yassinus",
				"niveau":110,
				"ilvl":855,
				"label":"Tank",
				"specialisation":"protection",
				"epee":"Cure dent du templier",
				"bouclier":"Targe ebrechee",
				"armure":"Armure du Tueur de Dragons",
				"guilde":"Les reveurs du Dimanche",
				"metier":[
					{
						"nom":"Mineur"
					}
				],
				"competenceVol":"false",
				"argent":17523
			}

	zakkarioum = {
				"nom":"Zakkarioum",
				"niveau":25,
				"ilvl":125,
				"label":"DPS",
				"specialisation":"arme",
				"epeeG":"Lame du prince dechu",
				"epeeD":"Lame de guerre d'ebene glaciale",
				"armure":"Armure du Tueur de Dragons",
				"competenceVol":"false",
				"argent":1.17
			}

	db.guerrier.update(yassinus, yassinus, upsert=True)
	db.guerrier.update(zakkarioum, zakkarioum, upsert=True)

	#Creation de la troisieme collection: les Pretres
	pretreColl = db['pretre']
	moiselium = {
				"nom":"Moiselium",
				"niveau":110,
				"ilvl":800,
				"specialisation":"Sacre",
				"label":"Heal",
				"baton":"Branche de l'Arbre Monde",
				"robe":"Robe du soigneur indecis",
				"guilde":"Les reveurs du Dimanche",
				"competenceVol":"true",
				"argent":124
			}
	db.pretre.update(moiselium, moiselium, upsert=True)



	#Creation de la quatrieme collection: les voleur


	abdelicieux = {
				"nom":"Abdelicieux",
				"niveau":110,
				"ilvl":837,
				"specialisation":"finesse",
				"label":"DPS",
				"dagueG":"Dent de Mannoroth",
				"dagueD":"Dent de Mannoroth",
				"armure":"Ensemble du gladiateur farouche en Cuir",
				"guilde":"Les reveurs du Dimanche",
				"metier":[
					{
						"name":"Cuisinier",
						"patron":["omelette d'autruche","Salade azshari", "Salade azshari"]
					}
				],
				"competenceVol":"true",
				"argent":2750
			}

	marcus = {
				"nom":"Marcus",
				"niveau":110,
				"ilvl":789,
				"specialisation":"assassinat",
				"label":"DPS",
				"epeeG":"Lame du voleur",
				"epeeD":"Epee fourbe",
				"armure":"Ensemble du meurtrier sanglant",
				"guilde":"Les reveurs du Dimanche",
				"metier":[
					{
						"nom":"alchimiste",
						"patron": ["fiole de soin", "skrixswaggle", "potion de vitesse","potion d'invisibilite mineure"]
					}
				],
				"competenceVol":"true",
				"argent":12723
			}
	db.voleur.update(abdelicieux, abdelicieux, upsert=True)
	db.voleur.update(marcus, marcus, upsert=True)

if __name__ == "__main__":
    print("Peuplement de la base de donnees...")
    populate()

    print("Recuperation des pieces d'or...")
    pprint.pprint(playerGoldOver(2000))

    print("Recuperation des personnages etant 'alchimiste' avec la recette 'potion de mana'...")
    pprint.pprint(hasRecipeInJob('alchimiste','potion de mana'))

    #print("Creation d'un groupe de 5 personnes...")
    #pprint.pprint(findGroup5(100000.0, 0.4,0.2,0.2,0.2))
