# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))
from database.sqlite import Database
import numpy as np
import copy

from src.goals.goal import Goal
from src.scheduler.actions.move_action import MoveAction
from src.scheduler.actions.harvest_action import HarvestAction
from src.scheduler.actions.action_interface import ActionInterface


class Resource(Goal):

    def __init__(self, database: Database, resources: list, account_number: int):
        self.database = database
        self.option = None
        self.account_number = account_number
        self.resources = self.resource_resolver(resources)
        print(self.resources)
        self.resources_location = None
        self.level = 200
        self.distance = 2 # max distances between groups
        self.best_groups = None
        self.character_routine = dict()
        self.routine = []
        self.set_positions_to_go()
        self.routine_type_by_id = dict()
        self.scheduler_characters_routine()

    def resource_resolver(self, resources: list):
        resource_list = list()
        for resource in resources:
            result = self.database.get_resource_by_name_or_id(resource.get('value'))
            for item in result:
                resource_list.append({
                    'id': item[0],
                    'level': item[2],
                    'name': item[1]
                })
        return resource_list

    def search_resource(self, resource):
        data = self.database.get_resource_by_name_or_id(resource)
        if data:
            return {
                'id': data[0][0],
                'name': data[0][1],
                'level': data[0][2],

            }
        return None

    def add_resources_to_collect(self, resouces: list):
        os.system('cls' if os.name == 'nt' else 'clear')
        names = list()
        for resource in resouces:
            names.append(resource.get('name'))
        names = ', '.join(names)
        print(f'SELECTED items: ({names})')
        print('Digit the name or id of the resource: ')
        resource = input()
        if resource == '':
            return resouces
        result = self.search_resource(resource)
        if result:
            resouces.append(result)
            self.add_resources_to_collect(resouces)

    def get_resources_location(self):
        resources_ids = list()
        for resource in self.resources:
            if resource['level'] <= self.level:
                resources_ids.append(str(resource['id']))
        positions = self.database.get_resources_location(resources_ids)
        return positions, [int(id) for id in resources_ids]

    def get_grouped_location(self, positions: list):
        groups = list()
        while True:
            pivo = positions.pop()
            group = list()
            group.append(pivo)
            group, positions = self.get_neighborhood(pivo, positions, group, 0)
            groups.append(group)
            if len(positions) == 0:
                break
        return groups

    def get_neighborhood(self, pivo: tuple, positions: list, group: list, level: int = 0):
        boundary = self.database.get_boundary((pivo[1], pivo[2], 1))
        # if (pivo[1] == -12 and pivo[2] == 2) or (pivo[1] == -11 and pivo[2] == 2):
        #     print(boundary)
        #     print(group)

        if len(boundary) > 0:
            has_t = boundary[0][2] == 1
            has_q = boundary[0][3] == 1
            has_x = boundary[0][4] == 1
            has_b = boundary[0][5] == 1
        else:
            has_t = True
            has_q = True
            has_x = True
            has_b = True
        # if (pivo[1] == -12 and pivo[2] == 2) or (pivo[1] == -11 and pivo[2] == 2):
        #     print(
        #         has_t,
        #         has_q,
        #         has_x,
        #         has_b
        #     )
        #     input()
        if has_t:
            nb_pivo_t = (-1, pivo[1], pivo[2]+1)
            position_t, positions = self.filter_positions(nb_pivo_t, positions)
        if has_q:
            nb_pivo_q = (-1, pivo[1]-1, pivo[2])
            position_q, positions = self.filter_positions(nb_pivo_q, positions)
        if has_x:
            nb_pivo_x = (-1, pivo[1], pivo[2]-1)
            position_x, positions = self.filter_positions(nb_pivo_x, positions)
        if has_b:
            nb_pivo_b = (-1, pivo[1]+1, pivo[2])
            position_b, positions = self.filter_positions(nb_pivo_b, positions)

        if has_t:
            if position_t:
                group = self.add_in_group(group, position_t)
                group, positions = self.get_neighborhood(position_t[0], positions, group)
            elif level < self.distance and position_t is None:
                level_t = copy.deepcopy(level) + 1
                group, positions = self.get_neighborhood(nb_pivo_t, positions, group, level_t)
        if has_q:
            if position_q:
                group = self.add_in_group(group, position_q)
                group, positions = self.get_neighborhood(position_q[0], positions, group)
            elif level < self.distance and position_q is None:
                level_q = copy.deepcopy(level) + 1
                group, positions = self.get_neighborhood(nb_pivo_q, positions, group, level_q)
        if has_x:
            if position_x:
                group = self.add_in_group(group, position_x)
                group, positions = self.get_neighborhood(position_x[0], positions, group)
            elif level < self.distance and position_x is None:
                level_x = copy.deepcopy(level) + 1
                group, positions = self.get_neighborhood(nb_pivo_x, positions, group, level_x)
        if has_b:
            if position_b:
                group = self.add_in_group(group, position_b)
                group, positions = self.get_neighborhood(position_b[0], positions, group)
            elif level < self.distance and position_b is None:
                level_b = copy.deepcopy(level) + 1
                group, positions = self.get_neighborhood(nb_pivo_b, positions, group, level_b)
        return group, positions

    def add_in_group(self, group: list, items: list):
        new_goup = copy.deepcopy(group)
        for item in items:
            new_goup.append(item)
        return new_goup

    def filter_positions(self, position_to_search: tuple, positions: list):
        results = [ position for position in positions if position[1] == position_to_search[1] and position[2] == position_to_search[2] ]
        for result in results:
            positions.pop(positions.index(result))
        if len(results) > 0:
            return results, positions
        return None, positions

    def get_groups_quantities(self, groups: list) -> list:
        groups_info = []
        self.cells_in_groups = []
        for group in groups:
            group_info = dict()
            distint_cells_list = []
            for item in group:
                if item[3] not in group_info:
                    group_info[item[3]] = item[4]
                else:
                    group_info[item[3]] += item[4]
                if (item[1],item[2]) not in distint_cells_list:
                    distint_cells_list.append((item[1],item[2]))
            self.cells_in_groups.append(distint_cells_list)
            group_info['density'] = sum(group_info.values())/len(distint_cells_list)
            groups_info.append(group_info)
        group_index = 0
        comparation_list = list()
        for group_quantitie in groups_info:
            comparation_list.append([group_index, group_quantitie , 0])
            group_index += 1
        return comparation_list

    def check_ids_in_groups(self, resources_ids: list, comparation_list: list, groups_index: list):
        ids_not_in_group = []
        for id in resources_ids:
            if id not in comparation_list[0][1]:
                ids_not_in_group.append(id)
        groups_index[comparation_list[0][0]] = list(set(resources_ids) - set(ids_not_in_group))
        del comparation_list[0]
        if len(ids_not_in_group) != 0:
            for group in comparation_list:
                group[2] = 0
            ids_not_in_group.append('density')
            self.chose_best_groups(
                resources_ids=ids_not_in_group,
                comparation_list=comparation_list,
                groups_index=groups_index
            )

    def chose_best_groups(self, comparation_list: list, resources_ids: list, groups_index: dict = dict()) -> dict: # checar se todos recursos estao no geupo[0]
        #Rerotna o numero de personagens para cada grupo.
        #separar recursivamente os grupos pra cada personagem, tira o atribuido e roda dnv pro proximo
        comparation_list = comparation_list
        groups_index = groups_index
        for id in resources_ids:
            itens_to_sort = [group for group in comparation_list if id in group[1]]
            itens_to_sort.sort(key=lambda x: x[1][id])
            score = abs(len(itens_to_sort) - len(comparation_list))
            for item in itens_to_sort:
                comparation_list[comparation_list.index(item)][2] += score
                score += 1
        comparation_list.sort(key=lambda x: x[2])
        comparation_list = comparation_list[::-1]
        self.check_ids_in_groups(
            resources_ids=resources_ids,
            comparation_list=comparation_list,
            groups_index=groups_index
        )
        for index in groups_index:
            if 'density' in groups_index[index]:
                groups_index[index].remove('density')
        return groups_index

    def set_positions_to_go(self):
        positions, resources_ids = self.get_resources_location()
        groups = self.get_grouped_location(positions)
        resources_ids.append('density')
        groups_index = self.chose_best_groups(
            comparation_list=self.get_groups_quantities(groups),
            resources_ids=resources_ids
        )
        itens_to_search = {}
        resources_ids = list()
        for key in groups_index:
            resources_ids = list(set(resources_ids) | set(groups_index[key]))
            itens_to_search[str(groups_index[key])] = self.cells_in_groups[key]
        self.best_groups = itens_to_search
        self.resources_ids = resources_ids

    def scheduler_characters_routine(self):
        self.account_number
        best_groups_quantity = len(self.best_groups)
        for i in range(0, self.account_number):
            self.character_routine[i] = i
        if self.account_number == best_groups_quantity:
            for key in self.best_groups:
                self.routine.append(self.best_groups.get(key))
        else:
            all_position = list()
            for key in self.best_groups:
                all_position += self.best_groups.get(key)
            chunk_size = int(len(all_position)/self.account_number)
            for i in range(0, self.account_number):
                if i+1 == self.account_number:
                    self.routine.append(all_position[chunk_size*i:])
                    continue
                self.routine.append(all_position[chunk_size*i:chunk_size])
        #print(self.routine)

    def get_next_step(self, character_name: str) -> ActionInterface:
        character_routine_id = self.get_character_routine_id(character_name=character_name)
        action = self.get_next_routine_by_id(routine_id=character_routine_id)
        #print(action)
        return action

    def get_next_routine_by_id(self, routine_id: int) -> ActionInterface:
        if self.routine_type_by_id[routine_id] == 'MOVE':
            routine = self.routine[routine_id]
            to_return = routine.pop(0)
            routine.append(to_return)
            self.routine[routine_id] = routine
            self.routine_type_by_id[routine_id] = 'HARVEST'
            return MoveAction(x=to_return[0], y=to_return[1])
        else:
            self.routine_type_by_id[routine_id] = 'MOVE'
            return HarvestAction(items=self.resources)

    def get_character_routine_id(self, character_name: str) -> int:
        if self.character_routine.get(character_name) is None:
            key_to_update = None
            for key, value in self.character_routine.items():
                if key == value:
                    key_to_update = key
                    break
            self.character_routine.pop(key_to_update)
            self.character_routine[character_name] = key_to_update
            self.routine_type_by_id[key_to_update] = 'MOVE'
        return self.character_routine.get(character_name)


if __name__ == '__main__':
    database = Database()
    resource = Resource(database)