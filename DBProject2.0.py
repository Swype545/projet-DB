
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
		print("Les parametres entres doivent etre des floats.")
		return 0


	#On recupere l'ensemble des connections
	try:
		collections = db.collection_names(include_system_collections=False)
	except:
		print("Impossible de trouver les collections.")
		return 0
	playersList = []

	#On boucle sur toutes les collections
	try:
		for collection in collections:
			#On boucle sur tout les joueurs dans la collection donnee
			for player in db[collection].find({"argent":{ "$gt": limitPO} }):
				playersList.append(player)
	except:
		print("Erreur lors de la requete de connection aux collections")
		return 0

	if(len(playersList) > 0):
		return playersList
	else:
		print("Aucun joueur ne possede plus de cette somme.")
		return 0

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

#Troisieme fonction: realiser un groupe constitue de tanks, de dps, de heal avec un niveau d'objet (ilvl) minimum donne en parametres
def createGroup(limitTank, limitHeal, limitDps):
	
	#Gestion d'erreur
	if((type(limitTank) == float) or (type(limitTank) == int)):
		i = 0
	else:
		print("Les parametres entres doivent etre des floats.")
		return 0
	
	if((type(limitHeal) == float) or (type(limitHeal) == int)):
		i = 0
	else:
		print("Les parametres entres doivent etre des floats.")
		return 0
	
	if((type(limitDps) == float) or (type(limitDps) == int)):
		i = 0
	else:
		print("Les parametres entres doivent etre des floats.")
		return 0
	
	#On recupere l'ensemble des collections de la db
	try:
		collections = db.collection_names(include_system_collections=False)
	except:
		print("Impossible de trouver les collections.")
		return 0
	
	#On initialise le groupe
	party = {
		"tank":[],
		"heal":[],
		"dps":[],
		
		"tankTotilvl": 0,
		"healTotilvl": 0,
		"dpsTotilvl": 0
	}
	
	#On realise les requetes pour recuperer les infos
	#Recuperer les TANKS
	
	for player in db.guerrier.find({"$and": [{"specialisation":"protection"}, {"niveau":110}]}):

		#Si la limite de niveau d'objet n'est pas atteinte
		if(party['tankTotilvl'] < limitTank):
			#On check s'il a un ilvl definit (verification). Si non, il n'est pas comptabilise
			if("ilvl" in player):
				party['tankTotilvl'] += player["ilvl"]
				#On ajoute le joueur a l'array "tank"
				party['tank'].append(player)
		
	if(party['tankTotilvl'] < limitTank):
		print("pas assez de tank disponible dans la DB")
		return 0

	
	#Recupere les HEALS
	for player in db.pretre.find({"$and": [{"specialisation":"Sacre"}, {"niveau":110}]}):	
		#Si la limite de niveau d'objet n'est pas atteinte
		if(party['healTotilvl'] < limitHeal):
			#Verification de la presence de l'ilvl dans "player" avant l'ajout
			if("ilvl" in player):
				party['healTotilvl'] += player["ilvl"]
				party['heal'].append(player)
	
	if(party['healTotilvl'] < limitHeal):
		print("pas assez de heal disponible dans la DB")
		return 0
	
	#Recupere les DPS (soit guerrier arme, soit mage, soit voleur)
	#Array tampon
	guerriersDPS = []
	magesDPS = []
	voleursDPS = []
	
	for player in db.guerrier.find({"$and": [{"specialisation":"arme"}, {"niveau":110}]}):
		guerriersDPS.append(player)
		
	for player in db.mage.find({"niveau":110}):
		magesDPS.append(player)
	
	for player in db.voleur.find({"niveau":110}):
		voleursDPS.append(player)
	
	while(party['dpsTotilvl'] < limitDps):
		add = 0

		#On verifie qu'il y'a encore des personnages dans l'array
		if(len(guerriersDPS) >= 1):
			if(party['dpsTotilvl'] < limitDps):
				#Verification de la presence de l'ilvl dans "player" avant l'ajout
				if("ilvl" in guerrierDPS[add]):
					party['dps'].append(guerriersDPS[add])
					party['dpsTotilvl'] += guerriersDPS[add]["ilvl"]
					del guerriersDPS[add]

			else:
				#On break si plus de place en DPS
				break
		
		if(len(magesDPS) >= 1):
			if(party['dpsTotilvl'] < limitDps):
				#Verification de la presence de l'ilvl dans "player" avant l'ajout
				if("ilvl" in magesDPS[add]):
					party['dps'].append(magesDPS[add])
					party['dpsTotilvl'] += magesDPS[add]["ilvl"]
					del magesDPS[add]
			else:
				break
				
		if(len(voleursDPS) >= 1):
			if(party['dpsTotilvl'] < limitDps):
				#Verification de la presence de l'ilvl dans "player" avant l'ajout
				if("ilvl" in voleursDPS[add]):
					party['dps'].append(voleursDPS[add])
					party['dpsTotilvl'] += voleursDPS[add]["ilvl"]
					del voleursDPS[add]
			else:
				break
		
		add += 1
		
		#S'il n'y a plus assez de DPS pour former le groupe, on break, et on affichera un message d'erreur.
		if( (len(guerriersDPS) == 0) and (len(magesDPS) == 0) and (len(voleursDPS) == 0)):
			break 


	if(party['dpsTotilvl'] < limitDps):
		print("pas assez de DPS disponible dans la DB")
		return 0
	
	
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
    
    print("\n---------------------------------------------------")
    print("Debut des tests")
    print("---------------------------------------------------\n")

    print("Peuplement de la base de donnees...")
    populate()

    print("---------------------------------------------------\n")

    #Commande qui renvoit les personnages en entier (l'ensemble du dictionnaire):
    #pprint.pprint(playerGoldOver(2000))

    print("Recuperation des personnages avec plus de 2000 pieces d'or... (affichage des noms uniquement)")
    value = playerGoldOver(20000)
    if (value != 0):
	    for player in value:
	    	print(player["nom"])

    print("---------------------------------------------------\n")

    #Commande qui renvoit les personnages en entier (l'ensemble du dictionnaire):
    #pprint.pprint(hasRecipeInJob('alchimiste','potion de mana'))
    print("Recuperation des personnages etant 'alchimiste' avec la recette 'potion de mana'... (affichage des noms uniquement)")
    value = hasRecipeInJob('alchimiste','potion de mana')
    if(value != 0):
	    for player in value:
	    	print(player["nom"])

    print("---------------------------------------------------\n")

    #Commande qui renvoit les personnages en entier (l'ensemble du dictionnaire):
    #pprint.pprint(createGroup(800,800,1000))
    print("Creation d'un groupe de personnes avec un niveau d'objet minimum de 800 pour les tanks, 800 pour les heals et 1000 pour les dps... (affichage des noms uniquement)")
    newgroup = createGroup(800,800,1800)
    if(newgroup != 0):
	    print(" ")

	    print("Tank:")
	    print("----")
	    for tank in newgroup["tank"]:
	    	print(tank["nom"])
	    print(" ")

	    print("Heal:")
	    print("----")
	    for heal in newgroup["heal"]:
	    	print(heal["nom"])
	    print(" ")

	    print("Dps:")
	    print("----")
	    for dps in newgroup["dps"]:
	    	print(dps["nom"])
	    print(" ")
