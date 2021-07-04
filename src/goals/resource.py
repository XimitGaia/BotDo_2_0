# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))
from database.sqlite import Database
import numpy as np
import copy
import math

from src.goals.goal import Goal
from src.scheduler.actions.move_action import MoveAction
from src.scheduler.actions.harvest_action import HarvestAction
from src.scheduler.actions.action_interface import ActionInterface

class Resource(Goal):

    def __init__(self, database: Database, resources: list, account_number: int):
        self.database = database
        self.account_number = account_number
        self.resources = resources
        #self.get_resources_map_dict()
        self.number_of_resources = len(self.resources)
        self.distance = 2
        self.index = 0
        self.cluster_list = list()

    def get_next_step(self, character_name: str) -> ActionInterface:
        pass

    #  ::::::::  :::       :::    :::  :::::::: ::::::::::: :::::::::: :::::::::   ::::::::
    # :+:    :+: :+:       :+:    :+: :+:    :+:    :+:     :+:        :+:    :+: :+:    :+:
    # +:+        +:+       +:+    +:+ +:+           +:+     +:+        +:+    +:+ +:+
    # +#+        +#+       +#+    +:+ +#++:++#++    +#+     +#++:++#   +#++:++#:  +#++:++#++
    # +#+        +#+       +#+    +#+        +#+    +#+     +#+        +#+    +#+        +#+
    # #+#    #+# #+#       #+#    #+# #+#    #+#    #+#     #+#        #+#    #+# #+#    #+#
    #  ########  ########## ########   ########     ###     ########## ###    ###  ########

    def get_world_maps_by_harvestables(self):
        connections = self.database.get_world_map_with_harvestable_indication(self.resources)
        world_map_dict = dict()
        harvestables_map = list()
        for connection in connections:
            if world_map_dict.get(connection[0]) is None:
                world_map_dict[connection[0]] = {
                    'destinies': [connection[1]],
                    'harvestable_quantity': dict()
                }
                if connection[3] is not None:
                    world_map_dict[connection[0]]['harvestable_quantity'].update({connection[3]: connection[2]})
                if connection[2] != 0:
                    harvestables_map.append(connection[0])
                continue
            if connection[1] not in world_map_dict[connection[0]]['destinies']:
                world_map_dict[connection[0]]['destinies'].append(connection[1])
            if connection[3] is not None and connection[3] not in world_map_dict[connection[0]]['harvestable_quantity']:
                world_map_dict[connection[0]]['harvestable_quantity'][connection[3]] = connection[2]
        return world_map_dict, harvestables_map

    def clusterise(self, world_map_dict: dict, harvestables_map: list, map_id: int, current_distance: int = -1):
        if map_id in harvestables_map:
            harvestables_map.remove(map_id)
        map_metadata = world_map_dict.get(map_id)
        if map_metadata is None:
            return
        del world_map_dict[map_id]
        harvestable_quantity_metadata = map_metadata.get('harvestable_quantity')
        total = 0
        for harvestable_quantity in harvestable_quantity_metadata:
            if harvestable_quantity not in self.cluster_list[self.index]['quantities']:
                self.cluster_list[self.index]['quantities'][harvestable_quantity] = 0
            self.cluster_list[self.index]['quantities'][harvestable_quantity] += harvestable_quantity_metadata.get(harvestable_quantity)
            self.cluster_list[self.index]['quantities']['total'] += harvestable_quantity_metadata.get(harvestable_quantity)
            total += harvestable_quantity_metadata.get(harvestable_quantity)
        if total == 0:
            current_distance += 1
            if current_distance == self.distance:
                return
        else:
            self.cluster_list[self.index]['maps_id'].append(map_id)
        for destiny_map_id in map_metadata.get('destinies'):
            self.clusterise(
                world_map_dict=world_map_dict,
                harvestables_map=harvestables_map,
                map_id=destiny_map_id,
                current_distance=current_distance
            )

    def get_clusters(self):
        world_map_dict, harvestables_map = self.get_world_maps_by_harvestables()
        while len(harvestables_map) > 0:
            self.cluster_list.append({'quantities': {'total': 0}, 'maps_id': list(), 'score': 0})
            map_id = harvestables_map.pop()
            self.clusterise(
                world_map_dict=world_map_dict,
                harvestables_map=harvestables_map,
                map_id=map_id,
            )
            self.index += 1

    def assing_score(self, criterion: callable, weight=1):
        score = len(self.cluster_list) + 1
        last_criterion_value = None
        for cluster in self.cluster_list:
            actual_criterion_value = criterion(cluster)
            if actual_criterion_value != last_criterion_value:
                score -= 1
            cluster['score'] += weight*score
            last_criterion_value = actual_criterion_value

    def gaussian(self, cluster):
        quantities = cluster['quantities']
        middle = 1/self.number_of_resources #(len(quantities) - 1)
        exponent = sum([(quantities[i]/quantities['total'] - middle)**2 for i in quantities if i != 'total'])
        return math.exp(-exponent)

    def get_cluster_total_resources(self, cluster):
        return cluster['quantities']['total']

    def get_cluster_density(self, cluster):
        return cluster['quantities']['total']/len(cluster['maps_id'])

    def rank_clusters(self):
        # quantity
        self.cluster_list = sorted(self.cluster_list, key=lambda u: self.get_cluster_total_resources(u), reverse=True)
        self.assing_score(criterion=self.get_cluster_total_resources, weight=2)
        # density
        self.cluster_list = sorted(self.cluster_list, key=lambda u: self.get_cluster_density(u), reverse=True)
        self.assing_score(criterion=self.get_cluster_density)
        # gaussian
        self.cluster_list = sorted(self.cluster_list, key=lambda u: self.gaussian(u), reverse=True)
        self.assing_score(criterion=self.gaussian, weight=2)
        # sorting
        self.cluster_list = sorted(self.cluster_list, key=lambda u: u['score'], reverse=True)


if __name__ == '__main__':
    database = Database()
    # resource = Resource(database=database, resources=[47, 46, 19], account_number=1)
    resource = Resource(database=database, resources=[1,2,19], account_number=1)
    resource.get_clusters()
    resource.rank_clusters()
    print(resource.cluster_list)