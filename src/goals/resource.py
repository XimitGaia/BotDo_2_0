# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))
from database.sqlite import Database
import numpy as np
import copy




class Resource:

    def __init__(self, database: Database):
        self.database = database
        self.option = None
        self.resources = self.resource_menu()
        self.resources_location = None
        self.level = 200
        self.distance = 2 # max distances between groups
        print(self.run())


    def resource_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('SELECT ONE OF THE OPTIONS')
        print('1 - Up job')
        print('2 - get resources')
        option = int(input("Select what you want: "))
        if option == 1:
            self.option = 1
            os.system('cls' if os.name == 'nt' else 'clear')
            jobs = self.database.get_jobs()
            for job in jobs:
                print(f'{job[0]} - {job[1]}')
            print('SELECT ONE OF THE OPTIONS')
            id = int(input("Select what you want: "))
            result = self.database.get_resources_by_job_id(id)
            resource_list = list()
            for item in result:
                resource_list.append({
                    'id': item[0],
                    'level': item[2],
                    'name': item[1]
                })
        if option == 2:
            self.option = 2
            resource_list = list()
            self.add_resources_to_collect(resource_list)
        print(resource_list)
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
        barrer = self.database.get_barrer(pivo[1], pivo[2])
        # if (pivo[1] == -12 and pivo[2] == 2) or (pivo[1] == -11 and pivo[2] == 2):
        #     print(barrer)
        #     print(group)

        if len(barrer) > 0:
            has_t = barrer[0][2] == 1
            has_q = barrer[0][3] == 1
            has_x = barrer[0][4] == 1
            has_b = barrer[0][5] == 1
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


    def get_groups_quantities(self, groups: list)-> list:
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


    def check_ids_in_groups(self, resources_ids:list, comparation_list:list ,groups_index: list):
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


    def chose_best_groups(self,comparation_list:list, resources_ids:list, groups_index:dict = dict())->dict:# checar se todos recursos estao no geupo[0]
        comparation_list = comparation_list
        groups_index = groups_index
        for id in resources_ids:
            itens_to_sort = [group for group in comparation_list if id in group[1]]
            itens_to_sort.sort(key = lambda x: x[1][id])
            score = abs(len(itens_to_sort) - len(comparation_list))
            for item in itens_to_sort:
                comparation_list[comparation_list.index(item)][2] += score
                score += 1
        comparation_list.sort(key=lambda x: x[2])
        comparation_list = comparation_list[::-1]
        #print(comparation_list)
        self.check_ids_in_groups(
        resources_ids=resources_ids,
        comparation_list=comparation_list,
        groups_index=groups_index
        )
        for index in groups_index:
            if 'density' in groups_index[index]:
                groups_index[index].remove('density')
        return groups_index
            

    def run(self):
        positions, resources_ids = self.get_resources_location()
        groups = self.get_grouped_location(positions)
        resources_ids.append('density')
        groups_index = self.chose_best_groups(
            comparation_list=self.get_groups_quantities(groups),
            resources_ids=resources_ids
        )
        # print(groups_index)
        itens_to_search = {}
        for key in groups_index:
            itens_to_search[str(groups_index[key])] = self.cells_in_groups[key]
        return itens_to_search

if __name__ == '__main__':
    database = Database()
    resource = Resource(database)