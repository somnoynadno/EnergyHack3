import json

from neo4j import GraphDatabase

# user imports
from parser import topology


URI = "neo4j://somnoynadno.ru:7687"
CREDS = ("neo4j", "password")
VERBOSE = True


def create_node(tx, node):
	tx.run("CREATE (n{}:{} {})".format(node.rtid, node.class_name, str(node)))


def create_link(tx, node1, node2):
	tx.run('MATCH (n{0}:{1}), (n{2}:{3}) WHERE n{0}.RTID = {0} AND n{2}.RTID = {2} CREATE (n{0})-[r:CONNECTED_TO]->(n{2})'.format(
		node1.rtid, node1.class_name, node2.rtid, node2.class_name))


def main():
	driver = GraphDatabase.driver(URI, auth=CREDS, encrypted=False)


	# CREATE NODES
	with driver.session() as session:
		i = 0
		for rtid, node in topology.items():
			session.write_transaction(create_node, node)

			if VERBOSE:
				print("{}: OK".format(i))
			i += 1


	# CONNECT NODES
	with driver.session() as session:
		for rtid, node in topology.items():
			for n in node.nodes:
				try:
					child_node = topology[int(n)]
					session.write_transaction(create_link, node, child_node)

					if VERBOSE:
						print("{}:{}: OK".format(node.rtid, child_node.rtid))
				except KeyError:
					if VERBOSE:
						print("no entry for", n)


	driver.close()


if __name__ == "__main__":
	# 4422 nodes ~ 11 minutes
	main()
