import random as rd
import entities
from ansimarkup import parse, ansiprint


testAct = 0

def move_after_combat(game_map,game_map_dict):
	spots = []
	
	
	mawBank = False
	for relic in entities.active_character[0].relics:
		if relic.get("Name") == "Maw Bank":
			mawBank = True
			mawBankIndex = entities.active_character[0].relics.index(relic)

	
	while True:
		try:
			i = 0
			entities.active_character[0].show_status(event=True)
			print("Where do you want to go?\n")
			for connection in game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"]:				
				if "Creep" in connection[0]:
					ansiprint(str(i+1)+". " + "<red>"+connection[0]+"</red>")
				elif "Shop$" in connection[0]:
					ansiprint(str(i+1)+". " + "<yellow>"+connection[0]+"</yellow>")
				elif "Event" in connection[0]:
					ansiprint(str(i+1)+". " + "<blue>"+connection[0]+"</blue>")
				elif "Elite" in connection[0]:
					ansiprint(str(i+1)+". " + "<m>"+connection[0]+"</m>")
				elif "Fires" in connection[0]:
					ansiprint(str(i+1)+". " + "<green>"+connection[0]+"</green>")
				elif "Boss" in connection[0]:
					ansiprint(str(i+1)+". " + "<black>"+connection[0]+"</black>")
				elif "Chest" in connection[0]:
					ansiprint(str(i+1)+". " + "<light-red>"+connection[0]+"</light-red>")
				elif "Super" in connection[0]:
					ansiprint(str(i+1)+". " + "<m>"+connection[0]+"</m>")				
				i = i + 1
			

			target = input("\nPick the place you want to go\n")
			target = int(target)-1

			if target in range(len(game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"])):
				if mawBank:
					if entities.active_character[0].relics[mawBankIndex]["Working"] == True:
						entities.active_character[0].set_gold(12)

				break
			else:
				print("You can't go there.")
				continue
		except Exception as e:
			#print (e,"an error has happened in move_after_combat")
			entities.active_character[0].explainer_function(target)
			pass

	y = game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"][target][1]
	x = game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"][target][2]
	entities.active_character[0].set_position([y,x])

	#environment_update(maps[target])


def nchoices_with_restrictions(weights=None, restrictions=None,k = 100):
    if restrictions == None:
        restrictions = {}
    N = 0 # count how many values we have yielded so far
    last_value = None # last value that was yielded
    repeat_count = 0 # how often it has been yielded in a row
    while N < k:
        while True:
            x = rd.choices(range(len(weights)), weights)[0]
            if x == last_value and repeat_count == restrictions.get(x, 0):
                continue
            break
        yield x
        N += 1
        if x == last_value:
            repeat_count += 1
        else:
            repeat_count = 1
            last_value = x


def generate_map(superElite = True):
	global testAct
	#testAct = 3
	# 0 = normal_fight
	# 1 = elite_fight
	# 2 = question_mark
	# 3 = merchant
	# 4 = bon_fire
	# 5 = treasure_room 
	# 6 = boss_fight
	# 7 = start
	paths = []
	i = 0
	while i < 5:
		lengthOfPath = 12
		roomDistribution = list(nchoices_with_restrictions([0.450,0.155,0.225,0.05,0.12],{0:2,1:1,2:1,3:1,4:1},k=lengthOfPath))
		#snap = list(nchoices_with_restrictions([0.05,0.155,0.225,0.450,0.12],{0:3,1:1,2:1,3:1,4:1},k=lengthOfPath))
		#snap = list(nchoices_with_restrictions([0.462,0.143,0.225,0.05,0.12],{0:3,1:1,2:1,3:1,4:1},k=lengthOfPath))
		#snap = list(nchoices_with_restrictions([0.480,0.128,0.24,0.05,0.12],{0:2,1:1,2:1,3:1,4:1},k=lengthOfPath))
		#snap = list(nchoices_with_restrictions([0.33,0.13,0.27,0.10,0.17],{0:3,1:1,2:1,3:1,4:1},k=13))
		roomDistribution[7] = 5
		roomDistribution[0] = 0
		if roomDistribution[lengthOfPath-1] == 4:
			randy = rd.randint(0,3)
			
			if randy == 0:
				roomDistribution[lengthOfPath-1] = 0
			
			elif randy == 1:
				roomDistribution[lengthOfPath-1] = 1
			
			elif randy == 2:
				roomDistribution[lengthOfPath-1] = 2
			
			elif randy == 3:
				roomDistribution[lengthOfPath-1] = 3

		k = 0
		while k < len(roomDistribution):
			if k < 5:
				if roomDistribution[k] == 4 or roomDistribution[k] == 1:
					
					randy = rd.randint(0,2)
			
					if randy == 0:
						roomDistribution[k] = 0
						
					elif randy == 1:
						roomDistribution[k] = 2
					
					elif randy == 2:
						roomDistribution[k] = 3
					
			if roomDistribution[k] == 0:
				roomDistribution[k] = "Creep"
			elif roomDistribution[k] == 1:
				roomDistribution[k] = "Elite"
			elif roomDistribution[k] == 2:
				roomDistribution[k] = "Event"
			elif roomDistribution[k] == 3:
				roomDistribution[k] = "Shop$"
			elif roomDistribution[k] == 4:
				roomDistribution[k] = "Fires"
			elif roomDistribution[k] == 5:
				roomDistribution[k] = "Chest"

			k += 1	
		
		paths.append(roomDistribution)
		i += 1
	

	final_map = []
	
	while len(paths[0]) > 0:
		sub_map =[]
		i = 0
		while i < len(paths): 
			sub_map.append(paths[i].pop(0))
			i += 1
		
		final_map.append(sub_map)

	

	final_map.insert(0,["Start"])
	final_map.insert(len(final_map),["Fires", "Fires", "Fires", "Fires"])
	final_map.insert(len(final_map),["Boss"])
	if testAct == 3:
		final_map.insert(len(final_map),["Boss"])

	
	y = 0
	for row in final_map:
		
		if y > 0:
			if len(row) > 1:
				snap = rd.randint(0,2)
				if snap == 0:
					pass
				elif snap == 1:
					row.pop(len(row)-1)
				elif snap == 2:
					row.pop(len(row)-1)
					row.pop(len(row)-1)
				elif snap == 3:
					row.pop(len(row)-1)
					row.pop(len(row)-1)
					row.pop(len(row)-1)
		
		y += 1
	
	if superElite == True:
	
		while True:
			superElite = rd.randint(0,len(final_map)-1)
			if "Elite" in final_map[superElite]:
				change = final_map[superElite].index("Elite")
				final_map[superElite][change] = "Super"
				break
			else:
				continue
	
	return final_map
	
def generate_connections(map_of_the_game):
	connection_dict = {}
	
	y = 0	
	for row in map_of_the_game:
	
		x = 0
		sub_dict = {}
	
		for tile in row:
	
			connections = []
	
			if y < len(map_of_the_game) - 1:
				xOne = 0
				for gyle in map_of_the_game[y+1]:
					connections.append((gyle,y+1,xOne))
					xOne += 1
			
			sub_dict[tile,y,x] = {"Type": tile,"y": y, "x":x, "Connections": connections}
			x += 1
		
		connection_dict.update(sub_dict)
		y += 1

	
	for k,v in connection_dict.items():
		i = 0
		while i < len(v["Connections"]):
			if v["Type"] != "Start":
				if abs(v["x"] - v["Connections"][i][2]) > 1:
					
					v["Connections"].pop(i)

				else:
					i += 1
			else:
				i+=1
	
	for k,v in connection_dict.items():
		i = 0
		while i < len(v["Connections"]):
			
			if v["Type"] != "Start":	
				snap = rd.randint(0,2)

				if snap == 0:
					pass
					
				elif snap == 1:
					if len(v["Connections"]) > 1:
						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))
					
				elif snap == 2:
					if len(v["Connections"]) > 2:

						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))
						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))
						
					elif len(v["Connections"]) > 1:
						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))

					else:
						pass
				i += 1
			else:
				i += 1
	

	for k,v in connection_dict.items():
		
		if len(v["Connections"]) == 0 and v["Type"] != "Boss":
				
			v["Connections"].append((map_of_the_game[v["y"]+1] [len(map_of_the_game[v["y"]+1])-1] , v["y"]+1, len(map_of_the_game[v["y"]+1])-1))

	for k,v in connection_dict.items():
		if v["Type"] != "Boss" and v["Type"] != "Start" :
			dict_reference_same_X = (map_of_the_game[v["y"]+1][0],v["y"]+1,v["x"]) 
			dict_reference_same_Y = (map_of_the_game[v["y"]][1],v["y"],v["x"]+1) 
			
			if v["x"] == 0:
				if v["Connections"][0][2] != 0 and connection_dict[dict_reference_same_Y]["Connections"][0][2] != 0:
					v["Connections"].insert(0,dict_reference_same_X)
			
			if v["x"] == len(map_of_the_game[v["y"]]) - 1:
				if len(map_of_the_game[v["y"]]) == len(map_of_the_game[v["y"]+1]):
					check = False
					for connection in v["Connections"]:
						if connection[2] == v["x"]:
							check = True

					if check == False:
						if len(v["Connections"]) == 1:
							v["Connections"].insert(1,dict_reference_same_X)
						elif len(v["Connections"]) == 0:
							v["Connections"].insert(0,dict_reference_same_X)



	rooms_without_connections = []
	
	for k,v in connection_dict.items():
		if v["Type"] != "Boss" and v["Type"] != "Start":
			x = 0
			test_list = []
			while x < len(map_of_the_game[v["y"]-1]):
				
				for connection in connection_dict[(map_of_the_game[v["y"]-1][x],v["y"]-1,x)]["Connections"]:
					test_list.append(connection)
				x += 1
				

			if (v["Type"],v["y"],v["x"]) not in test_list:

				rooms_without_connections.append((v["Type"],v["y"],v["x"]))


	
	for k,v in connection_dict.items():
		y = 0
		while y < len(rooms_without_connections):
			
			if k == rooms_without_connections[y]:
				
				while True:
					try:
						
						room_above = (map_of_the_game[k[1]-1][k[2]],k[1]-1,k[2])	
						break
					
					except Exception as e:
							
							room_on_outside_right_x = len(map_of_the_game[k[1]-1]) - 1
							room_above = (map_of_the_game[k[1]-1][room_on_outside_right_x],k[1]-1,room_on_outside_right_x)
							break



				connection_dict[room_above]["Connections"].append(rooms_without_connections.pop(y))
			else:
				y+=1
	

	for k,v in connection_dict.items():
		
		if len(v["Connections"]) > 2:	
			if v["Connections"][len(v["Connections"])-1][2] == v["Connections"][len(v["Connections"])-2][2]:
					v["Connections"].pop(len(v["Connections"])-2)

	for k,v in connection_dict.items():
		v["Connections"].sort(key=takeThird)

	return connection_dict

def generate_act4Map():
	finalAct4Map = [["Start"],["Shop$"],["Fires"],["Elite"],["Boss"]]
	return finalAct4Map

def generate_act4ConnectionDict(map_of_the_game):
	connection_dict = {}
	
	y = 0	
	for row in map_of_the_game:
	
		x = 0
		sub_dict = {}
	
		for tile in row:
	
			connections = []
	
			if y < len(map_of_the_game) - 1:
				xOne = 0
				for gyle in map_of_the_game[y+1]:
					connections.append((gyle,y+1,xOne))
					xOne += 1
			
			sub_dict[tile,y,x] = {"Type": tile,"y": y, "x":x, "Connections": connections}
			x += 1
		
		connection_dict.update(sub_dict)
		y += 1

	
	return connection_dict


def show_map(map_of_the_game,connection_dict):
	z = 0
	snaperline = ""
	
	yy = 0
	for row in map_of_the_game:
		xx = 0
		tiling = ""
		for tile in row:
			
			if yy == entities.active_character[0].position[0] and xx == entities.active_character[0].position[1]:
				tiling += "<BLUE>"+tile+"</BLUE>    "

			elif yy == entities.active_character[0].position[0] + 1:

				testDing = (map_of_the_game[yy][xx],yy,xx)	

				for connection in connection_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"]:
					if yy == connection[1] and xx == connection[2]:
						connection[0] == map_of_the_game[yy][xx]

				if testDing in connection_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"]:
					
					if testDing[0] == "Creep":
						tiling += "<red>"+tile+"</red>    "
					elif testDing[0] == "Shop$":
						tiling += "<yellow>"+tile+"</yellow>    "
					elif testDing[0] == "Event":
						tiling += "<blue>"+tile+"</blue>    "
					elif testDing[0] == "Elite":
						tiling += "<m>"+tile+"</m>    "
					elif testDing[0] == "Fires":
						tiling += "<green>"+tile+"</green>    "
					elif testDing[0] == "Boss":
						tiling += "<black>"+tile+"</black>    "
					elif testDing[0] == "Chest":
						tiling += "<light-red>"+tile+"</light-red>    "
					elif testDing[0] == "Super":
						tiling += "<m>"+tile+"</m>    "
				else:
					tiling += tile + "    "
			else:
				tiling += tile + "    "
				
			xx +=1
		ansiprint("  "+tiling)
		yy+=1

		y = 0
		all_lines = ""
		for tile in row:
			x = 0
			connector_line = ""
			for connection in connection_dict[tile,z,y]["Connections"]:
								
				if connection[0] == "Outsider":
					connector_line += "/"

				elif connection[2] < connection_dict[tile,z,y]["x"]:
					connector_line += "/"
					
				elif connection[2] == connection_dict[tile,z,y]["x"]:
					connector_line += "|"

				elif connection[2] > connection_dict[tile,z,y]["x"]:
					connector_line += "\\"
						
				x += 1
						
				all_lines += connector_line
				connector_line = ""
			y+=1

			back_spaces = ""	
			if len(all_lines) == 1:
				back_spaces = "        "
			elif len(all_lines) == 2:
				back_spaces = "       "
			elif len(all_lines) == 3:
				back_spaces = "      "

			front_spaces = ""	
			if len(all_lines) == 1:
				front_spaces = "    "
			elif len(all_lines) == 2:
				front_spaces = "  "
			elif len(all_lines) == 3:
				front_spaces = " "
			front_spaces = ""


			snaperline += front_spaces + all_lines + back_spaces
			
			all_lines = ""
		
		ansiprint("    " + snaperline)
		snaperline = ""
		z += 1

def takeThird(elem):
	return elem[2]


# =====================================================================
# Slay-the-Spire faithful map generation.
# A 15-floor x 7-column grid traversed by 6 climbing paths, with StS's room
# rules: floor 1 = Monster, floor 9 = Treasure, floor 14 = Rest, floor 15 =
# Boss (all paths converge); no Elite/Rest/Shop in the first 5 floors; the same
# special room type (Elite/Rest/Shop) never connects directly to itself; room
# weights Monster .455 / Event .22 / Elite .16 / Rest .12 / Shop .05, with Elite
# weight x1.6 at Ascension 1+. Output matches the existing game_map (list of
# rows of room-type strings, row 0 = Start, last row = Boss) and the
# connection_dict format consumed by show_map / move_after_combat.
# =====================================================================

MAP_HEIGHT = 15
MAP_WIDTH = 7
MAP_PATHS = 6

# (game_row, x) -> list of (childGameRow, childX); filled by sts_generate_map and
# read by sts_generate_connections.
map_children = {}


def _chooseNext(r, c, edges):
    cands = [c + d for d in (-1, 0, 1) if 0 <= c + d < MAP_WIDTH]

    def crosses(nc):
        # Prevent two path edges from crossing each other (an X between siblings).
        if nc > c:
            for ec in edges.get((r, c + 1), set()):
                if ec <= c:
                    return True
        elif nc < c:
            for ec in edges.get((r, c - 1), set()):
                if ec >= c:
                    return True
        return False

    nc = rd.choice(cands)
    if crosses(nc):
        alts = [x for x in cands if not crosses(x)]
        if alts:
            nc = rd.choice(alts)
    return nc


def _generatePaths():
    nodes = [set() for _ in range(MAP_HEIGHT)]
    edges = {}
    firstStart = None
    for p in range(MAP_PATHS):
        c = rd.randint(0, MAP_WIDTH - 1)
        if p == 0:
            firstStart = c
        elif p == 1:
            while c == firstStart:
                c = rd.randint(0, MAP_WIDTH - 1)
        nodes[0].add(c)
        for r in range(MAP_HEIGHT - 1):
            nc = _chooseNext(r, c, edges)
            edges.setdefault((r, c), set()).add(nc)
            nodes[r + 1].add(nc)
            c = nc
    return nodes, edges


def _pickRoom(r, c, rooms, parents, children, types, weights):
    for _ in range(50):
        t = rd.choices(types, weights)[0]
        if t in ("Elite", "Fires", "Shop$") and r <= 4:
            continue
        if t in ("Elite", "Fires", "Shop$"):
            # The same special type may not connect directly to itself (either way).
            if any(rooms.get((r - 1, pc)) == t for pc in parents.get((r, c), [])):
                continue
            if any(rooms.get((r + 1, cc)) == t for cc in children.get((r, c), [])):
                continue
        return t
    return "Creep"


def _assignRooms(nodes, edges, ascension):
    rooms = {(r, c): None for r in range(MAP_HEIGHT) for c in nodes[r]}
    for c in nodes[0]:
        rooms[(0, c)] = "Creep"          # floor 1: Monster
    for c in nodes[8]:
        rooms[(8, c)] = "Chest"          # floor 9: Treasure
    for c in nodes[13]:
        rooms[(13, c)] = "Fires"         # floor 14: Rest
    for c in nodes[MAP_HEIGHT - 1]:
        rooms[(MAP_HEIGHT - 1, c)] = "Boss"

    eliteW = 0.16 * (1.6 if ascension >= 1 else 1.0)   # Ascension 1: more Elites
    types = ["Creep", "Event", "Elite", "Fires", "Shop$"]
    weights = [0.455, 0.22, eliteW, 0.12, 0.05]

    parents = {}
    children = {}
    for (r, c), ncs in edges.items():
        children[(r, c)] = list(ncs)
        for nc in ncs:
            parents.setdefault((r + 1, nc), []).append(c)

    for r in range(1, MAP_HEIGHT - 1):
        if r in (8, 13):
            continue
        for c in sorted(nodes[r]):
            if rooms[(r, c)] is None:
                rooms[(r, c)] = _pickRoom(r, c, rooms, parents, children, types, weights)
    return rooms


def sts_generate_map(superElite=True):
    global map_children
    try:
        import helping_functions
        ascension = getattr(helping_functions, "ascensionLevel", 0)
    except Exception:
        ascension = 0

    nodes, edges = _generatePaths()
    rooms = _assignRooms(nodes, edges, ascension)

    colIndex = {}
    rows = [["Start"]]
    for r in range(MAP_HEIGHT):
        cols = sorted(nodes[r])
        for i, c in enumerate(cols):
            colIndex[(r, c)] = i
        if r == MAP_HEIGHT - 1:
            rows.append(["Boss"])
        else:
            rows.append([rooms[(r, c)] for c in cols])

    if superElite:
        elites = [(gy, x) for gy, row in enumerate(rows)
                  for x, t in enumerate(row) if t == "Elite"]
        if elites:
            gy, x = rd.choice(elites)
            rows[gy][x] = "Super"

    map_children = {}
    floor0 = sorted(nodes[0])
    map_children[(0, 0)] = [(1, i) for i in range(len(floor0))]   # Start -> floor 1
    bossRow = MAP_HEIGHT          # game row of the Boss (Start + 15 floors)
    for r in range(MAP_HEIGHT - 1):
        for c in sorted(nodes[r]):
            gy = r + 1
            x = colIndex[(r, c)]
            if r == MAP_HEIGHT - 2:
                map_children[(gy, x)] = [(bossRow, 0)]   # floor 14 (Rest) -> Boss
            else:
                map_children[(gy, x)] = sorted(
                    {(r + 2, colIndex[(r + 1, nc)]) for nc in edges.get((r, c), set())})
    map_children[(bossRow, 0)] = []
    return rows


def sts_generate_connections(map_of_the_game):
    connection_dict = {}
    for gy, row in enumerate(map_of_the_game):
        for x, tile in enumerate(row):
            conns = [(map_of_the_game[cy][cx], cy, cx)
                     for (cy, cx) in map_children.get((gy, x), [])]
            connection_dict[(tile, gy, x)] = {"Type": tile, "y": gy, "x": x, "Connections": conns}
    return connection_dict


# Use the faithful StS generators everywhere the old names are referenced.
generate_map = sts_generate_map
generate_connections = sts_generate_connections




