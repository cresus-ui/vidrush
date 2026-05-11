
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.services import nlp

script = "Le monde du football n'est pas seulement un spectacle de talents sur le terrain, c'est aussi un univers où les fortunes se comptent en millions, voire en milliards. Qui sont ces athlètes d'exception dont la richesse dépasse l'entendement ? Des icônes comme Cristiano Ronaldo et Lionel Messi dominent invariablement ce classement, leurs salaires faramineux complétés par des contrats de sponsoring colossaux avec les plus grandes marques mondiales. Mais ils ne sont pas seuls ; des joueurs tels que Neymar Jr., avec ses transferts records et ses partenariats lucratifs, ou encore Kylian Mbappé, dont la valeur marchande et les revenus publicitaires explosent, figurent également parmi les plus nantis. Ces footballeurs ne se contentent pas de leurs émoluments sportifs ; ils investissent judicieusement dans l'immobilier, la mode, la technologie et d'autres entreprises, bâtissant ainsi des empires financiers qui perdureront bien après la fin de leur carrière sur les pelouses."

people = nlp.extract_people(script)
print(f"Extracted people: {people}")
