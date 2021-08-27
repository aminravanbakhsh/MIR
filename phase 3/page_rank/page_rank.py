import json
import os
import typing
from copy import deepcopy


class Node:
    def __init__(self):
        self.out_links = []
        self.back_links = []


class PageRank:
    def __init__(self, data_file_path: str, damping_factor: float):
        self.d = damping_factor
        self.ranks = {}
        self.graph: typing.Dict[str, Node] = self._construct_graph(data_file_path)
        self.node_count = len(self.graph)
        self.max_iteration_count = 10

    @staticmethod
    def _add_paper_if_not_in_graph(graph, paper_id):
        if paper_id not in graph:
            graph[paper_id] = Node()

    def _construct_graph(self, data_file_path):
        with open(data_file_path, 'r') as f:
            papers = json.load(f)
        graph = {}
        for paper in papers:
            paper_id = paper['id']

            self._add_paper_if_not_in_graph(graph, paper_id)
            graph[paper_id].out_links = deepcopy(paper['references'])

            for reference in paper['references']:
                self._add_paper_if_not_in_graph(graph, reference)
                graph[reference].back_links.append(paper_id)
        return graph

    def calculate_page_rank(self):
        for paper_id in self.graph:
            self.ranks[paper_id] = 1 / float(self.node_count)
        for _ in range(self.max_iteration_count):
            for paper_id in self.graph:
                rank_sum = 0
                neighbors = self.graph[paper_id].back_links
                for neighbor in neighbors:
                    out_link_count = len(self.graph[neighbor].out_links)
                    if out_link_count > 0:
                        rank_sum += self.ranks[neighbor] / float(out_link_count)

                self.ranks[paper_id] = (1 - self.d) / float(self.node_count) + self.d * rank_sum

        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_dir, 'PageRank.json'), 'w') as f:
            json.dump(self.ranks, f)
