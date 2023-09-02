import itertools
import warnings
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt


warnings.filterwarnings("ignore")


class PerfOpt:
    def __init__(self, Appworkflow, mem_list=None):
        self.App = Appworkflow

        if mem_list is None:
            self.mem_list = [128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024, 1088, 1152,
                             1216,
                             1280, 1344, 1408, 1472, 1536, 1600, 1664, 1728, 1792, 1856, 1920, 1984, 2048, 2112, 2176,
                             2240,
                             2304, 2368, 2432, 2496, 2560, 2624, 2688, 2752, 2816, 2880, 2944, 3008]
        else:
            self.mem_list = mem_list

        # self.minimal_mem_configuration, self.maximal_mem_configuration, self.maximal_cost, self.minimal_avg_rt, self.minimal_cost, self.maximal_avg_rt = self.get_optimization_boundary()
        self.get_optimization_boundary()

        self.update_BCR('public')
        self.update_BCR('private')

        self.all_simple_paths = [path for path in
                                 nx.all_simple_paths(self.App.deloopedG, self.App.startPoint, self.App.endPoint)]

        self.simple_paths_num = len(self.all_simple_paths)

        self.CPcounter = 0

    # Update mem and rt attributes of each node in the workflow

    def update_mem_rt(self, G, mem_dict, configuration, updation):
        # # print('G, mem_dict, configuration, updation :',G, mem_dict, configuration, updation)
        for node in mem_dict:
            G.nodes[node]['mem'] = (mem_dict[node])

            if configuration == 'hybrid':
                configuration = G.nodes[node]['config_type']

            if updation:
                G.nodes[node]['config_type'] = configuration
            if configuration == 'public':
                G.nodes[node]['rt'] = G.nodes[node]['public_perf_profile'][mem_dict[node]]
            else:
                G.nodes[node]['rt'] = G.nodes[node]['private_perf_profile'][mem_dict[node]]

    # Update mem and rt attributes of each node in the workflow
    def update_App_workflow_mem_rt(self, App, mem_dict, configuration, updation):
        self.update_mem_rt(App.workflowG, mem_dict, configuration, updation)
        App.updateRT()

    def get_optimization_boundary(self):

        node_list = [item for item in self.App.workflowG.nodes]
        # # print('NodeList',node_list)

        # get minimal, maximal memory confiquration with private
        # get average rt for both above
        # why he ask for hybrid?
        # when still he is in maximal memory confiquration in private, but RT is higher than the his contrain
        # deploy some functions in public and reduce RT
        # meantime check the budget contrain,
        # we can get several situation under his budget and performance constrain

        # print("private memories", self.App.workflowG.nodes[1]['private_perf_profile'].keys())
        # print("public memories", self.App.workflowG.nodes[1]['public_perf_profile'].keys())

        public_minimal_mem_configuration = {node: min(self.App.workflowG.nodes[node]['public_perf_profile'].keys()) for node in
                                            node_list}
        self.public_minimal_mem_configuration = public_minimal_mem_configuration
        # print("public_minimal_mem_configuration", public_minimal_mem_configuration)

        # # print("Minimal Memory Configuration of Nodes",minimal_mem_configuration)

        public_maximal_mem_configuration = {node: max(self.App.workflowG.nodes[node]['public_perf_profile'].keys()) for node in
                                            node_list}
        self.public_maximal_mem_configuration = public_maximal_mem_configuration
        # print("public_maximal_mem_configuration", public_maximal_mem_configuration)

        # assume: user using maximum private confiq and need to change some into public to get better performance
        private_maximal_mem_configuration = {node: max(self.App.workflowG.nodes[node]['private_perf_profile'].keys()) for node in
                                             node_list}
        self.private_maximal_mem_configuration = private_maximal_mem_configuration

        private_minimal_mem_configuration = {node: min(self.App.workflowG.nodes[node]['private_perf_profile'].keys()) for node in
                                             node_list}
        self.private_minimal_mem_configuration = private_minimal_mem_configuration

        # print("private_minimal_mem_configuration", private_minimal_mem_configuration)
        # print("private_maximal_mem_configuration", private_maximal_mem_configuration)

        # # print("Maximal Memory Configuration",maximal_mem_configuration)

        # # print("-------Before Update_Number Of Executions of Each Node------ne",self.App.ne)
        # # print("-------Before Update_Number Of Executions of Each Node------deloopedGraph",self.App.deloopedG)
        # self.drawGraph(self.App.workflowG)
        # self.drawGraph(self.App.deloopedG)

        self.App.update_NE()

       # self.drawGraph(self.App.workflowG)
        # # print("-------After Update_NUmber of Executions of Each Node--",self.App.ne)
        # # print("-------After Update_Number Of Executions of Each Node------deloopedGraph",self.App.deloopedG)
        # self.drawGraph(self.App.deloopedG)

        #-----------------private max cost, min rt-------------------------#
        # Update Each node's Memory to max memory Congiguration In WorkFlowG
        # print()

        # print("private_maximal_mem_configuration", private_maximal_mem_configuration)
        self.update_App_workflow_mem_rt(
            self.App, private_maximal_mem_configuration, 'private', True)

        # Get Avarage Cost of WorkFlowG based On billingModel and Num of execution of each node
        # If we used max MemConfig then It would maximal Cost
        # print("in Private, If we used max MemConfig then It would maximal Cost, min time")
        private_maximal_cost = self.App.get_avg_cost()
        self.private_maximal_cost = private_maximal_cost
        # print("private_maximal_cost", private_maximal_cost)

        # Simplify Graph To get average ResponceTime
        # Removes paralel brach,loops
        # # print("        ")
        # # print('---RT before simple Graph--',self.App.rt)
        # # print('---DAGrt before of Simple Graph, before simplify the Graph',self.App.DAGrt)
        # # print("---WorkFlow Graph before Simple Dag- Max memory")
        # self.drawGraph(self.App.workflowG)
        # # print("--SimpleGrapg before simplifies--")
        # self.drawGraph(self.App.simpleDAG)

        self.App.get_simple_dag()
        # # print("        ")
        # # print("--WorkFlow Graph after end of simplifies--Max memory")
        # self.drawGraph(self.App.workflowG)
        # # print('--SimpleGrapg after simplifies')
        # self.drawGraph(self.App.simpleDAG)
        # # print('---RT After simple Graph--',self.App.rt)
        # # print('---DAGrt After of Simple Graph, After simplify the Graph',self.App.DAGrt)
        # # print("---WorkFlow Graph by end Of Simple Dag")

        # Average RT calculated for simple Graph, with help of edgeDelays, DAGrt

        # Max memory used that's why it minimal_avg_rt, want to minimize more with public config
        private_minimal_avg_rt = self.App.get_avg_rt()
        self.private_minimal_avg_rt = private_minimal_avg_rt
        # print("private_minimal_avg_rt", private_minimal_avg_rt)

        #-----------------private min cost, max rt-------------------------#
        # print()

        # print("private_minimal_mem_configuration", private_minimal_mem_configuration)
        self.update_App_workflow_mem_rt(
            self.App, private_minimal_mem_configuration, 'private', True)

        # print("in Private, If we used max MemConfig then It would maximal Cost, min time")
        private_minimal_cost = self.App.get_avg_cost()
        self.private_minimal_cost = private_minimal_cost
        # print("private_minimal_cost", private_minimal_cost)

        self.App.get_simple_dag()

        private_maximal_avg_rt = self.App.get_avg_rt()
        self.private_maximal_avg_rt = private_maximal_avg_rt
        # print("private_minimal_avg_rt", private_maximal_avg_rt)

        # Again memory of workflow gets Updated with minimal memory configutarions with public
        # print()

        # print("public_minimal_mem_configuration", public_minimal_mem_configuration)
        self.update_App_workflow_mem_rt(
            self.App, public_minimal_mem_configuration, 'public', True)

        # MinCost calculated by help of Node execution(probability) and costModel
        # print("in Public, If we used min MemConfig then It would min Cost, max time")
        public_minimal_cost = self.App.get_avg_cost()
        self.public_minimal_cost = public_minimal_cost
        # print("public_minimal_cost", public_minimal_cost)

        # Simple Dag updated with new DAGrt for new memory configurations
        # # print("---WorkFlow Graph before Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)

        self.App.get_simple_dag()

        # # print("---WorkFlow Graph After Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)

        # Max average Time calculated because now we used min mem configurations
        public_maximal_avg_rt = self.App.get_avg_rt()
        self.public_maximal_avg_rt = public_maximal_avg_rt
        # print("public_maximal_avg_rt", public_maximal_avg_rt)

        # public max mem config
        # print()

        # print("public_maximal_mem_configuration", public_maximal_mem_configuration)
        self.update_App_workflow_mem_rt(
            self.App, public_maximal_mem_configuration, 'public', True)

        # print("in Public, If we used max MemConfig then It would max Cost, min time")
        public_maximal_cost = self.App.get_avg_cost()
        self.public_maximal_cost = public_maximal_cost
        # print("public_maximal_cost", public_maximal_cost)

        # Simple Dag updated with new DAGrt for new memory configurations
        # # print("---WorkFlow Graph before Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)

        self.App.get_simple_dag()

        # # print("---WorkFlow Graph After Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)

        # Max average Time calculated because now we used min mem configurations
        public_minimal_avg_rt = self.App.get_avg_rt()
        self.public_minimal_avg_rt = public_minimal_avg_rt
        # print("public_minimal_avg_rt", public_minimal_avg_rt)

        # # print("Get_opt_boundry", (minimal_mem_configuration, maximal_mem_configuration, maximal_cost, minimal_avg_rt, minimal_cost,
        #         maximal_avg_rt))
        # return (1, 2, 3, 4, 5)
        return(private_minimal_avg_rt, private_maximal_avg_rt, public_minimal_avg_rt, public_maximal_avg_rt)
    # Get the Benefit Cost Ratio (absolute value) of each function
    def update_BCR(self, configuration):
        node_list = [item for item in self.App.workflowG.nodes]
        # print("node_list", node_list)
        if configuration == 'public':
            for node in node_list:
                available_mem_list = [item for item in np.sort(
                    list(self.App.workflowG.nodes[node]['public_perf_profile'].keys()))]
                available_rt_list = [self.App.workflowG.nodes[node]
                                     ['public_perf_profile'][item] for item in available_mem_list]
                slope, intercept = np.linalg.lstsq(np.vstack([available_mem_list, np.ones(len(available_mem_list))]).T,
                                                   np.array(available_rt_list), rcond=None)[0]
                self.App.workflowG.nodes[node]['public_BCR'] = np.abs(slope)
                # # print("# Get the Benefit Cost Ratio (absolute value) of each function")

        # Plot the data
            #   fig, ax = plt.subplots()

            #   ax.plot(available_mem_list, available_rt_list, label='private: '+ 'slope = ' + str(round(slope, 3)) + ', intercept = ' + str(round(intercept, 3)) )

            #   # Add axis labels and legend
            #   ax.set_xlabel('X Values')
            #   ax.set_ylabel('Y Values')
            #   plt.title('Scatter plot with thresholds')
            # # Draw a horizontal line at the y threshold
            #   plt.axhline(y=2000, color='r', linestyle='--')
            # # Draw a vertical line at the x threshold
            #   plt.axvline(x=2000, color='r', linestyle='--')
            #   ax.legend()
            #   # Show the plot
            #   plt.show()

            else:
                for node in node_list:
                    available_mem_list = [item for item in np.sort(
                        list(self.App.workflowG.nodes[node]['private_perf_profile'].keys()))]
                    available_rt_list = [
                        self.App.workflowG.nodes[node]['private_perf_profile'][item] for item in available_mem_list]
                    slope, intercept = np.linalg.lstsq(np.vstack([available_mem_list, np.ones(len(available_mem_list))]).T,
                                                       np.array(available_rt_list), rcond=None)[0]
                    self.App.workflowG.nodes[node]['private_BCR'] = np.abs(
                        slope)
                    # # print("# Get the Benefit Cost Ratio (absolute value) of each function")

    # Find the probability refined critical path in self.App
    def find_PRCP(self, i=0, order=0, leastCritical=False):
        self.CPcounter += 1

        # self.App.delooped Graph - workFlowGraph withOut selfloop ||
        # all-simple_path - node 1 to node 6 without any loop
        # simple path may not consist all nodes
        # tp list -> {path1:productOfProbability,path2:productOfProbability2}
        tp_list = self.App.getTP(self.App.deloopedG, self.all_simple_paths)
        # example-> [0.9999999999999999, 0.19999999999999998, 0.7999999999999999]

        # rt_list -> {path1:sumOfRTofnode,path2:sumofRTofNodes}
        rt_list = self.App.sumRT_with_NE(
            self.all_simple_paths, includeStartNode=True, includeEndNode=True)
        # example -> [2701.498042857143, 2497.029951428571, 2627.4685571428568]

        prrt_list = np.multiply(tp_list, rt_list)
        # example ->[2701.49804286  499.40599029 2101.97484571]

        # least criticle->return min (rt * prob) of simple paths
        # # print(tp_list, rt_list, prrt_list)
        if (leastCritical):
            PRCP = np.argsort(prrt_list)[order]

        else:
            PRCP = np.argsort(prrt_list)[-1 - order]

        # Return the simple path that consist least pathRT*pathPb  if leastCriticle=True
        # Else return high pathRT*pathPb if leastCriticle=False
        return (self.all_simple_paths[PRCP])

    # Update the list of available memory configurations in ascending order

    def update_available_mem_list(self):
        node_list = [item for item in self.App.workflowG.nodes]
        for node in node_list:

            public_available_mem_list = [item for item in
                                         np.sort(list(self.App.workflowG.nodes[node]['public_perf_profile'].keys()))]

            # Sorted list
            self.App.workflowG.nodes[node]['public_available_mem'] = public_available_mem_list

            private_available_mem_list = [item for item in
                                          np.sort(list(self.App.workflowG.nodes[node]['private_perf_profile'].keys()))]

            # Sorted list
            self.App.workflowG.nodes[node]['private_available_mem'] = private_available_mem_list

    def drawGraph(self, G):
        pos = nx.planar_layout(G)
        nx.draw(G, pos, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        pos_higher_offset = {}
        for k, v in pos.items():
            pos_higher_offset[k] = (v[0], v[1] + 0.05)
        labels = nx.get_node_attributes(G, 'rt')
        nx.draw_networkx_labels(G, pos_higher_offset, labels=labels)
        # plt.show()

    def PrerformanceConstraintModel(self, rt_constraint, cloud_type):
        # print()
        # print()
        # print()
        # print()
        # print()

        # print("##########----------PrerformanceConstraintModel----------############")
        # print('-----------INITIATE PERF CONST MODEL--------------------')

        # if public minimal cost is lesser than the cost connstraint and public maximal avg time is lesser than rt constraint
        # the optimal solution is come under finding the optimal solution for public onlyp

        # self.drawGraph(App.workflowG)
        # Update memory of each node based on log data
        self.update_available_mem_list()
        if cloud_type == 'public':
            iterations_count_limit = 100
        elif cloud_type == 'private':
            iterations_count_limit = 100
        else:
            iterations_count_limit = 100
        # Configure AppWorkFlow to Max_memory Configuration -> so RT is minimal
        if cloud_type == 'private':
            self.update_App_workflow_mem_rt(
                self.App, self.private_maximal_mem_configuration, "private", True)
            current_avg_rt = self.private_minimal_avg_rt
            current_cost = self.private_maximal_cost
            # performance_surplus = rt_constraint - current_avg_rt
        else:
            self.update_App_workflow_mem_rt(
                self.App, self.public_maximal_mem_configuration, "public", True)
            current_avg_rt = self.public_minimal_avg_rt
            current_cost = self.public_maximal_cost
        
        performance_surplus = rt_constraint - current_avg_rt
        # cost_public_maximal_mem_configuration = self.public_maximal_cost
        # print("current_avg_rt", current_avg_rt)

        # Nigotiatable RT
        
        # cost_surplus = cost_public_maximal_mem_configuration - cost_constraint
        # print("performance_surplus", performance_surplus)

        # Current cost is the Maximal Cost Because We used Max Memory Configuration for each Node
        
        # print("current_cost", current_cost)

        last_e2ert_cost_BCR = 0
        order = 0
        iterations_count = 0
        target_changes = ""

        # # print('--------------------Before Going While Loop------------------------------------')
        # # print(App.workflowG)
        # self.drawGraph(self.App.workflowG)
        self.App.get_simple_dag()
        self.drawGraph(self.App.simpleDAG)
        # print('at the start: ', rt_constraint, current_avg_rt, performance_surplus)
        # Until Negotiatable RT get finished
        while (round(performance_surplus, 4) >= 0):
            iterations_count += 1
            # print('in the ', iterations_count, ' perf sur is ', performance_surplus, ' current rt is ', current_avg_rt)
            # def_rt = self.App.get_avg_rt()
            # # print('self.App.get_avg_rt() is', def_rt)
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$------iterations_count", iterations_count)
            # Criticle Path ->least criticle -simple path with min RTofpath*Pb of path
            critical_path = self.find_PRCP(
                iterations_count, leastCritical=True, order=order)
            # print("critical_path", critical_path)
            max_cost_reduction_of_each_node = {}
            mem_backup = nx.get_node_attributes(self.App.workflowG, 'mem')
            mem_backupType = nx.get_node_attributes(
                self.App.workflowG, 'config_type')
            # mem_type_backup = ""
            # print('mem_backup', mem_backup)
            # print('mem_backupType', mem_backupType)

            for node in critical_path:  # get nodes in a criticle path -> process single node of criticle path
                # print('for node in criti..........')
                # {Mem1:costReduction,Mem2:costReduction} for node x
                cost_reduction_of_each_mem_config = {}
                # # print('cost_reduction_of_each_mem_config AFTER DEFINED', cost_reduction_of_each_mem_config)

                # loop with available public memories for selected node of criticle path
                if cloud_type == 'public' or cloud_type == 'hybrid':
                    for mem in self.App.workflowG.nodes[node]['public_available_mem']:
                        # print('for mem in self.app...........')
                        if (mem >= mem_backup[node]):
                            # # print('break, avoid larger memories BREAK')
                            break  # Our intention is reduce cost -> avoid larger memories
                        # mem_type_backup = mem_backupType[node]
                        # update memory of that node with available mem
                        self.update_App_workflow_mem_rt(
                            self.App, {node: mem}, 'public', True)
                        self.App.get_simple_dag()  # produce new RT with helpof simple Dag
                        temp_avg_rt = self.App.get_avg_rt()
                        increased_rt = temp_avg_rt - current_avg_rt  # Increase in RT
                        temp_avg_cost = self.App.get_avg_cost()
                        cost_reduction = current_cost - temp_avg_cost  # Reduction in cost
                        # # print(mem, ' public', 'INCREASED RT:', increased_rt, '   COST REDUCTION:', cost_reduction)

                        # if (increased_rt < performance_surplus and cost_reduction < 0):  ##### cost increase
                        # # print('********PUBLIC****inc rt, per surplus**************', increased_rt, performance_surplus)
                        # # print('******PUBLIC********cost_reduction****', mem, "     ", temp_avg_cost,  cost_reduction)

                        if (increased_rt < performance_surplus):  # cost reduce
                            # print('if (increased_rt < performance_surplus):........')
                            if iterations_count > iterations_count_limit:
                                if cost_reduction > 0:
                                    # print('if (increased_rt < performance_surplus):........ @ all 3 ifs.............')
                                    cost_reduction_of_each_mem_config[str(
                                        mem) + ' public'] = (cost_reduction, increased_rt)
                            # # print('increased_rt < performance_surplus and cost_reduction > 0')
                            else:
                                cost_reduction_of_each_mem_config[str(
                                    mem) + ' public'] = (cost_reduction, increased_rt)

                    self.update_App_workflow_mem_rt(
                        self.App, {node: mem_backup[node]}, mem_backupType[node], True)

                # loop with available private memories for selected node of criticle path
                if cloud_type == 'private' or cloud_type == 'hybrid':
                    for mem in self.App.workflowG.nodes[node]['private_available_mem']:
                        if (mem >= mem_backup[node]):
                            # # print('break, avoid larger memories BREAK')
                            break  # Our intention is reduce cost -> avoid larger memories
                        # mem_type_backup = mem_backupType[node]
                        # update memory of that node with available mem
                        self.update_App_workflow_mem_rt(
                            self.App, {node: mem}, 'private', True)
                        self.App.get_simple_dag()  # produce new RT with helpof simple Dag
                        temp_avg_rt = self.App.get_avg_rt()
                        increased_rt = temp_avg_rt - current_avg_rt  # Increase in RT
                        temp_avg_cost = self.App.get_avg_cost()
                        cost_reduction = current_cost - temp_avg_cost  # Reduction in cost
                        # # print(mem, ' private', 'INCREASED RT:', increased_rt, '   COST REDUCTION:', cost_reduction)

                        # if (increased_rt < performance_surplus and cost_reduction < 0):
                        # # print('******PRIVATE******inc rt, per surplus**************', increased_rt, performance_surplus)
                        # # print('**********PRIVATE********cost_reduction********', mem, "     ", temp_avg_cost, cost_reduction)

                        if (increased_rt < performance_surplus):
                            if iterations_count > iterations_count_limit:
                                if cost_reduction > 0:
                                    cost_reduction_of_each_mem_config[str(
                                        mem) + ' private'] = (cost_reduction, increased_rt)

                            # # print('increased_rt < performance_surplus and cost_reduction > 0')
                            else:
                                cost_reduction_of_each_mem_config[str(
                                    mem) + ' private'] = (cost_reduction, increased_rt)

                    self.update_App_workflow_mem_rt(
                        self.App, {node: mem_backup[node]}, mem_backupType[node], True)  # Reset memConfigurations

                # # print("cost_reduction_of_each_mem_config AFTER LOOPS", cost_reduction_of_each_mem_config)

                if (len(cost_reduction_of_each_mem_config) != 0):
                    # print('if (len(cost_reduction_of_each_mem_config) != 0):///////////////////////////////////////')
                    # get max cost reduction for a node
                    max_cost_reduction = np.max(
                        [item[0] for item in cost_reduction_of_each_mem_config.values()])
                    min_increased_rt_under_MAX_cost_reduction = np.min(
                        [item[1] for item in cost_reduction_of_each_mem_config.values() if
                         item[0] == max_cost_reduction])  # Get incresed RT under Max_cost reduction
                    # max_cost_reduction_memType = cost_reduction_of_each_mem_config[cost_reduction_of_each_mem_config.index(min_increased_rt_under_MAX_cost_reduction)]
                    # print('max cost reduction for each node: ', max_cost_reduction, 'min_increased_rt_under_MAX_cost_reduction: ', min_increased_rt_under_MAX_cost_reduction)
                    reversed_dict = dict(
                        zip(cost_reduction_of_each_mem_config.values(), cost_reduction_of_each_mem_config.keys()))
                    max_cost_reduction_of_each_node[node] = (
                        reversed_dict[(
                            max_cost_reduction, min_increased_rt_under_MAX_cost_reduction)],
                        max_cost_reduction,
                        min_increased_rt_under_MAX_cost_reduction)
                # print("ADDED MEMORY: ", max_cost_reduction_of_each_node)

            if (len(max_cost_reduction_of_each_node) == 0):
                if (order >= self.simple_paths_num - 1):
                    break
                else:
                    order += 1
                    continue

            # print("max_cost_reduction_of_each_node", max_cost_reduction_of_each_node)
            max_cost_reduction = np.max(
                [item[1] for item in max_cost_reduction_of_each_node.values()])
            # print("max_cost_reduction", max_cost_reduction)
            min_increased_rt_under_MAX_cost_reduction = np.min(
                [item[2] for item in max_cost_reduction_of_each_node.values() if item[1] == max_cost_reduction])
            # print("min_increased_rt_under_MAX_cost_reduction", min_increased_rt_under_MAX_cost_reduction)

            target_mem_list = [item[0] for item in max_cost_reduction_of_each_node.values() if
                               item[1] == max_cost_reduction
                               and
                               item[2] == min_increased_rt_under_MAX_cost_reduction]
            # print('target_mem_list', target_mem_list)
            target_mem = 10000
            target_mem_type = ''
            target_node = -1
            for tag_mem in target_mem_list:
                if int(tag_mem.split()[0]) < target_mem:
                    target_mem = int(tag_mem.split()[0])
                    # print('target_mem_type', tag_mem.split()[1])
                    target_mem_type = tag_mem.split()[1]

            # print("target_mem", target_mem)
            target_node = -1

            for key1 in max_cost_reduction_of_each_node:
                if max_cost_reduction_of_each_node[key1][1] == max_cost_reduction:
                    target_node = key1

            # print("target_node", target_node)
            # print("target_mem_type", target_mem_type)

            target_changes += str(target_node)
            target_changes += ' : '
            target_changes += str(target_mem)
            target_changes += ' '
            target_changes += target_mem_type
            target_changes += " "

            self.update_App_workflow_mem_rt(
                self.App, {target_node: target_mem}, target_mem_type, True)
            max_cost_reduction = max_cost_reduction_of_each_node[target_node][1]
            min_increased_rt_under_MAX_cost_reduction = max_cost_reduction_of_each_node[
                target_node][2]
            
            current_cost = current_cost - max_cost_reduction
            performance_surplus = performance_surplus - \
                min_increased_rt_under_MAX_cost_reduction
            current_avg_rt = current_avg_rt + min_increased_rt_under_MAX_cost_reduction

            # current_cost = self.App.get_avg_cost()
            # current_avg_rt = self.App.get_avg_rt()
            # performance_surplus = rt_constraint - current_avg_rt

            current_e2ert_cost_BCR = max_cost_reduction / \
                min_increased_rt_under_MAX_cost_reduction

            if (current_e2ert_cost_BCR == float('Inf')):
                last_e2ert_cost_BCR = 0
            else:
                last_e2ert_cost_BCR = current_e2ert_cost_BCR

        current_mem_configuration = nx.get_node_attributes(
            self.App.workflowG, 'mem')
        current_mem_configuration_type = nx.get_node_attributes(
            self.App.workflowG, 'config_type')

        # # print(self.App.workflowG)
        # # print(self.App.get_simple_dag())
        del current_mem_configuration['Start']
        del current_mem_configuration['End']
        del current_mem_configuration_type['Start']
        del current_mem_configuration_type['End']
        print('Optimized Memory Configuration: {}'.format(current_mem_configuration))
        print('Optimized Memory Configuration Type: {}'.format( current_mem_configuration_type))
        print('Average end-to-end response time: {}'.format(current_avg_rt))
        print('Average Cost: {}'.format(current_cost))
        print('  in:  ', cloud_type,'-  itt count: ', iterations_count, ' rt const: ', rt_constraint)
        print('Performance Optimization Completed.')

        # final_rt = self.App.get_avg_rt()
        # final_cost = self.App.get_avg_cost()
        # # print('current_avg_rt', current_avg_rt, 'final_rt', final_rt)
        # # print('current_cost', current_cost, 'final_cost', final_cost)
        response={}
        response['perf_const'] = rt_constraint
        response['Achived_rt']=round(current_avg_rt, 2)
        response['Achived_cost']=round(current_cost, 2)
        response['CloudTypeOfFunctions']=current_mem_configuration_type
        response['MemoryOfFunctions']=current_mem_configuration
        response['TargetChanges']=target_changes
        response['IterationCount']=iterations_count

        return response
