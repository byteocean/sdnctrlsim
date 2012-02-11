#!/usr/bin/env python
#
# Dan Levin <dlevin@net.t-labs.tu-berlin.de>
# Brandon Heller <brandonh@stanford.edu>

import networkx as nx
import os
import unittest
import sys
import unittest

sys.path.append(os.path.dirname(__file__) + "/..")

from sim.controller import *

###############################################################################
# Test helper functions
###############################################################################

def one_switch_topo():
    graph = nx.DiGraph()
    graph.add_nodes_from(['sw1'], type='switch')
    graph.add_nodes_from(['s1', 's2'], type='server')
    graph.add_edges_from([['s1', 'sw1', {'capacity':100, 'used':0.0}],
                          ['s2', 'sw1', {'capacity':100, 'used':0.0}]])
    return graph

def two_switch_topo():
    graph = nx.DiGraph()
    graph.add_nodes_from(['sw1', 'sw2'], type='switch')
    graph.add_nodes_from(['s1', 's2'], type='server')
    graph.add_edges_from([['s1', 'sw1', {'capacity':100, 'used':0.0}],
                          ['sw1', 'sw2', {'capacity':1001, 'used':0.0}],
                          ['sw2', 'sw1', {'capacity':1001, 'used':0.0}],
                          ['s2', 'sw2', {'capacity':100, 'used':0.0}]])
    return graph

def two_switch_narrow_topo():
    graph = nx.DiGraph()
    graph.add_nodes_from(['sw1', 'sw2'], type='switch')
    graph.add_nodes_from(['s1', 's2'], type='server')
    graph.add_edges_from([['s1', 'sw1', {'capacity':101, 'used':0.0}],
                          ['sw1', 'sw2', {'capacity':10, 'used':0.0}],
                          ['sw2', 'sw1', {'capacity':10, 'used':0.0}],
                          ['s2', 'sw2', {'capacity':101, 'used':0.0}]])
    return graph

# Anja's topology suggestion to test for non-triviality of 'SW2'
# decision on whom to send requests when not served by s2
def three_switch_topo():
    graph = nx.DiGraph()
    graph.add_nodes_from(['sw1', 'sw2', 'sw3'], type='switch')
    graph.add_nodes_from(['s1', 's2', 's3'], type='server')
    graph.add_edges_from([['s1', 'sw1', {'capacity':100, 'used':0.0}],
                          ['sw1', 'sw2', {'capacity':50, 'used':0.0}],
                          ['sw2', 'sw1', {'capacity':50, 'used':0.0}],
                          ['sw2', 'sw3', {'capacity':50, 'used':0.0}],
                          ['sw3', 'sw2', {'capacity':50, 'used':0.0}],
                          ['s2', 'sw2', {'capacity':100, 'used':0.0}],
                          ['s3', 'sw3', {'capacity':100, 'used':0.0}]])
    return graph


# Dan put this here to demonstrate corner cases of simulation logic
def greedy_topo():
    graph = nx.DiGraph()
    graph.add_nodes_from(['sw1', 'sw2', 'sw3', 'sw4'], type='switch')
    graph.add_nodes_from(['s1a', 's1b', 's3', 's4'], type='server')
    graph.add_edges_from([['s1a', 'sw1', {'capacity':100, 'used':0.0}],
                          ['s1b', 'sw1', {'capacity':100, 'used':0.0}],
                          ['sw1', 'sw2', {'capacity':50, 'used':0.0}],
                          ['sw2', 'sw1', {'capacity':50, 'used':0.0}],
                          ['sw2', 'sw3', {'capacity':50, 'used':0.0}],
                          ['sw3', 'sw2', {'capacity':50, 'used':0.0}],
                          ['sw3', 'sw4', {'capacity':50, 'used':0.0}],
                          ['sw4', 'sw3', {'capacity':50, 'used':0.0}],
                          ['s3', 'sw3', {'capacity':100, 'used':0.0}],
                          ['s4', 'sw4', {'capacity':100, 'used':0.0}]])
    return graph

def two_ctrls(greedy=False, greedylimit=1):
    """Return list of two different controllers."""
    ctrls = []
    c1 = LinkBalancerCtrl(sw=['sw1'], srv=['s1', 's2'], greedy=greedy, greedylimit=greedylimit)
    c2 = LinkBalancerCtrl(sw=['sw2'], srv=['s1', 's2'], greedy=greedy, greedylimit=greedylimit)
    ctrls.append(c1)
    ctrls.append(c2)
    return ctrls

def strictly_local_ctrls(n=2):
    """ Create a number of controllers that strictly only send traffic to one local server they know about """
    return [ LinkBalancerCtrl(sw=["sw%d"%i], srv=["s%d"%i], greedy=True, greedylimit=1000) for i in range(1, 1+ n) ]

def three_ctrls(greedy=False, greedylimit=1):
    """Return list of three different controllers."""
    ctrls = []
    c1 = LinkBalancerCtrl(sw=['sw1'], srv=['s1a', 's1b', 's3'], greedy=greedy, greedylimit=greedylimit)
    c2 = LinkBalancerCtrl(sw=['sw2'], srv=['s1a', 's1b', 's3'], greedy=greedy, greedylimit=greedylimit)
    c3 = LinkBalancerCtrl(sw=['sw3'], srv=['s1a', 's1b', 's3'], greedy=greedy, greedylimit=greedylimit)
    ctrls.append(c1)
    ctrls.append(c2)
    ctrls.append(c3)
    return ctrls

