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
        # print('G, mem_dict, configuration, updation :',G, mem_dict, configuration, updation)
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
        # print('NodeList',node_list)

        # get minimal, maximal memory confiquration with private
        # get average rt for both above
        # why he ask for hybrid? 
              # when still he is in maximal memory confiquration in private, but RT is higher than the his contrain
        # deploy some functions in public and reduce RT
        # meantime check the budget contrain, 
        # we can get several situation under his budget and performance constrain
        
        print("private memories", self.App.workflowG.nodes[1]['private_perf_profile'].keys())
        print("public memories", self.App.workflowG.nodes[1]['public_perf_profile'].keys())

        public_minimal_mem_configuration = {node: min(self.App.workflowG.nodes[node]['public_perf_profile'].keys()) for node in
                                     node_list}
        self.public_minimal_mem_configuration = public_minimal_mem_configuration
        print("public_minimal_mem_configuration", public_minimal_mem_configuration)
        
        # print("Minimal Memory Configuration of Nodes",minimal_mem_configuration)
        
        public_maximal_mem_configuration = {node: max(self.App.workflowG.nodes[node]['public_perf_profile'].keys()) for node in
                                     node_list}
        self.public_maximal_mem_configuration = public_maximal_mem_configuration
        print("public_maximal_mem_configuration", public_maximal_mem_configuration)


        # assume: user using maximum private confiq and need to change some into public to get better performance
        private_maximal_mem_configuration = {node: max(self.App.workflowG.nodes[node]['private_perf_profile'].keys()) for node in
                                     node_list}
        self.private_maximal_mem_configuration = private_maximal_mem_configuration

        private_minimal_mem_configuration = {node: min(self.App.workflowG.nodes[node]['private_perf_profile'].keys()) for node in
                                     node_list}
        self.private_minimal_mem_configuration = private_minimal_mem_configuration

        print("private_minimal_mem_configuration", private_minimal_mem_configuration)
        print("private_maximal_mem_configuration", private_maximal_mem_configuration)
        
        # print("Maximal Memory Configuration",maximal_mem_configuration)
        
        # print("-------Before Update_Number Of Executions of Each Node------ne",self.App.ne)
        # print("-------Before Update_Number Of Executions of Each Node------deloopedGraph",self.App.deloopedG)
        # self.drawGraph(self.App.workflowG)
        # self.drawGraph(self.App.deloopedG)

        self.App.update_NE()

       # self.drawGraph(self.App.workflowG)
        # print("-------After Update_NUmber of Executions of Each Node--",self.App.ne)
        # print("-------After Update_Number Of Executions of Each Node------deloopedGraph",self.App.deloopedG)
        # self.drawGraph(self.App.deloopedG)
           
        
         #-----------------private max cost, min rt-------------------------#
        #Update Each node's Memory to max memory Congiguration In WorkFlowG
        print()

        print("private_maximal_mem_configuration", private_maximal_mem_configuration)     
        self.update_App_workflow_mem_rt(self.App, private_maximal_mem_configuration, 'private', True)
        
        #Get Avarage Cost of WorkFlowG based On billingModel and Num of execution of each node
        #If we used max MemConfig then It would maximal Cost
        print("in Private, If we used max MemConfig then It would maximal Cost, min time")
        private_maximal_cost = self.App.get_avg_cost()
        self.private_maximal_cost = private_maximal_cost
        print("private_maximal_cost", private_maximal_cost)
        
        #Simplify Graph To get average ResponceTime
        #Removes paralel brach,loops
        # print("        ")
        # print('---RT before simple Graph--',self.App.rt)
        # print('---DAGrt before of Simple Graph, before simplify the Graph',self.App.DAGrt)
        # print("---WorkFlow Graph before Simple Dag- Max memory")
        # self.drawGraph(self.App.workflowG)
        # print("--SimpleGrapg before simplifies--")
        # self.drawGraph(self.App.simpleDAG)

        self.App.get_simple_dag()
        # print("        ")
        # print("--WorkFlow Graph after end of simplifies--Max memory")
        # self.drawGraph(self.App.workflowG)
        # print('--SimpleGrapg after simplifies')
        # self.drawGraph(self.App.simpleDAG)
        # print('---RT After simple Graph--',self.App.rt)
        # print('---DAGrt After of Simple Graph, After simplify the Graph',self.App.DAGrt)
        # print("---WorkFlow Graph by end Of Simple Dag")
    
        #Average RT calculated for simple Graph, with help of edgeDelays, DAGrt

        #Max memory used that's why it minimal_avg_rt, want to minimize more with public config
        private_minimal_avg_rt = self.App.get_avg_rt()
        self.private_minimal_avg_rt = private_minimal_avg_rt
        print("private_minimal_avg_rt", private_minimal_avg_rt)

        #-----------------private min cost, max rt-------------------------#
        print()

        print("private_minimal_mem_configuration", private_minimal_mem_configuration)
        self.update_App_workflow_mem_rt(self.App, private_minimal_mem_configuration, 'private', True)
        
        print("in Private, If we used max MemConfig then It would maximal Cost, min time")
        private_minimal_cost = self.App.get_avg_cost()
        self.private_minimal_cost = private_minimal_cost
        print("private_minimal_cost", private_minimal_cost)

        self.App.get_simple_dag()

        private_maximal_avg_rt = self.App.get_avg_rt()
        self.private_maximal_avg_rt = private_maximal_avg_rt
        print("private_minimal_avg_rt", private_maximal_avg_rt)


        #Again memory of workflow gets Updated with minimal memory configutarions with public
        print()

        print("public_minimal_mem_configuration", public_minimal_mem_configuration)
        self.update_App_workflow_mem_rt(self.App, public_minimal_mem_configuration, 'public', True)
        
        #MinCost calculated by help of Node execution(probability) and costModel
        print("in Public, If we used min MemConfig then It would min Cost, max time")
        public_minimal_cost = self.App.get_avg_cost()
        self.public_minimal_cost = public_minimal_cost
        print("public_minimal_cost", public_minimal_cost)
        
        #Simple Dag updated with new DAGrt for new memory configurations
        # print("---WorkFlow Graph before Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)

        self.App.get_simple_dag()

        # print("---WorkFlow Graph After Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)


        #Max average Time calculated because now we used min mem configurations
        public_maximal_avg_rt = self.App.get_avg_rt()
        self.public_maximal_avg_rt = public_maximal_avg_rt
        print("public_maximal_avg_rt", public_maximal_avg_rt)

        # public max mem config
        print()

        print("public_maximal_mem_configuration", public_maximal_mem_configuration)
        self.update_App_workflow_mem_rt(self.App, public_maximal_mem_configuration, 'public', True)
        
        print("in Public, If we used max MemConfig then It would max Cost, min time")
        public_maximal_cost = self.App.get_avg_cost()
        self.public_maximal_cost = public_maximal_cost
        print("public_maximal_cost", public_maximal_cost)
        
        #Simple Dag updated with new DAGrt for new memory configurations
        # print("---WorkFlow Graph before Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)

        self.App.get_simple_dag()

        # print("---WorkFlow Graph After Simple Dag- Min memory")
        # self.drawGraph(self.App.workflowG)


        #Max average Time calculated because now we used min mem configurations
        public_minimal_avg_rt = self.App.get_avg_rt()
        self.public_minimal_avg_rt = public_minimal_avg_rt
        print("public_minimal_avg_rt", public_minimal_avg_rt)
        
        # print("Get_opt_boundry", (minimal_mem_configuration, maximal_mem_configuration, maximal_cost, minimal_avg_rt, minimal_cost,
        #         maximal_avg_rt))
        # return (1, 2, 3, 4, 5)

    # Get the Benefit Cost Ratio (absolute value) of each function
    def update_BCR(self, configuration):
        node_list = [item for item in self.App.workflowG.nodes]
        print("node_list", node_list)
        if configuration == 'public':
          for node in node_list:
              available_mem_list = [item for item in np.sort(list(self.App.workflowG.nodes[node]['public_perf_profile'].keys()))]
              available_rt_list = [self.App.workflowG.nodes[node]['public_perf_profile'][item] for item in available_mem_list]
              slope, intercept = np.linalg.lstsq(np.vstack([available_mem_list, np.ones(len(available_mem_list))]).T,
                                                np.array(available_rt_list), rcond=None)[0]
              self.App.workflowG.nodes[node]['public_BCR'] = np.abs(slope)
              # print("# Get the Benefit Cost Ratio (absolute value) of each function")


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
              available_mem_list = [item for item in np.sort(list(self.App.workflowG.nodes[node]['private_perf_profile'].keys()))]
              available_rt_list = [self.App.workflowG.nodes[node]['private_perf_profile'][item] for item in available_mem_list]
              slope, intercept = np.linalg.lstsq(np.vstack([available_mem_list, np.ones(len(available_mem_list))]).T,
                                                np.array(available_rt_list), rcond=None)[0]
              self.App.workflowG.nodes[node]['private_BCR'] = np.abs(slope)
              # print("# Get the Benefit Cost Ratio (absolute value) of each function")

    # Find the probability refined critical path in self.App
    def find_PRCP(self,i=0 ,order=0, leastCritical=False  ):
        self.CPcounter += 1
        
        #self.App.delooped Graph - workFlowGraph withOut selfloop ||
        #all-simple_path - node 1 to node 6 without any loop
        #simple path may not consist all nodes
        #tp list -> {path1:productOfProbability,path2:productOfProbability2}
        tp_list = self.App.getTP(self.App.deloopedG, self.all_simple_paths)
        #example-> [0.9999999999999999, 0.19999999999999998, 0.7999999999999999]
        
        #rt_list -> {path1:sumOfRTofnode,path2:sumofRTofNodes}
        rt_list = self.App.sumRT_with_NE(self.all_simple_paths, includeStartNode=True, includeEndNode=True)
        #example -> [2701.498042857143, 2497.029951428571, 2627.4685571428568]
        
        prrt_list = np.multiply(tp_list, rt_list)
        #example ->[2701.49804286  499.40599029 2101.97484571]
        
        #least criticle->return min (rt * prob) of simple paths 
        
        if (leastCritical):
            PRCP = np.argsort(prrt_list)[order]
            
        else:
            PRCP = np.argsort(prrt_list)[-1 - order]
            
        #Return the simple path that consist least pathRT*pathPb  if leastCriticle=True
        #Else return high pathRT*pathPb if leastCriticle=False
        return (self.all_simple_paths[PRCP])

    
    # Update the list of available memory configurations in ascending order
    def update_available_mem_list(self):
        node_list = [item for item in self.App.workflowG.nodes]
        for node in node_list:
            
            public_available_mem_list = [item for item in
                                      np.sort(list(self.App.workflowG.nodes[node]['public_perf_profile'].keys()))]
            
            self.App.workflowG.nodes[node]['public_available_mem'] = public_available_mem_list  # Sorted list

            private_available_mem_list = [item for item in
                                      np.sort(list(self.App.workflowG.nodes[node]['private_perf_profile'].keys()))]
            
            self.App.workflowG.nodes[node]['private_available_mem'] = private_available_mem_list  # Sorted list

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
        plt.show()

    def CostConstraintModel(self, budget):
        print()
        print()
        print()
        print()
        print()


        print('-----------INITIATE COST MODEL--------------------')
        self.update_available_mem_list() # Only for BCR - False
        
        self.update_App_workflow_mem_rt(self.App, self.private_minimal_mem_configuration, 'private', True)
        cost = self.private_minimal_cost
        print("cost", cost)

        #Take avg rt as maximum for All MinMemoryConfig
        current_avg_rt = self.private_maximal_avg_rt
        cost_surplus = budget - cost
        print('cost surplus: ', cost_surplus)
        print("current_avg_rt", current_avg_rt)
        
        #Take Current Cost as MinCost(because all memConfigs are minimums)
        current_cost = self.private_minimal_cost
        
        last_e2ert_cost_BCR = 0
        order = 0
        iterations_count = 0
        target_changes = ''
        
        while (round(cost_surplus, 4) >= 0):
            # print('----------------------come under while loop-----------------------')
            iterations_count += 1
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$------iterations_count", iterations_count)

            critical_path = self.find_PRCP(order=order, leastCritical=False)
            print('critical_path: ', critical_path)
            max_avg_rt_reduction_of_each_node = {}
            mem_backup = nx.get_node_attributes(self.App.workflowG, 'mem')
            mem_backupType = nx.get_node_attributes(self.App.workflowG, 'config_type')
            mem_type_backup = ""
            print('mem_backup', mem_backup)
            print('mem_backupType', mem_backupType)

            for node in critical_path:
                # print('----------------------come under cp for loop-----------------------', self.App.workflowG.nodes[node]['config_type'])

                avg_rt_reduction_of_each_mem_config = {}

                # if self.App.workflowG.nodes[node]['config_type'] == 'private':
                for mem in reversed(self.App.workflowG.nodes[node]['private_available_mem']):
                        # print('----------------------come under mem for loop-----------------------')

                        if (mem <= mem_backup[node]):
                            break
                        mem_type_backup = mem_backupType[node]

                        self.update_App_workflow_mem_rt(self.App, {node: mem}, 'private', True)
                        increased_cost = self.App.get_avg_cost() - current_cost
                        # print('--------==============----increased_cost------=================--------', increased_cost)
                        if (increased_cost < cost_surplus):
                            self.App.get_simple_dag()
                            rt_reduction = current_avg_rt - self.App.get_avg_rt()
                            # print('--------++++++++++++----rt_reduction------++++++++++++++++++++++++--------', rt_reduction)
                            if (rt_reduction > 0):
                                if iterations_count > 12:
                                    if increased_cost > 0:
                                        avg_rt_reduction_of_each_mem_config[str(mem)+ ' private'] = (rt_reduction, increased_cost)
                                else:
                                        avg_rt_reduction_of_each_mem_config[str(mem)+ ' private'] = (rt_reduction, increased_cost)

                                # print('--------++++++++++++----avg_rt_reduction_of_each_mem_config ADDED------++++++++++++++++++++++++--------', mem, increased_cost, rt_reduction)
                self.update_App_workflow_mem_rt(self.App, {node: mem_backup[node]}, mem_type_backup, True)

                
                for mem in reversed(self.App.workflowG.nodes[node]['public_available_mem']):
                # print('----------------------come under public for loop-----------------------')

                        if (mem <= mem_backup[node]):
                            break
                        mem_type_backup = mem_backupType[node]

                        self.update_App_workflow_mem_rt(self.App, {node: mem}, 'public', True)
                        increased_cost = self.App.get_avg_cost() - current_cost
                        if (increased_cost < cost_surplus):
                            self.App.get_simple_dag()
                            rt_reduction = current_avg_rt - self.App.get_avg_rt()
                            if (rt_reduction > 0):
                                if iterations_count > 12:
                                    if increased_cost > 0:
                                        avg_rt_reduction_of_each_mem_config[str(mem)+ ' public'] = (rt_reduction, increased_cost)
                                else:
                                        avg_rt_reduction_of_each_mem_config[str(mem)+ ' public'] = (rt_reduction, increased_cost)

                self.update_App_workflow_mem_rt(self.App, {node: mem_backup[node]}, mem_type_backup, True)

                # print('++++++++++++++++++++avg_rt_reduction_of_each_mem_config++++++++++++', avg_rt_reduction_of_each_mem_config)

                if (len(avg_rt_reduction_of_each_mem_config) != 0):
                    # print('--------------------come under if len check------------------')
                    max_rt_reduction = np.max([item[0] for item in avg_rt_reduction_of_each_mem_config.values()])
                    min_increased_cost_under_MAX_rt_reduction = np.min(
                        [item[1] for item in avg_rt_reduction_of_each_mem_config.values() if
                         item[0] == max_rt_reduction])
                    reversed_dict = dict(zip(avg_rt_reduction_of_each_mem_config.values(),
                                             avg_rt_reduction_of_each_mem_config.keys()))
                    max_avg_rt_reduction_of_each_node[node] = (
                        reversed_dict[(max_rt_reduction, min_increased_cost_under_MAX_rt_reduction)],
                        max_rt_reduction,
                        min_increased_cost_under_MAX_rt_reduction)
                    
                print("ADDED MEMORY: ", max_avg_rt_reduction_of_each_node)
                

            if (len(max_avg_rt_reduction_of_each_node) == 0):
                if (order >= self.simple_paths_num - 1):
                    break
                else:
                    order += 1
                    continue
           
            # max_rt_reduction = np.max([item[1] for item in max_avg_rt_reduction_of_each_node.values()])
            # min_increased_cost_under_MAX_rt_reduction = np.min(
            #     [item[2] for item in max_avg_rt_reduction_of_each_node.values() if item[1] == max_rt_reduction])
            
            print("max_cost_reduction_of_each_node", max_avg_rt_reduction_of_each_node)
            max_RT_reduction = np.max([item[1] for item in max_avg_rt_reduction_of_each_node.values()])
            print("max_RT_reduction", max_RT_reduction)
            min_increased_cost_under_MAX_RT_reduction = np.min(
                [item[2] for item in max_avg_rt_reduction_of_each_node.values() if item[1] == max_RT_reduction])
            print("min_increased_cost_under_MAX_RT_reduction", min_increased_cost_under_MAX_RT_reduction)

            # target_mem = np.min([item[0] for item in max_avg_rt_reduction_of_each_node.values() if
            #                      item[1] == max_rt_reduction and item[
            #                          2] == min_increased_cost_under_MAX_rt_reduction])
            # target_node = [key for key in max_avg_rt_reduction_of_each_node if
            #                max_avg_rt_reduction_of_each_node[key] == (
            #                    target_mem, max_rt_reduction, min_increased_cost_under_MAX_rt_reduction)][0]
            
            target_mem_list = [item[0] for item in max_avg_rt_reduction_of_each_node.values() if
                                 item[1] == max_RT_reduction 
                                 and 
                                 item[2] == min_increased_cost_under_MAX_RT_reduction]
            print('target_mem_list', target_mem_list)
            target_mem = 10000
            target_mem_type = ''
            target_node = -1
            for tag_mem in target_mem_list:
                if int(tag_mem.split()[0]) < target_mem:
                    target_mem = int(tag_mem.split()[0])
                    print('target_mem_type',tag_mem.split()[1])
                    target_mem_type = tag_mem.split()[1]

            print("target_mem", target_mem)
            target_node = -1

            for key1 in max_avg_rt_reduction_of_each_node:
                if max_avg_rt_reduction_of_each_node[key1][1] == max_RT_reduction:
                    target_node = key1

            print("target_node", target_node)
            print("target_mem_type", target_mem_type)

            target_changes += str(target_node)
            target_changes += ' : '
            target_changes += str(target_mem)
            target_changes += ' '
            target_changes += target_mem_type
            target_changes += ",  " 

            
            self.update_App_workflow_mem_rt(self.App, {target_node: target_mem}, target_mem_type, True)
            
            print('++++++++++++++max_avg_rt_reduction_of_each_node++++++++++++++++++', max_avg_rt_reduction_of_each_node)
            
            max_rt_reduction = max_avg_rt_reduction_of_each_node[target_node][1]
            print('++++++++++++++++++max_rt_reduction++++++++++++++++++', max_rt_reduction)

            min_increased_cost_under_MAX_rt_reduction = max_avg_rt_reduction_of_each_node[target_node][2]
            print('++++++++++++++++++min_increased_cost_under_MAX_rt_reduction++++++++++++++++++', min_increased_cost_under_MAX_rt_reduction)

            current_avg_rt = current_avg_rt - max_rt_reduction
            print('++++++++++++++++++current_avg_rt++++++++++++++++++', current_avg_rt)

            cost_surplus = cost_surplus - min_increased_cost_under_MAX_rt_reduction
            print('++++++++++++++++++cost_surplus++++++++++++++++++', cost_surplus)

            current_cost = self.App.get_avg_cost()
            print('++++++++++++++++++current_cost++++++++++++++++++', current_cost)
            
            current_e2ert_cost_BCR = max_rt_reduction / min_increased_cost_under_MAX_rt_reduction
            if (current_e2ert_cost_BCR == float('Inf')):
                last_e2ert_cost_BCR = 0
            else:
                last_e2ert_cost_BCR = current_e2ert_cost_BCR

        current_mem_configuration = nx.get_node_attributes(self.App.workflowG, 'mem')
        current_mem_configuration_type = nx.get_node_attributes(self.App.workflowG, 'config_type')

        del current_mem_configuration['Start']
        del current_mem_configuration['End']
        del current_mem_configuration_type['Start']
        del current_mem_configuration_type['End']
        print('Optimized Memory Configuration: {}'.format(current_mem_configuration))
        print('Optimized Memory Configuration: {}'.format(current_mem_configuration_type))

        print('Average end-to-end response time: {}'.format(current_avg_rt))
        print('Average Cost: {}'.format(current_cost))
        print('PRCP_BPBC Optimization Completed.')
        return (current_avg_rt, current_cost, current_mem_configuration_type, current_mem_configuration, iterations_count, target_changes)