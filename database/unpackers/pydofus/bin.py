#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ._binarystream import _BinaryStream


class BinReader:

    def __init__(self, stream):
        self._stream = stream
        D2O_file_binary = _BinaryStream(self._stream, True)
        self._bin_file_binary = D2O_file_binary
        self._total = self._bin_file_binary.read_int32()
        self._counter = 0
        self._vertices = dict()
        self._edges = dict()
        self._outgoing_edges = dict()
        self._vertex_uid = 0

        while self._counter < self._total:
            vertex_from = self.add_vertex(self._bin_file_binary.read_double(), self._bin_file_binary.read_int32())
            vertex_to = self.add_vertex(self._bin_file_binary.read_double(), self._bin_file_binary.read_int32())
            edge = self.add_edge(vertex_from, vertex_to)
            xxx = self._bin_file_binary.read_int32()
            count = 0
            while count < xxx:
                _type = int.from_bytes(self._bin_file_binary.read_byte(), 'little')
                direction = int.from_bytes(self._bin_file_binary.read_byte(), 'little')
                skill_id = self._bin_file_binary.read_int32()
                lenght = self._bin_file_binary.read_int32()
                criterion = self._bin_file_binary.read_bytes(lenght).decode('UTF-8')
                transition_map_id = self._bin_file_binary.read_double()
                cell = self._bin_file_binary.read_int32()
                id = self._bin_file_binary.read_double()
                edge['transition'].append({
                    'type': _type,
                    'direction': direction,
                    'skill_id': skill_id,
                    'criterion': criterion,
                    'transition_map_id': transition_map_id,
                    'cell': cell,
                    'id': id
                })
                count += 1
            self._counter += 1

    def add_edge(self, vertex_from, vertex_to):
        edge = self.get_edge(vertex_from, vertex_to)
        from_uid = vertex_from.get('u_id')
        if edge:
            return edge
        if not self.does_vertex_exist(vertex_from) or not self.does_vertex_exist(vertex_to):
            return None
        edge = {'from': vertex_from, 'to': vertex_to, 'transition': list()}
        if not self._edges.get(from_uid):
            self._edges[from_uid] = dict()
        self._edges[from_uid][vertex_to.get('u_id')] = edge
        outgoing_edge = self._outgoing_edges.get(from_uid)
        if not outgoing_edge:
            self._outgoing_edges[from_uid] = list()
        self._outgoing_edges[from_uid].append(edge)
        return edge

    def get_edge(self, vertex_from, vertex_to):
        if self._edges.get(vertex_from.get('u_id')):
            return self._edges.get(vertex_from.get('u_id')).get(vertex_to.get('u_id'))
        return None

    def does_vertex_exist(self, vertex: dict):
        return self._vertices[vertex.get('map_id')][vertex.get('zone_id')] != None

    def add_vertex(self, map_id: int, zone_id: int):
        if not self._vertices.get(map_id):
            self._vertices[map_id] = dict()
        vertice = self._vertices[map_id].get(zone_id)
        if not vertice:
            self._vertex_uid += 1
            vertex = dict({'map_id': map_id, 'zone_id': zone_id, 'u_id': self._vertex_uid})
            self._vertices[map_id][zone_id] = vertex
        return self._vertices[map_id][zone_id]

    def get_data(self):
        return {'vertices': self._vertices, 'edges': self._edges, 'outgoing_edges': self._outgoing_edges}
