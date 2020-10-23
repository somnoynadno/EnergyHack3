#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from xml.dom import minidom


# nodes collection
topology = dict()


class Node:
	def __init__(self, sde):
		tech = sde.childNodes[1]

		tag = sde.attributes.get("tag")
		stag = sde.attributes.get("sTag")
		nodes = sde.attributes.get("nodes")
		intext = sde.attributes.get("inText")

		class_name = tech.attributes.get("className")
		rtid = tech.attributes.get("RTID").value

		if not nodes:
			nodes = []
		else:
			nodes = nodes.value.split(" ")

		if not class_name:
			class_name = "NONAME"
		else:
			class_name = class_name.value

		if not intext:
			intext = ''
		else:
			intext = intext.value.replace('"', "'")

		self.rtid = rtid
		self.tag = tag
		self.stag = stag
		self.class_name = class_name
		self.nodes = nodes
		self.intext = intext

	def __str__(self):
		return "{" + 'class: "{}", RTID: {}, nodes: {}, intext: "{}"'.format(
			self.class_name, self.rtid, self.nodes, self.intext) + "}"

	def __repr__(self):
		return {'class': self.class_name, "RTID": self.rtid, "nodes": self.nodes}


def print_tree_recursively(node, i=1):
	padding = "-"*i + ">"
	print(padding, str(node))

	if node.nodes:
		for rtid in node.nodes:
			try:
				print_tree_recursively(topology[int(rtid)], i+2)
			except:
				print(padding, rtid, 'no way')


def reverse_lookup(node):
	res = []
	for v in topology.values():
		for elem in v.nodes:
			if elem == node.rtid:
				res.append(v)

	return res


def print_full_topology(root):
	print_tree_recursively(root)
	rl = reverse_lookup(root)

	for elem in rl:
		if elem.rtid != root.rtid: # prevent self loop
			print_full_topology(elem)


def parse_xml():
	global topology

	xmldoc = minidom.parse('static/distr_network.xsde')
	itemlist = xmldoc.getElementsByTagName('SDE')

	for sde in itemlist:
		n = Node(sde)
		key = int(n.rtid)

		topology[key] = n


def main():
	# choosing some node just for debug
	n = topology[4]
	print_full_topology(n)


###############################
#                             #
#  Main loop goes down below  #
#                             #
###############################


parse_xml()

if __name__ == "__main__":
	main()
