# perpetual predator prey cycles
# conway's game of life

# This works with now predators, just prey and food, so lvl 1 perpetual prey food successful
# This also works with one predator (tweaks will need to be made to the predator code to keep it as one)

import random
import logging

logging.basicConfig(filename='predator_prey.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#rules
# T reproduces every round by duplication, nothing needed
# Predator eats Prey, Prey eats Food
# Prey reproduces if it eats T
# Predator reproduces if it eats O
# food can't move
# prey can move
# predator can move
# prey and predator need to be set up a a dict so that their params, hunger, reproduce bool..., are available
# when prey eats food, food takes an extra round to grow
# predator prey based on rules from game of life, if to many they die

#TODO: allow to go in 'circles' from 9->0 0->9
#TODO: Give safe spots for prey to hide but where food won't grow


def create_predator(predator, starvation_countdown=0):
    if starvation_countdown == 0:
        return {
            'Type': predator,
            'starvation countdown': 5,
        }
    else:
        return {
            'Type': predator,
            'starvation countdown': starvation_countdown,
        }


def create_prey(prey):
    return {
        'Type': prey
    }


def create_food(food):
    return {
        'Type': food
    }


def init():
    global world, predator, prey, food
    # build world
    world = [
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None]
    ]

    predator = 'Wolf Pack'
    prey = 'Rabbit Colony'
    food = 'Carrot Bunch'

    population_count = 8
    start_position = []
    for position in range(population_count):
        pos = [random.randrange(10), random.randrange(10)]
        while pos in start_position:
            pos = [random.randrange(10), random.randrange(10)]
        else:
            start_position.append(pos)
    # randomly place them onto the world
  #  world[start_position[0][0]][start_position[0][1]] = create_predator(predator, 15)
    world[start_position[2][0]][start_position[2][1]] = create_prey(prey)
    world[start_position[3][0]][start_position[3][1]] = create_prey(prey)
    world[start_position[4][0]][start_position[4][1]] = create_food(food)
    world[start_position[5][0]][start_position[5][1]] = create_food(food)
  #  world[start_position[6][0]][start_position[6][1]] = create_prey(prey)
  #  world[start_position[7][0]][start_position[7][1]] = create_prey(prey)

    for row in world:
        print(row)


def food_placement():
    food_positions = []

    for row in range(len(world)):
        for cell in range(len(world[row])):
            cell_value = world[row][cell]
            if cell_value is not None:
                if cell_value['Type'] == food:
                    food_positions.append([row, cell])

    logging.debug(f'Food positions: {food_positions}')
    # get square around food and randomly throw another food in there if it is empty
    for food_position in food_positions:
        free = []

        # Check three cells above
        if food_position[0] != 0:
            if food_position[1] != 0:
                if world[food_position[0] - 1][food_position[1] - 1] is None:
                    free.append([food_position[0] - 1, food_position[1] - 1])
            if world[food_position[0] - 1][food_position[1]] is None:
                free.append([food_position[0] - 1, food_position[1]])
            if food_position[1] != len(world[food_position[0]]) - 1:
                if world[food_position[0] - 1][food_position[1] + 1] is None:
                    free.append([food_position[0] - 1, food_position[1] + 1])

        # Check cells either side
        if food_position[1] != 0:
            if world[food_position[0]][food_position[1] - 1] is None:
                free.append([food_position[0], food_position[1] - 1])
        if food_position[1] != len(world[food_position[0]]) - 1:
            if world[food_position[0]][food_position[1] + 1] is None:
                free.append([food_position[0], food_position[1] + 1])

        # Check 3 cells below
        if food_position[0] != len(world) - 1:
            if food_position[1] != 0:
                if world[food_position[0] + 1][food_position[1] - 1] is None:
                    free.append([food_position[0] + 1, food_position[1] - 1])
            if world[food_position[0] + 1][food_position[1]] is None:
                free.append([food_position[0] + 1, food_position[1]])
            if food_position[1] != len(world[food_position[0]]) - 1:
                if world[food_position[0] + 1][food_position[1] + 1] is None:
                    free.append([food_position[0] + 1, food_position[1] + 1])

        if len(free) == 0:
            continue

        logging.debug(f'Free cells: {free}')

        new_food = free[random.randrange(len(free))]
        world[new_food[0]][new_food[1]] = create_food(food)


def prey_placement():
    prey_positions = []

    for row in range(len(world)):
        for cell in range(len(world[row])):
            cell_value = world[row][cell]
            if cell_value is not None:
                if cell_value['Type'] == prey:
                    prey_positions.append([row, cell])

    logging.debug(f'Prey positions {prey_positions}')

    for prey_position in prey_positions:

        food_position = []
        free_position = []
        predator_position = []
        mate_position = []
        overpopulation_count = 0

        # check cells above
        if prey_position[0] != 0:
            # check cell above left
            if prey_position[1] != 0:
                if world[prey_position[0] - 1][prey_position[1] - 1] is None:
                    free_position.append([prey_position[0] - 1, prey_position[1] - 1])
                elif world[prey_position[0] - 1][prey_position[1] - 1]['Type'] == food:
                    food_position.append([prey_position[0] - 1, prey_position[1] - 1])
                elif world[prey_position[0] - 1][prey_position[1] - 1]['Type'] == predator:
                    predator_position.append([prey_position[0] - 1, prey_position[1] - 1])
                elif world[prey_position[0] - 1][prey_position[1] - 1]['Type'] == prey:
                    overpopulation_count += 1
                    mate_position.append([prey_position[0] - 1, prey_position[1] - 1])

            # check cell above
            if world[prey_position[0] - 1][prey_position[1]] is None:
                free_position.append([prey_position[0] - 1, prey_position[1]])
            elif world[prey_position[0] - 1][prey_position[1]]['Type'] == food:
                food_position.append([prey_position[0] - 1, prey_position[1]])
            elif world[prey_position[0] - 1][prey_position[1]]['Type'] == predator:
                predator_position.append([prey_position[0] - 1, prey_position[1]])
            elif world[prey_position[0] - 1][prey_position[1]]['Type'] == prey:
                overpopulation_count += 1
                mate_position.append([prey_position[0] - 1, prey_position[1]])

            # check cell above right
            if prey_position[1] != len(world[prey_position[0]]) - 1:
                if world[prey_position[0] - 1][prey_position[1] + 1] is None:
                    free_position.append([prey_position[0] - 1, prey_position[1] + 1])
                elif world[prey_position[0] - 1][prey_position[1] + 1]['Type'] == food:
                    food_position.append([prey_position[0] - 1, prey_position[1] + 1])
                elif world[prey_position[0] - 1][prey_position[1] + 1]['Type'] == predator:
                    predator_position.append([prey_position[0] - 1, prey_position[1] + 1])
                elif world[prey_position[0] - 1][prey_position[1] + 1]['Type'] == prey:
                    overpopulation_count += 1
                    mate_position.append([prey_position[0] - 1, prey_position[1] + 1])


        # check cell on the left
        if prey_position[1] != 0:
            if world[prey_position[0]][prey_position[1] - 1] is None:
                free_position.append([prey_position[0], prey_position[1] - 1])
            elif world[prey_position[0]][prey_position[1] - 1]['Type'] == food:
                food_position.append([prey_position[0], prey_position[1] - 1])
            elif world[prey_position[0]][prey_position[1] - 1]['Type'] == predator:
                predator_position.append([prey_position[0], prey_position[1] - 1])
            elif world[prey_position[0]][prey_position[1] - 1]['Type'] == prey:
                overpopulation_count += 1
                mate_position.append([prey_position[0], prey_position[1] - 1])


        # check cell on the right
        if prey_position[1] != len(world[prey_position[0]]) - 1:
            if world[prey_position[0]][prey_position[1] + 1] is None:
                free_position.append([prey_position[0], prey_position[1] + 1])
            elif world[prey_position[0]][prey_position[1] + 1]['Type'] == food:
                food_position.append([prey_position[0], prey_position[1] + 1])
            elif world[prey_position[0]][prey_position[1] + 1]['Type'] == predator:
                predator_position.append([prey_position[0], prey_position[1] + 1])
            elif world[prey_position[0]][prey_position[1] + 1]['Type'] == prey:
                overpopulation_count += 1
                mate_position.append([prey_position[0], prey_position[1] + 1])


        # check cells below
        if prey_position[0] != len(world) - 1:
            # check cell below left
            if prey_position[1] != 0:
                if world[prey_position[0] + 1][prey_position[1] - 1] is None:
                    free_position.append([prey_position[0] + 1, prey_position[1] - 1])
                elif world[prey_position[0] + 1][prey_position[1] - 1]['Type'] == food:
                    food_position.append([prey_position[0] + 1, prey_position[1] - 1])
                elif world[prey_position[0] + 1][prey_position[1] - 1]['Type'] == predator:
                    predator_position.append([prey_position[0] + 1, prey_position[1] - 1])
                elif world[prey_position[0] + 1][prey_position[1] - 1]['Type'] == prey:
                    overpopulation_count += 1
                    mate_position.append([prey_position[0] + 1, prey_position[1] - 1])

            # check cell below
            if world[prey_position[0] + 1][prey_position[1]] is None:
                free_position.append([prey_position[0] + 1, prey_position[1]])
            elif world[prey_position[0] + 1][prey_position[1]]['Type'] == food:
                food_position.append([prey_position[0] + 1, prey_position[1]])
            elif world[prey_position[0] + 1][prey_position[1]]['Type'] == predator:
                predator_position.append([prey_position[0] + 1, prey_position[1]])
            elif world[prey_position[0] + 1][prey_position[1]]['Type'] == prey:
                overpopulation_count += 1
                mate_position.append([prey_position[0] + 1, prey_position[1]])

            # check cell below right
            if prey_position[1] != len(world[prey_position[0]]) - 1:
                if world[prey_position[0] + 1][prey_position[1] + 1] is None:
                    free_position.append([prey_position[0] + 1, prey_position[1] + 1])
                elif world[prey_position[0] + 1][prey_position[1] + 1]['Type'] == food:
                    food_position.append([prey_position[0] + 1, prey_position[1] + 1])
                elif world[prey_position[0] + 1][prey_position[1] + 1]['Type'] == predator:
                    predator_position.append([prey_position[0] + 1, prey_position[1] + 1])
                elif world[prey_position[0] + 1][prey_position[1] + 1]['Type'] == prey:
                    overpopulation_count += 1
                    mate_position.append([prey_position[0] + 1, prey_position[1] + 1])

        logging.debug(f'Free food positions for prey {prey_position}: {food_position}')
        logging.debug(f'Predator positions for prey {prey_position}: {predator_position}')
        logging.debug(f'Overpopulation count for prey {prey_position}: {overpopulation_count}')
        logging.debug(f'Free positions for prey {prey_position}: {free_position}')

        if overpopulation_count >= 3:
            # if there are too many prey, it dies from overpopulation
            logging.debug(f'Killing prey {prey_position} due to overpopulation')
            #world[prey_position[0]][prey_position[1]] = empty_cell
            world[prey_position[0]][prey_position[1]] = create_food(food)
        elif predator_position:
            # move in opposite direction of a random predator, can't get away from the all...
            logging.debug(f'Predators have been seen')
            escape_position = free_position
            for food_escape in food_position:
                escape_position.append(food_escape)
            logging.debug(f'Potential escape routes {escape_position}')
            for seen_predator in predator_position:
                # remove all positions around predator
                if [seen_predator[0] - 1, seen_predator[1] - 1] in escape_position:
                    escape_position.remove([seen_predator[0] - 1, seen_predator[1] - 1])
                if [seen_predator[0] - 1, seen_predator[1]] in escape_position:
                    escape_position.remove([seen_predator[0] - 1, seen_predator[1]])
                if [seen_predator[0] - 1, seen_predator[1] + 1] in escape_position:
                    escape_position.remove([seen_predator[0] - 1, seen_predator[1] + 1])
                if [seen_predator[0], seen_predator[1] - 1] in escape_position:
                    escape_position.remove([seen_predator[0], seen_predator[1] - 1])
                if [seen_predator[0], seen_predator[1]] in escape_position:
                    escape_position.remove([seen_predator[0], seen_predator[1]])
                if [seen_predator[0], seen_predator[1] + 1] in escape_position:
                    escape_position.remove([seen_predator[0], seen_predator[1] + 1])
                if [seen_predator[0] + 1, seen_predator[1] - 1] in escape_position:
                    escape_position.remove([seen_predator[0] + 1, seen_predator[1] - 1])
                if [seen_predator[0] + 1, seen_predator[1]] in escape_position:
                    escape_position.remove([seen_predator[0] + 1, seen_predator[1]])
                if [seen_predator[0] + 1, seen_predator[1] + 1] in escape_position:
                    escape_position.remove([seen_predator[0] + 1, seen_predator[1] + 1])
            logging.debug(f'Escape routes left {escape_position}')
            if escape_position:
                # go to a random escape position
                if len(prey_positions) == 1:
                    #split up, more chance of surviving
                    escape = escape_position[random.randrange(len(escape_position))]
                    logging.debug(f'Some of the prey are attempting {escape}')
                    world[escape[0]][escape[1]] = create_prey(prey)
                    world[prey_position[0]][prey_position[1]] = create_prey(prey)
                else:
                    escape = escape_position[random.randrange(len(escape_position))]
                    logging.debug(f'The prey are attempting {escape}')
                    world[escape[0]][escape[1]] = create_prey(prey)
                    world[prey_position[0]][prey_position[1]] = None
            else:
                if len(prey_positions) == 1:
                    # some make a run for it even if there is nowhere to go
                    desperate_escape_position = free_position
                    for food_escape in food_position:
                        desperate_escape_position.append(food_escape)
                    desparate_escape = desperate_escape_position[random.randrange(len(desperate_escape_position))]
                    logging.debug(f'Some of the prey are attempting {desparate_escape}')
                    world[desparate_escape[0]][desparate_escape[1]] = create_prey(prey)
                    world[prey_position[0]][prey_position[1]] = create_prey(prey)
                else:
                    logging.debug('Nowhere to go...')
                    continue

        elif food_position:
            if mate_position:
                # choose random food to eat and reproduce if someone is close
                logging.debug(f'Prey {prey_position} is eating and reproducing')
                eaten_food = food_position[random.randrange(len(food_position))]
                world[eaten_food[0]][eaten_food[1]] = create_prey(prey)
            else:
                # No one is around to reproduce, so just eat and move to food position
                logging.debug(f'Prey {prey_position} is just eating')
                eaten_food = food_position[random.randrange(len(food_position))]
                if len(prey_positions) == 1:
                    world[eaten_food[0]][eaten_food[1]] = create_prey(prey)
                    world[prey_position[0]][prey_position[1]] = create_prey(prey)
                else:
                    world[eaten_food[0]][eaten_food[1]] = create_prey(prey)
                    world[prey_position[0]][prey_position[1]] = None

        elif not food_position:
            # move to find food
            if not free_position:
                continue
            new_position = free_position[random.randrange(len(free_position))]
            # if there in only 1 prey remaining the herd splits
            if len(prey_positions) == 1:
                world[prey_position[0]][prey_position[1]] = create_prey(prey)
                world[new_position[0]][new_position[1]] = create_prey(prey)
            else:
                world[prey_position[0]][prey_position[1]] = None
                world[new_position[0]][new_position[1]] = create_prey(prey)


def predator_placement():
    predator_positions = []
    for row in range(len(world)):
        for cell in range(len(world[row])):
            cell_value = world[row][cell]
            if cell_value is not None:
                if cell_value['Type'] == predator:
                    predator_positions.append([row, cell])

    logging.debug(f'Predator positions {predator_positions}')

    for predator_position in predator_positions:

        prey_position = []
        free_position = []
        mate_position = []
        overpopulation_count = 0

        # check cells above
        if predator_position[0] != 0:
            # check cell above left
            if predator_position[1] != 0:
                if world[predator_position[0] - 1][predator_position[1] - 1] is None:
                    free_position.append([predator_position[0] - 1, predator_position[1] - 1])
                elif world[predator_position[0] - 1][predator_position[1] - 1]['Type'] == predator:
                    overpopulation_count += 1
                    mate_position.append([predator_position[0] - 1, predator_position[1] - 1])
                elif world[predator_position[0] - 1][predator_position[1] - 1]['Type'] == prey:
                    prey_position.append([predator_position[0] - 1, predator_position[1] - 1])
                elif world[predator_position[0] - 1][predator_position[1] - 1]['Type'] == food:
                    free_position.append([predator_position[0] - 1, predator_position[1] - 1])

            # check cell above
            if world[predator_position[0] - 1][predator_position[1]] is None:
                free_position.append([predator_position[0] - 1, predator_position[1]])
            elif world[predator_position[0] - 1][predator_position[1]]['Type'] == predator:
                overpopulation_count += 1
                mate_position.append([predator_position[0] - 1, predator_position[1]])
            elif world[predator_position[0] - 1][predator_position[1]]['Type'] == prey:
                prey_position.append([predator_position[0] - 1, predator_position[1]])
            elif world[predator_position[0] - 1][predator_position[1]]['Type'] == food:
                free_position.append([predator_position[0] - 1, predator_position[1]])

            # check cell above right
            if predator_position[1] != len(world[predator_position[0]]) - 1:
                if world[predator_position[0] - 1][predator_position[1] + 1] is None:
                    free_position.append([predator_position[0] - 1, predator_position[1] + 1])
                elif world[predator_position[0] - 1][predator_position[1] + 1]['Type'] == predator:
                    overpopulation_count += 1
                    mate_position.append([predator_position[0] - 1, predator_position[1] + 1])
                elif world[predator_position[0] - 1][predator_position[1] + 1]['Type'] == prey:
                    prey_position.append([predator_position[0] - 1, predator_position[1] + 1])
                elif world[predator_position[0] - 1][predator_position[1] + 1]['Type'] == food:
                    free_position.append([predator_position[0] - 1, predator_position[1] + 1])


        # check cell on the left
        if predator_position[1] != 0:
            if world[predator_position[0]][predator_position[1] - 1] is None:
                free_position.append([predator_position[0], predator_position[1] - 1])
            elif world[predator_position[0]][predator_position[1] - 1]['Type'] == predator:
                overpopulation_count += 1
                mate_position.append([predator_position[0], predator_position[1] - 1])
            elif world[predator_position[0]][predator_position[1] - 1]['Type'] == prey:
                prey_position.append([predator_position[0], predator_position[1] - 1])
            elif world[predator_position[0]][predator_position[1] - 1]['Type'] == food:
                free_position.append([predator_position[0], predator_position[1] - 1])


        # check cell on the right
        if predator_position[1] != len(world[predator_position[0]]) - 1:
            if world[predator_position[0]][predator_position[1] + 1] is None:
                free_position.append([predator_position[0], predator_position[1] + 1])
            elif world[predator_position[0]][predator_position[1] + 1]['Type'] == predator:
                overpopulation_count += 1
                mate_position.append([predator_position[0], predator_position[1] + 1])
            elif world[predator_position[0]][predator_position[1] + 1]['Type'] == prey:
                prey_position.append([predator_position[0], predator_position[1] + 1])
            elif world[predator_position[0]][predator_position[1] + 1]['Type'] == food:
                free_position.append([predator_position[0], predator_position[1] + 1])

        # check cells below
        if predator_position[0] != len(world) - 1:
            # check cell below left
            if predator_position[1] != 0:
                if world[predator_position[0] + 1][predator_position[1] - 1] is None:
                    free_position.append([predator_position[0] + 1, predator_position[1] - 1])
                elif world[predator_position[0] + 1][predator_position[1] - 1]['Type'] == predator:
                    overpopulation_count += 1
                    mate_position.append([predator_position[0] + 1, predator_position[1] - 1])
                elif world[predator_position[0] + 1][predator_position[1] - 1]['Type'] == prey:
                    prey_position.append([predator_position[0] + 1, predator_position[1] - 1])
                elif world[predator_position[0] + 1][predator_position[1] - 1]['Type'] == food:
                    free_position.append([predator_position[0] + 1, predator_position[1] - 1])

            # check cell below
            if world[predator_position[0] + 1][predator_position[1]] is None:
                free_position.append([predator_position[0] + 1, predator_position[1]])
            elif world[predator_position[0] + 1][predator_position[1]]['Type'] == predator:
                overpopulation_count += 1
                mate_position.append([predator_position[0] + 1, predator_position[1]])
            elif world[predator_position[0] + 1][predator_position[1]]['Type'] == prey:
                prey_position.append([predator_position[0] + 1, predator_position[1]])
            elif world[predator_position[0] + 1][predator_position[1]]['Type'] == food:
                free_position.append([predator_position[0] + 1, predator_position[1]])

            # check cell below right
            if predator_position[1] != len(world[predator_position[0]]) - 1:
                if world[predator_position[0] + 1][predator_position[1] + 1] is None:
                    free_position.append([predator_position[0] + 1, predator_position[1] + 1])
                elif world[predator_position[0] + 1][predator_position[1] + 1]['Type'] == predator:
                    overpopulation_count += 1
                    mate_position.append([predator_position[0] + 1, predator_position[1] + 1])
                elif world[predator_position[0] + 1][predator_position[1] + 1]['Type'] == prey:
                    prey_position.append([predator_position[0] + 1, predator_position[1] + 1])
                elif world[predator_position[0] + 1][predator_position[1] + 1]['Type'] == food:
                    free_position.append([predator_position[0] + 1, predator_position[1] + 1])


        logging.debug(f'Prey positions for predator {predator_position}: {prey_position}')
        logging.debug(f'Overpopulation count for predator {predator_position}: {overpopulation_count}')
        logging.debug(f'Free positions for predator {predator_position}: {free_position}')

        if overpopulation_count >= 3:
            # if there are too many prey, it dies from overpopulation
            logging.debug(f'Killing predator {predator_position} due to overpopulation')
            world[predator_position[0]][predator_position[1]] = create_food(food)
        elif prey_position:
            if mate_position:
                # choose random food to eat and reproduce if someone is close
                logging.debug(f'Predator {predator_position} is eating and reproducing')
                eaten_prey = prey_position[random.randrange(len(prey_position))]
                world[eaten_prey[0]][eaten_prey[1]] = create_predator(predator)
            else:
                # No one is around to reproduce, so just eat and move to food position
                logging.debug(f'Predator {predator_position} is just eating')
                if len(predator_positions) == 1:
                    eaten_prey = prey_position[random.randrange(len(prey_position))]
                    world[eaten_prey[0]][eaten_prey[1]] = create_predator(predator)
                    world[predator_position[0]][predator_position[1]] = create_predator(predator)
                else:
                    eaten_prey = prey_position[random.randrange(len(prey_position))]
                    world[eaten_prey[0]][eaten_prey[1]] = create_predator(predator)
                    world[predator_position[0]][predator_position[1]] = None
        elif not prey_position:
            # move to find food
            logging.debug(f'Nothing for {predator_position} to eat')
            hungry_predator = world[predator_position[0]][predator_position[1]]
            starvation_countdown = hungry_predator['starvation countdown'] - 1
            if starvation_countdown <= 0:
                logging.debug(f'Predator {predator_position} has starved to death')
                world[predator_position[0]][predator_position[1]] = create_food(food)
            else:
                if not free_position:
                    logging.debug(f'Predator {predator_position} has nowhere to go')
                    continue
                logging.debug(f'Predator {predator_position} is going somewhere else')
                if len(predator_positions) == 1:
                    new_position = free_position[random.randrange(len(free_position))]
                    world[predator_position[0]][predator_position[1]] = create_predator(predator, starvation_countdown)
                    world[new_position[0]][new_position[1]] = create_predator(predator, starvation_countdown)
                else:
                    new_position = free_position[random.randrange(len(free_position))]
                    world[predator_position[0]][predator_position[1]] = None
                    world[new_position[0]][new_position[1]] = create_predator(predator, starvation_countdown)


init()
count = 0

while True:
    print(f'Start of generation {count}')
    logging.info(f'Start of generation {count}')

    food_placement()
    prey_placement()
    predator_placement()

    food_count = 0
    prey_count = 0
    predator_count = 0

    for row in world:
        row_out = []
        for cell in range(len(row)):
            if row[cell] is not None:
                row_out.append(row[cell]['Type'][0])
                if row[cell]['Type'] == food:
                    food_count += 1
                elif row[cell]['Type'] == prey:
                    prey_count += 1
                elif row[cell]['Type'] == predator:
                    predator_count += 1
            else:
                row_out.append(' ')
        print(row_out)

    logging.debug(f'Count of food: {food_count}')
    logging.debug(f'Count of prey: {prey_count}')
    logging.debug(f'Count of predator: {predator_count}')

    if food_count == 0:
        print('Out of food...')
        break
    if prey_count == 0:
        print(f'All {prey} are dead')
        break
    if predator_count == 0:
        print(f'All {predator} have gone')
        break

    print(f'End of generation {count}')
    logging.info(f'End of generation {count}')
    count += 1



