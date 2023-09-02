from models.BCPC import PerfOpt as BCPC_perfOpt
from models.BPBC import PerfOpt as BPBC_PerfOpt
from models.CPC  import PerfOpt as CPC_PerfOpt
from models.AppWorkFlow import ServerlessAppWorkflow
import networkx as nx
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
from pymongo import MongoClient
import itertools
import warnings
from flask import request, jsonify
warnings.filterwarnings("ignore")

def modelsMain(app_id,request):
    try:
        # print('App_id',app_id)
        data = request.json
        # print('data', data)

        # print('Stage 1')


        client = MongoClient('mongodb://localhost:27017/')  
        db = client['cloudPerformace']  
        userCollection = db['users'] 
        applicationCollection=db['applications']
        application = applicationCollection.find_one({'_id': ObjectId(app_id)})
        optimizations = application.get('optimizations')
        # # print('application', application)

        functionList = application['functions']
        nodes = []
        nodes_names = []
        performance_profile = {}

        for function in functionList:
            nameF = function['functionShortName']
            nodes_names.append(nameF)
            fn_no = int(nameF.split('f')[1])
            nodes.append(fn_no)
            
            responseTimes = function['responseTimes']
            # # print(responseTimes)
            times = {'public': {}, 'private': {}}
            for res in responseTimes:
                if res['cloudType'] == 'public':
                    res_p = res['rts']
                    converted_data_public = {d["mem"]: d["rt"] for d in res_p}
                else:
                    res_p = res['rts']
                    converted_data_private = {d["mem"]: d["rt"] for d in res_p}
            times['private'] = converted_data_private
            times['public'] = converted_data_public
            performance_profile[nameF] = times

        # # print('performance_profile', performance_profile)

        edges_data = application['edges']
        edges = [(x[0], x[1], x[2]) for x in edges_data]
        # print('edges', edges)

        cost_c = 0
        performance_c = 0
        TCO = 0
        if data['performanceConstraint'] == '':
            performance_c = 0
        else:
            performance_c = float(data['performanceConstraint'])
        
        if data['costConstraint'] == '':
            cost_c = 0
        else:
            cost_c = float(data['costConstraint'])

        cloud_type = data['cloudType']
        optimization_type = data['optimizationType']

        TCO =0
        if data['partOfTCO'] == '':
            TCO = 0
        else:
            TCO = float(data['partOfTCO'])

        App6_G = nx.DiGraph()

        # App without positions
        App6_G.add_node('Start')
        for node in nodes:
            App6_G.add_node(node)
        App6_G.add_node('End')

        # Define edges and the transition probability
        # AppWorkflow_G.add_weighted_edges_from([$start from, $end at, $transition probability])
        App6_G.add_weighted_edges_from(edges)
        App6_G.add_weighted_edges_from(
            [
                ('Start', 1, 1),
                (6, 'End', 1)
            ]
        )

        # Show the workflow graph
        # pos_App6_G = nx.get_node_attributes(App6_G, 'pos')
        pos = nx.circular_layout(App6_G)
        nx.draw(App6_G, pos=pos, with_labels=True)
        labels_App6_G = nx.get_edge_attributes(App6_G, 'weight')
        nx.draw_networkx_edge_labels(App6_G, pos, edge_labels=labels_App6_G)
        pos_higher_offset_App6_G = {}
        for k, v in pos.items():
            pos_higher_offset_App6_G[k] = (v[0], v[1] + 0.15)
        # plt.show()

        for node in nodes:
            node_name = 'f' + str(node)
            App6_G.nodes[node]['private_perf_profile'] = performance_profile[node_name]['private']
            App6_G.nodes[node]['public_perf_profile'] = performance_profile[node_name]['public']





        # print('Stage 2')

        # TCO = 200
        App = ServerlessAppWorkflow(
            G=App6_G.copy(), TCO=TCO)  # need to Change Delay Type

        optimizer_1 = BCPC_perfOpt(App)
        private_minimal_avg_rt, private_maximal_avg_rt, public_minimal_avg_rt, public_maximal_avg_rt = optimizer_1.get_optimization_boundary()
        # print('perf_boundries', private_minimal_avg_rt, private_maximal_avg_rt, public_minimal_avg_rt, public_maximal_avg_rt)

        optimizer_2 = BPBC_PerfOpt(App)
        private_minimal_cost, private_maximal_cost, public_minimal_cost, public_maximal_cost = optimizer_2.get_optimization_boundary()
        # print('cost_boundries', private_minimal_cost, private_maximal_cost, public_minimal_cost, public_maximal_cost)

        optimizer_3 = CPC_PerfOpt(App)

        # Performance constraint is 6400 ms

        # print('Stage 3')

        # const_list = [3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000, 16500, 17000, 17500, 18000, 18500, 19000, 19500, 20000, 20500, 21000, 21500, 22000, 22500, 23000, 23500, 24000, 24500, 25000]

        # data_temp = {}
        # for cons in const_list:
        #     data_temp[cons] = {}
        #     data_temp[cons]['mem'] = cons
        #     # print(data_temp)
        #     publicAns = optimizer_1.PrerformanceConstraintModel(cons, 'public')
        #     # print('publicAns', publicAns)
        #     data_temp[cons]['public'] = publicAns['Achived_cost']
        #     hybridAns = optimizer_1.PrerformanceConstraintModel(cons, 'hybrid')
        #     # print('hybridAns', hybridAns)
        #     data_temp[cons]['hybrid'] = hybridAns['Achived_cost']
        # print(data_temp)

        # print('stage 4')


        new_optmizations = {}

        if(optimization_type =='cost'):
            new_optmizations['optimizationType'] = 'cost'
            if (cloud_type=='public'):
                
                if(performance_c > public_minimal_avg_rt and performance_c <public_maximal_avg_rt ):
                    configuration_after_optimization = optimizer_1.PrerformanceConstraintModel(performance_c, cloud_type)
                    # print(configuration_after_optimization)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("RT constraint must be between "+str(public_minimal_avg_rt)+" and "+str(public_maximal_avg_rt))
            elif (cloud_type=='private'):
                
                if(performance_c > private_minimal_avg_rt and performance_c < private_maximal_avg_rt ):
                    configuration_after_optimization = optimizer_1.PrerformanceConstraintModel(performance_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("RT constraint must be between "+str(private_minimal_avg_rt)+" and "+str(private_maximal_avg_rt))
            else:
                
                if(performance_c > public_minimal_avg_rt and performance_c < private_maximal_avg_rt ):
                    configuration_after_optimization = optimizer_1.PrerformanceConstraintModel(performance_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("RT constraint must be between "+str(public_minimal_avg_rt)+" and "+str(private_maximal_avg_rt))


        if(optimization_type =='performance'):
            new_optmizations['optimizationType'] = 'performance'
            if (cloud_type=='public'):
                
                if(cost_c > public_minimal_cost and cost_c <public_maximal_cost ):
                    configuration_after_optimization = optimizer_2.CostConstraintModel(cost_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("Cost constraint must be between "+str(public_minimal_cost)+" and "+str(public_maximal_cost))
            elif (cloud_type=='private'):
                
                if(cost_c > private_minimal_cost and cost_c < private_maximal_cost ):
                    configuration_after_optimization = optimizer_2.CostConstraintModel(cost_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("Cost constraint must be between "+str(private_minimal_cost)+" and "+str(private_maximal_cost))
            else:
                
                if(cost_c > private_minimal_cost and cost_c < public_maximal_cost ):
                    configuration_after_optimization = optimizer_2.CostConstraintModel(cost_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("Cost constraint must be between "+str(private_minimal_cost)+" and "+str(public_maximal_cost))

        if(optimization_type =='both'):
            new_optmizations['optimizationType'] = 'cost&performace'
            if (cloud_type=='public'):
                
                if(cost_c > public_minimal_cost and cost_c <public_maximal_cost and performance_c > public_minimal_avg_rt and performance_c <public_maximal_avg_rt):
                    configuration_after_optimization = optimizer_3.Cost_Performance_ConstraintModel(performance_c,cost_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("RT constraint must be between "+str(public_minimal_avg_rt)+" and "+str(public_maximal_avg_rt)+ "and Cost constraint must be between "+str(public_minimal_cost)+" and "+str(public_maximal_cost))
            elif (cloud_type=='private'):
                
                if(cost_c > private_minimal_cost and cost_c < private_maximal_cost and performance_c > private_minimal_avg_rt and performance_c < private_maximal_avg_rt  ):
                    configuration_after_optimization = optimizer_3.Cost_Performance_ConstraintModel(performance_c, cost_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("RT constraint must be between "+str(private_minimal_avg_rt)+" and "+str(private_maximal_avg_rt)+ " and Cost constraint must be between "+str(private_minimal_cost)+" and "+str(private_maximal_cost))
            else:
                
                if(cost_c > private_minimal_cost and cost_c < public_maximal_cost and performance_c > public_minimal_avg_rt and performance_c < private_maximal_avg_rt ):
                    configuration_after_optimization = optimizer_3.Cost_Performance_ConstraintModel(performance_c, cost_c, cloud_type)
                    # return configuration_after_optimization
                else:
                    raise ValueError ("RT constraint must be between "+str(public_minimal_avg_rt)+" and "+str(private_maximal_avg_rt)+ " and Cost constraint must be between "+str(private_minimal_cost)+" and "+str(public_maximal_cost))
        
        new_optmizations['state'] = 'current'
        new_optmizations['achivedCost'] = str(configuration_after_optimization['Achived_cost']) + 'USD'
        new_optmizations['achivedPerformace'] = configuration_after_optimization['Achived_rt']
        new_optmizations['performaceConstraint'] = performance_c
        new_optmizations['costConstraint'] = str(cost_c) + 'USD'

        memoryConfigurations = []
        for node in nodes:    
            provider = ''
            if configuration_after_optimization['CloudTypeOfFunctions'][node] == 'public':
                provider = 'Lambda'
            else:
                provider = 'openFaaS'
            func = {
                    "functionName" : "function" + str(node),
                    "cloud" : configuration_after_optimization['CloudTypeOfFunctions'][node],
                    "provider" : provider,
                    "mem" : configuration_after_optimization['MemoryOfFunctions'][node]
                }
            memoryConfigurations.append(func)

        new_optmizations['memoryConfigurations'] = memoryConfigurations
        new_optmizations['TCO'] = str(TCO) + 'USD'
        new_optmizations['cloudType'] = cloud_type

        # print()
        # print()
        # print('optimizations BEFORE', optimizations)
        optimizations.append(new_optmizations)
        # print()
        # print()
        # print('optimizations after', optimizations)

        application['optimizations'] = optimizations

        applicationCollection.update_one({'_id': ObjectId(app_id)}, {'$set': application})

        print('Stage 4')
        return configuration_after_optimization

    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400