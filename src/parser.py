#!/usr/bin/env python3

import sys

from xml.dom import minidom


# source file
FILE_PATH = 'static/distr_network.xsde'

# nodes collection
topology = dict()


class Node:
	def __init__(self, sde):
		tech = sde.childNodes[1]

		tag = sde.attributes.get("tag")
		stag = sde.attributes.get("sTag")
		nodes = sde.attributes.get("nodes")

		rtid = tech.attributes.get("RTID").value
		class_name = tech.attributes.get("className").value
		voltage = tech.attributes.get("voltage")
		name = tech.attributes.get("DispName")

		# handle Breakers state
		closed = None
		if class_name in ["Breaker", "GroundDisconnector", "Disconnector"]:
			closed = 1
			try:
				closed = int(tech.attributes.get("closed").value)
			except:
				pass

		# handle SubstationTP capacity
		capacity = 0
		for elem in sde.childNodes:
			if elem.nodeName == "ParamText":
				c = elem.attributes.get("subscriptName")
				if c:
					try:
						capacity = int(c.value)
					except:
						pass

		# connected nodes list
		if not nodes:
			nodes = []
		else:
			nodes = nodes.value.split(" ")

		# voltage of node
		if not voltage:
			voltage = ''
		else:
			voltage = voltage.value

		# displayed name
		if not name:
			name = ''
		else:
			name = name.value.replace('"', "'")

		self.rtid = rtid
		self.tag = tag
		self.stag = stag
		self.class_name = class_name
		self.nodes = nodes
		self.voltage = voltage
		self.name = name
		self.capacity = capacity
		self.closed = closed

	def __str__(self):
		if self.closed is not None:
			return "{" + 'class: "{}", RTID: {}, nodes: {}, voltage: "{}", name: "{}", capacity: {}, closed: {}'.format(
					self.class_name, self.rtid, self.nodes, self.voltage, self.name, self.capacity, self.closed) + "}"
		else:
			return "{" + 'class: "{}", RTID: {}, nodes: {}, voltage: "{}", name: "{}", capacity: {}'.format(
					self.class_name, self.rtid, self.nodes, self.voltage, self.name, self.capacity) + "}"

	def __repr__(self):
		return {"class": self.class_name, "RTID": self.rtid, "closed": self.closed,
				"voltage": self.voltage, "nodes": self.nodes, "capacity": self.capacity}


# pretty print all childs of selected node
def print_tree_recursively(node, i=1):
	padding = "-"*i + ">"
	print(padding, str(node))

	if node.nodes:
		for rtid in node.nodes:
			try:
				print_tree_recursively(topology[int(rtid)], i+2)
			except:
				print(padding, rtid, 'no way')


# get list of parents os selected node
def reverse_lookup(node):
	res = []
	for v in topology.values():
		for elem in v.nodes:
			if elem == node.rtid:
				res.append(v)

	return res


# reverse lookup + print tree
def print_full_topology(root):
	print_tree_recursively(root)
	rl = reverse_lookup(root)

	for elem in rl:
		if elem.rtid != root.rtid: # prevent self loop
			print_full_topology(elem)


# building topology
def parse_xml():
	global topology

	xmldoc = minidom.parse(FILE_PATH)
	itemlist = xmldoc.getElementsByTagName('SDE')

	for sde in itemlist:
		tech = sde.childNodes[1]
		if tech.attributes.get("className"): # drop nodes without name
			n = Node(sde)
			key = int(n.rtid)

			topology[key] = n


def main():
	if len(sys.argv) <= 1:
		print("You need to specify root node RTID")
		exit(1)
	else:
		root = int(sys.argv[1])
		n = topology[root]
		print_full_topology(n)


###############################
#                             #
#  Main loop goes down below  #
#                             #
###############################


parse_xml()

if __name__ == "__main__":
	main()
