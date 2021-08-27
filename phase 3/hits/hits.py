import json
import typing


class Node:
    def __init__(self, name):
        self.name = name
        self.out_links = set()
        self.back_links = set()
        self.hub = 1.0
        self.authority = 1.0

    def update_authority(self, graph):
        self.authority = sum(graph[node].hub for node in self.back_links)

    def update_hub(self, graph):
        self.hub = sum(graph[node].authority for node in self.out_links)


class HITS:
    def __init__(self, data_file_path: str, top_authors_count: int):
        self.top_authors_count = top_authors_count
        self.graph: typing.Dict[str, Node] = self._construct_graph(data_file_path)
        self.max_iteration_count = 5

    @staticmethod
    def _add_author_if_not_in_graph(graph, author_name):
        if author_name not in graph:
            graph[author_name] = Node(author_name)

    def _construct_graph(self, data_file_path):
        with open(data_file_path, 'r') as f:
            papers = {paper['id']: paper for paper in json.load(f)}
        graph: typing.Dict[str, Node] = {}
        for paper in papers.values():
            authors = paper['authors']
            references = paper['references']
            for author in authors:
                self._add_author_if_not_in_graph(graph, author)
                for reference in references:
                    if reference not in papers:
                        continue
                    reference_authors = papers[reference]['authors']
                    graph[author].out_links.update(reference_authors)
                    for reference_author in reference_authors:
                        self._add_author_if_not_in_graph(graph, reference_author)
                        graph[reference_author].back_links.add(author)
        return graph

    def calculate_hits(self):
        for _ in range(self.max_iteration_count):
            for node in self.graph.values():
                node.update_authority(self.graph)
            for node in self.graph.values():
                node.update_hub(self.graph)
            authority_sum = sum(node.authority for node in self.graph.values())
            hub_sum = sum(node.hub for node in self.graph.values())

            for node in self.graph.values():
                node.authority /= authority_sum
                node.hub /= hub_sum
        nodes = list(self.graph.values())
        nodes.sort(key=lambda node: node.authority, reverse=True)
        return [(node.name, node.authority) for node in nodes[:self.top_authors_count]]
