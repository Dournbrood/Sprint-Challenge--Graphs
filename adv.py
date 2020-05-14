from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []

shortest_path = []

visited = {}

last_move = None

reverses = {"n": "s", "e": "w", "s": "n", "w": "e", }


def my_algorithm():
    # If the length of our rooms visited is equal to the length of our room graph, we're done.
    while len(visited.keys()) != len(room_graph):

        # Get current room and exits.
        if player.current_room.id not in visited.keys():
            visited[player.current_room.id] = {}

            for direction in player.current_room.get_exits():
                visited[player.current_room.id][direction] = "?"

        # If the room you're in has no exits at all or all adjacent rooms are ones you've explored, backtrack until this is no longer the case.
        if len(visited[player.current_room.id].keys()) > 0 and "?" not in visited[player.current_room.id].values():
            backtrack_moves = []

            while len(visited[player.current_room.id].keys()) > 0 and "?" not in visited[player.current_room.id].values():
                reverse_move = reverses[shortest_path[-1]]
                player.travel(reverse_move)
                shortest_path.pop()
                backtrack_moves.append(reverse_move)
                # return

            for move in backtrack_moves:
                traversal_path.append(move)

        # For each unexplored neighbor of the current room, move to it and add the direction you moved to the path.
        for direction, room in visited[player.current_room.id].items():
            if room == "?":
                last_move = (player.current_room.id, direction)
                player.travel(direction)
                traversal_path.append(direction)
                shortest_path.append(direction)
                visited[last_move[0]][last_move[1]] = player.current_room.id

                if player.current_room.id not in visited.keys():
                    visited[player.current_room.id] = {}

                    for direction2 in player.current_room.get_exits():
                        visited[player.current_room.id][direction2] = "?"

                visited[player.current_room.id][reverses[direction]] = last_move[0]

                break

    return


my_algorithm()

# TRAVERSAL TEST - DO NOT MODIFY


visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
