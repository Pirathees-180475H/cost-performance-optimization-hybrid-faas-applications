import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Table from '../components/table/Table';
import DefinedGraph from '../pages/DefinedGraph'; // Import the DefinedGraph component
import axios from 'axios';

const AppPage = () => {
  const { applicationId } = useParams();
  const [application,setApplication]=useState({});
  const [showGraph, setShowGraph] = useState(false);
  const [functionsList,setFunctionList] = useState([]);
  const [functionNodes,setFunctionNodes]=useState([]);
  const [functionEdges,setFunctionEdges] =useState([]);

  //For RT
  const [showRT,setShowRT] = useState(false);
  const [RTList,setRTList] =useState([]);

  useEffect(() => {
    fetchData()
  }, []);

  useEffect(() => {
    console.log(functionsList);
    console.log('RTS-',RTList)
  }, [functionsList,RTList]); // Checking Purpose


  const fetchData = async () =>{
    try {
        const responseOfApplicationRequest= await axios.get(`http://127.0.0.1:5000/application/${applicationId}`);
        setApplication(responseOfApplicationRequest.data.application)
        setFunctionList(responseOfApplicationRequest.data.application.functions)
        //set up nodes and edges
        const originalList=responseOfApplicationRequest.data.application.edges
        const allNodes = []; const allLinks = [];
        for (let i = 0; i < originalList.length; i++) {
          for (let j = 0; j < 2; j++) {
            const nodeId = originalList[i][j].toString();
            
            // Check if node exists in allNodes, if not, create a new node
            if (!allNodes.find(node => node.id === nodeId)) {
              allNodes.push({ id: nodeId, x: (Number(nodeId) * 100), y: 100 });
            }
          }
          const [source, target, weight] = originalList[i];
          allLinks.push({ source: source.toString(), target: target.toString(), weight });
        }
        setFunctionNodes(allNodes);
        setFunctionEdges(allLinks);
        //end of nodes setting


        let functions=responseOfApplicationRequest.data.application.functions;
        let Rts=[]

        functions.forEach((fn)=>{
          if(fn.responseTimes){
            let rt={'function':fn.functionName}
            fn.responseTimes.forEach((r)=>{
              rt.cloud=r.cloudType; rt.provider=r.provider;
              if(r.rts){
                r.rts.forEach((t)=>{
                  rt.memory=t.mem; rt.responseTime=t.rt;
                })
              }
            })
            if(rt.cloud && rt.provider && rt.memory && rt.responseTime){ Rts.push(rt);}
          }
        })

        setRTList(Rts);

    }
    catch (error){
        console.error('Error:', error);
    }
 } 

  const functionTableHead = [
    'Function Name',
    'Function short name',
    'Type of the function',
  ];

  const RTTableHead = [
    'Function',
    'Cloud',
    'Provider',
    'Memory',
    'Average Response Time'
  ];

  const handleShowGraphClick = () => {
    setShowGraph(!showGraph);
  };

  const handleShowRT =() =>{
    setShowRT(!showRT);
  }

  return (
    <div>
      <h2 className="page-header">Functions of {application.applicationName}</h2>
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card__body">
              {functionsList.length > 0 ? (
                <Table
                  limit="10"
                  headData={functionTableHead}
                  renderHead={(item, index) => <th key={index}>{item}</th>}
                  bodyData={functionsList}
                  renderBody={(item, index) => (
                    <tr key={index}>
                      <td>{item.functionName}</td>
                      <td>{item.functionShortName}</td>
                      <td>{item.functionType}</td>
                    </tr>
                  )}
                />
              ) : (
                <p>No functions found.</p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div style={{ textAlign: 'right' }}>
      <button
          style={{
            backgroundColor: '#349eff',
            color: '#ffffff',
            marginRight: '10px',
            padding: '8px 16px',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: 'pointer',
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
          }}
          onClick={handleShowGraphClick}
        >
          {showGraph ? 'Hide Workflow' : 'View Workflow'}
        </button>

        <button
          style={{
            backgroundColor: 'green',
            color: '#ffffff',
            marginRight: '10px',
            padding: '8px 16px',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: 'pointer',
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
          }}
          onClick={handleShowRT}
        >
          {showRT ? 'Hide RT' : 'View RT'}
        </button>

      </div>
      {showGraph && (
        <DefinedGraph nodes={functionNodes} links={functionEdges} pageFrom={'appPage'} />
      )}

      {showRT ?
      <div>
        <h2 className="page-header">Performances(Runtimes)</h2>
          <div className="row">
                  <div className="col-12">
                    <div className="card">
                      <div className="card__body">
                        {RTList.length > 0 ? (
                          <Table
                            limit="10"
                            headData={RTTableHead}
                            renderHead={(item, index) => <th key={index}>{item}</th>}
                            bodyData={RTList}
                            renderBody={(item, index) => (
                              <tr key={index}>
                                <td>{item.function}</td>
                                <td>{item.cloud}</td>
                                <td>{item.provider}</td>
                                <td>{item.memory}</td>
                                <td>{item.responseTime}</td>

                              </tr>
                            )}
                          />
                        ) : (
                          <p>No Runtimes found!.</p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
      </div> : null}
      
    </div>

  );
};

export default AppPage;