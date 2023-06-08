import networkx as nx
import matplotlib.pyplot as plt
import itertools
import warnings
warnings.filterwarnings("ignore")

App6_G = nx.DiGraph()

# Define functions and structural vertices in the App
# AppWorkflow_G.add_node($Vertex_Name, pos=$Vertex_Position)
App6_G.add_node('Start', pos=(0, 1))
App6_G.add_node(1, pos=(1, 1))
App6_G.add_node(2, pos=(2, 0))
App6_G.add_node(3, pos=(2, 3))
App6_G.add_node(4, pos=(3, 1))
App6_G.add_node(5, pos=(2, 2))
App6_G.add_node(6, pos=(4, 1))
App6_G.add_node('End', pos=(5, 1))

# Define edges and the transition probability
# AppWorkflow_G.add_weighted_edges_from([$start from, $end at, $transition probability])
App6_G.add_weighted_edges_from([(1, 2, 1), (1, 5, 0.2), (1, 3, 0.8), (3, 4, 1), (5, 4, 1), (2, 4, 1), (4, 1, 0.1),
                          (4, 4, 0.2), (4, 6, 0.7)])
App6_G.add_weighted_edges_from([('Start', 1, 1), (6, 'End', 1)])

# Show the workflow graph
pos_App6_G = nx.get_node_attributes(App6_G, 'pos')
nx.draw(App6_G, pos_App6_G, with_labels=True)
labels_App6_G = nx.get_edge_attributes(App6_G, 'weight')
nx.draw_networkx_edge_labels(App6_G, pos_App6_G, edge_labels=labels_App6_G)
pos_higher_offset_App6_G = {}
for k, v in pos_App6_G.items():
    pos_higher_offset_App6_G[k] = (v[0], v[1] + 0.15)
plt.show()

{'Start': 0, 1: 1.1428571428571428, 2: 1.1428571428571428, 3: 0.9142857142857143, 4: 1.4285714285714286, 
 5: 0.22857142857142856, 6: 1, 'End': 0}

import PerformanceProfile

f1_pf = PerformanceProfile.f1_pf
f2_pf = PerformanceProfile.f2_pf
f3_pf = PerformanceProfile.f3_pf
f4_pf = PerformanceProfile.f4_pf
f5_pf = PerformanceProfile.f5_pf
f6_pf = PerformanceProfile.f6_pf

# adding performance profile for all nodes
App6_G.nodes[1]['private_perf_profile'] = f1_pf['private']
App6_G.nodes[2]['private_perf_profile'] = f2_pf['private']
App6_G.nodes[3]['private_perf_profile'] = f3_pf['private']
App6_G.nodes[4]['private_perf_profile'] = f4_pf['private']
App6_G.nodes[5]['private_perf_profile'] = f5_pf['private']
App6_G.nodes[6]['private_perf_profile'] = f6_pf['private']

App6_G.nodes[1]['public_perf_profile'] = f1_pf['public']
App6_G.nodes[2]['public_perf_profile'] = f2_pf['public']
App6_G.nodes[3]['public_perf_profile'] = f3_pf['public']
App6_G.nodes[4]['public_perf_profile'] = f4_pf['public']
App6_G.nodes[5]['public_perf_profile'] = f5_pf['public']
App6_G.nodes[6]['public_perf_profile'] = f6_pf['public']




import AppWorkflow


App = ServerlessAppWorkflow(G=App6_G.copy(), delayType='SFN') # need to Change Delay Type

optimizer = PerfOpt(App)

# Performance constraint is 6400 ms

print('Total Cost Under Performance Constraint')

Performance_constraint = 4000
Cost_constraint = 90

Both_Performance_constraint = 6000
Both_Cost_constraint = 60


configuration_under_perf_const = optimizer.PrerformanceConstraintModel(Performance_constraint)
perf_RT, perf_CT, perf_memType, perf_mem, perf_iterations_count, perf_target_changes = configuration_under_perf_const # for graph purposes

configuration_under_cost_const = optimizer.CostConstraintModel(Cost_constraint)
cost_RT, cost_CT, cost_memType, cost_mem, cost_iterations_count, cost_target_changes = configuration_under_cost_const

configuration_under_perfCost_const = optimizer.Cost_Performance_ConstraintModel(Both_Performance_constraint, Both_Cost_constraint)
perfCost_RT, perfCost_CT, perfCost_memType, perfCost_mem, perfCost_iterations_count, perfCost_target_changes = configuration_under_perfCost_const
