import React, { useState,useEffect } from 'react';
import axios from 'axios';

const OptimizationPage = () => {
  const [applicationsOfUser,setApplicationofUser] = useState([]);
  const [applicationsToShow,setApplicationsToShow] = useState([]);
  const [selectedApplication, setSelectedApplication] = useState('');
  const [optimizationResult, setOptimizationResult] = useState(null)
  const [selectedCloudType, setSelectedCloudType] = useState('');
  const [selectedOptimizationType, setSelectedOptimizationType] = useState('');
  const [costConstraint, setCostConstraint] = useState('');
  const [performanceConstraint, setPerformanceConstraint] = useState('');
  const [partOfTCO,setPartOfTCO] = useState('')
  const [optAnim, setOptAnim] = useState(false)
  const [optInfo, setOptInfo] = useState(false)

  const userID = '647ccafb9ffc37a91aaad558'
  const [errorMessage,setErrorMessage] = useState(null)

  //Table Related 
  const [applicationSelectedForHistory,setApplicationSelectedForHistory]= useState(null)
  const [optimizationHistory,setOptimizationHistory] = useState(null)

  const [expandedRows, setExpandedRows] = useState([]);

  const toggleRow = (index) => {
    const currentIndex = expandedRows.indexOf(index);
    if (currentIndex !== -1) {
      setExpandedRows((prevState) => [
        ...prevState.slice(0, currentIndex),
        ...prevState.slice(currentIndex + 1),
      ]);
    } else {
      setExpandedRows((prevState) => [...prevState, index]);
    }
  };
  
  const hideErrorMessage =() =>{
    setErrorMessage(null)
  }
  //Side effects
  useEffect(() => {
    fetchData();
  }, []);

  //use this to update optimzation history
  useEffect(() => {
    console.log("Applications for history",applicationSelectedForHistory);
    const desiredApplication = applicationsOfUser.find((application) => application.id === applicationSelectedForHistory);
    if(desiredApplication && desiredApplication.optimizations){setOptimizationHistory(desiredApplication.optimizations)}else{
      setOptimizationHistory(null)
    }
    console.log('optimizationHistory', optimizationHistory)
  }, [applicationSelectedForHistory]);

  //Get data
  const fetchData = async () =>{
    try {
        const responseOfApplicationsRequest= await axios.get(`http://127.0.0.1:5000/application/user/${userID}`);
        setApplicationofUser(responseOfApplicationsRequest.data.applications) 
    }
    catch (error){
        console.error('Error:', error);
  }
  }

  //styles
  const headerStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '10px',
  };
  const textStyle = {
    fontSize: '16px',
    marginBottom: '20px',
  };
  const ctaContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
  };
  const buttonStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '10px 15px',
    margin: '10px 0',
    backgroundColor: '#349eff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  };
  const messageStyle = {
    position: 'relative',
    backgroundColor: 'red',
    color: 'black',
    padding: '10px',
    borderRadius: '4px',
    marginBottom: '10px',
  };

  const closeButtonStyle = {
    position: 'absolute',
    top: '5px',
    right: '5px',
    fontSize: '25px',
    fontWeight: 'bold',
    color: 'black',
    cursor: 'pointer',
  };
  const inputStyle = {
    marginBottom: '10px',
    marginRight: '10px',
    fontSize:'15px',
    backgroundColor: '#eee',
    border: '1px solid #000',
    padding: '10px',
    borderRadius: '5px',
  };

  //data of sections
  const cloudTypes = [
    { value: 'public', label: 'Public' },
    { value: 'private', label: 'Private' },
    { value: 'hybrid', label: 'Hybrid' },
  ];

  const optimizationTypes = [
    { value: 'cost', label: 'Cost' },
    { value: 'performance', label: 'Performance' },
    { value: 'both', label: 'Both' },
  ];

  const handleCloudTypeChange = (e) => {
    setSelectedCloudType(e.target.value);
    //filter applications to show
    let targetValue=e.target.value;
    let filteredApplications=[];
    if (targetValue === 'public') {
      filteredApplications = applicationsOfUser.filter(application => application.status.includes('Public_deployed'));
    } else if (targetValue === 'private') {
      filteredApplications = applicationsOfUser.filter(application => application.status.includes('Private_deployed'));
    } else if (targetValue==="hybrid"){
      filteredApplications = applicationsOfUser.filter(application => application.status.includes('Private_deployed'));
    }
    setSelectedCloudType(e.target.value);
    setApplicationsToShow(filteredApplications);
  };

  const handleOptimizationTypeChange = (e) => {
    setSelectedOptimizationType(e.target.value);
  };

  const handlePartOfTCO=(e)=>{
    setPartOfTCO(e.target.value)
  }

  const handleOptimize = async() => {
    //Step 1. Prepare request body
    setOptimizationResult(null)
    setOptAnim(true)
    setOptInfo(false)
    const reqbody = {
      cloudType: selectedCloudType,
      optimizationType: selectedOptimizationType,
      costConstraint: selectedOptimizationType == 'cost' ? '': costConstraint,
      performanceConstraint: selectedOptimizationType == 'performance' ? '': performanceConstraint,
      partOfTCO: selectedCloudType == 'public' ? '' : partOfTCO
    };
    // 2. Send Request to API
    try {
      console.log(reqbody)
      console.log('appId-',selectedApplication)
      const startTime = performance.now();

      const response = await axios.put(`http://127.0.0.1:5000/application/optimize/${selectedApplication}`, reqbody);

      const endTime = performance.now();
      const timeTaken = endTime - startTime;
      console.log(`Time taken: ${timeTaken} milliseconds`);
      
      console.log(response.data)
      setOptAnim(false)
      setOptimizationResult(response.data)
      setApplicationSelectedForHistory(applicationSelectedForHistory)
    } catch (error) {
      if(error.response && error.response.data && error.response.data.message){
        setOptInfo(true)
        setOptAnim(false)
        setErrorMessage(error.response.data.message)
      }else{
        setOptInfo(true)
        setOptAnim(false)
        setErrorMessage("Error in the request")
      }
    }

  };

  const renderCloudTypeFields = () => {
    const isHybrid = selectedCloudType === 'hybrid';
  
    return (
      <div>

        {isHybrid || selectedCloudType === 'private' ? (
          <div>
            <input
              type="number"
              style={inputStyle}
              placeholder="Part of TCO in USD"
              value={partOfTCO}
              onChange={handlePartOfTCO}
            />
          </div>
        ) : null}
      </div>
    );
  };  

  const renderOptimizationTypeFields = () => {
    if (selectedOptimizationType === 'performance') {
      return (
        <input
          type="number"
          style={inputStyle}
          placeholder="Cost Constraint in USD"
          value={costConstraint}
          onChange={(e) => setCostConstraint(e.target.value)}
        />
      );
    } else if (selectedOptimizationType === 'cost') {
      return (
        <input
          type="text"
          style={inputStyle}
          placeholder="Time Constraint in ms"
          value={performanceConstraint}
          onChange={(e) => setPerformanceConstraint(e.target.value)}
        />
      );
    } else if (selectedOptimizationType === 'both') {
      return (
        <div>
          <input
            type="number"
            style={inputStyle}
            placeholder="Cost Constraint USD"
            value={costConstraint}
            onChange={(e) => setCostConstraint(e.target.value)}
          />
          <input
            type="number"
            style={inputStyle}
            placeholder="Time Constraint in ms"
            value={performanceConstraint}
            onChange={(e) => setPerformanceConstraint(e.target.value)}
          />
        </div>
      );
    }
    return null;
  };

  const optStyle = `
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 10vh;
  }
  
  .text {
    font-size: 24px;
    color: #349eff;
  }
  @keyframes dot-blink {
    0% { opacity: 0; }
    50% { opacity: 1; }
    100% { opacity: 0; }
  }

  .dot-animation {
    animation: dot-blink 1s infinite;
  }
`;

  return (
    <div>
      <h3 style={headerStyle}>Optimization Page</h3>
      <p style={textStyle}>Select an application and deployment type to begin optimization.</p>

      {false && (
        <div>
          <h4>Informations</h4>
          <p>You can select platform which you going to deploy, in public or private only or in hybrid manner.</p>
          <p>You can select an application which you deployed earlier.</p>
          <p>When you select optimization type you want to consider this.</p>
          <p style={{marginLeft: 50}}>          When you select cost optimization, you want to add time constraint.</p>
          <p style={{marginLeft: 50}}>          When you select performance optimization, you want to add cost constraint.</p>
          <p style={{marginLeft: 50, marginBottom: 30}}>          When you select both, you want to add both constraints.</p>
        </div>
      )}
 
      {errorMessage && (
          <div style={messageStyle}>
            {errorMessage}
            <span style={closeButtonStyle} onClick={hideErrorMessage}>
                  &times;
                </span>
              </div>
      )}
      
      <div style={ctaContainerStyle}>
        <select
          style={inputStyle}
          value={selectedCloudType}
          onChange={handleCloudTypeChange}
        >
          <option value="">Select Platform</option>
          {cloudTypes.map((cloudType) => (
            <option key={cloudType.value} value={cloudType.value}>
              {cloudType.label}
            </option>
          ))}
        </select>

        <select
          style={inputStyle}
          value={selectedApplication}
          onChange={(e) => setSelectedApplication(e.target.value)}
        >
          <option value="">Select Application</option>
          {applicationsToShow.map((item) => (
            <option key={item.id} value={item.id}>
              {item.applicationName}
            </option>
          ))}
        </select>

        <select
          style={inputStyle}
          value={selectedOptimizationType}
          onChange={handleOptimizationTypeChange}
        >
          <option value="">Select Optimization Type</option>
          {optimizationTypes.map((optimizationType) => (
            <option key={optimizationType.value} value={optimizationType.value}>
              {optimizationType.label}
            </option>
          ))}
        </select>
        <button onClick={handleOptimize} style={{...buttonStyle,marginTop:0,fontSize:'16px'}}>
          Optimize
        </button>
      </div>
      <div style={ctaContainerStyle}>
        {renderCloudTypeFields()}
        {renderOptimizationTypeFields()}
      </div>
      { optAnim &&
        <div className="container">
          <div style={{ fontSize: '24px', color: '#349eff' }}>
            Optimizing<span className="dot-animation">...</span>
            <style>{optStyle}</style>
          </div>
        </div>
      }
      {optimizationResult && 
      <div style={{ backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)', padding: '16px'}}>
        <div style={{ display: 'flex', justifyContent: 'center', margin: '10px 0' }}>
          <h4>Optimized Results</h4>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', margin: '10px 0' }}>
          <table style={{ borderCollapse: 'collapse', width: '50%', backgroundColor: '#f2f2f2', border: '0.5px solid #ccc' }}>
            <thead>
              <tr style={{ backgroundColor: '#e6e6e6' }}>
                <th style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>Cost Constraint</th>
                <th style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>Achieved Cost</th>
                <th style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>Performance Constraint</th>
                <th style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>Achieved Performance</th>
                <th style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>Memory Configurations</th>
              </tr>
            </thead>
            <tbody>
              <tr>
              <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {optimizationResult['cost_const'] || 'N/A'}
                </td>
                <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {optimizationResult['Achived_cost'] || 'N/A'}
                </td>
                <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {optimizationResult['perf_const'] || 'N/A'}
                </td>
                <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {optimizationResult['Achived_rt'] || 'N/A'}
                </td>
                <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                  <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                    <tbody>
                      <tr>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['MemoryOfFunctions'][1]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['MemoryOfFunctions'][2]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['MemoryOfFunctions'][3]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['MemoryOfFunctions'][4]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['MemoryOfFunctions'][5]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['MemoryOfFunctions'][6]}
                        </td>
                      </tr>
                      <tr>
                      <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['CloudTypeOfFunctions'][1]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['CloudTypeOfFunctions'][2]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['CloudTypeOfFunctions'][3]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['CloudTypeOfFunctions'][4]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['CloudTypeOfFunctions'][5]}
                        </td>
                        <td style={{ color: '#333', padding: '8px', border: '1px solid #ccc' }}>
                          {optimizationResult['CloudTypeOfFunctions'][6]}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </div>
      }

      <h3 style={{...headerStyle, marginTop: 20}}>History</h3>
        <select
            style={{...buttonStyle}}
            value={applicationSelectedForHistory}
            onChange={(e) => setApplicationSelectedForHistory(e.target.value)}
          >
            <option value="">Select App</option>
            {applicationsOfUser.map((item) => (
              <option key={item.id} value={item.id}>
                {item.applicationName}
              </option>
            ))}
        </select>
      <p style={textStyle}>You can get the Optimal configuration for your application deployment here.</p>
      <div style={{ backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)', padding: '16px'}}>
     {optimizationHistory ?
      <table style={{ borderCollapse: 'collapse', width: '100%'}}>
      <thead>
        <tr>
          <th style={{ backgroundColor: '#349eff', color: '#fff',borderTopLeftRadius:'8px' }}>Optimization Type</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff'}}>Cloud Type</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff' }}>Cost Constraint</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff' }}>Performance Constraint</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff' }}>TCO</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff' }}>Achieved Cost</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff' }}>Achieved Performance</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff'}}>State</th>
          <th style={{ backgroundColor: '#349eff', color: '#fff',borderTopRightRadius:'8px' }}>Expand/Minimize</th>
        </tr>
      </thead>
      <tbody>
        {optimizationHistory.map((item, index) => (
          <React.Fragment key={index}>
            <tr style={{backgroundColor:'white',border:0, width:0}}>
              <td style={{ color: 'black' }}>{item.optimizationType}</td>
              <td style={{ color: 'black' }}>{item.cloudType}</td>
              <td style={{ color: 'black' }}>{item.costConstraint || 'N/A'}</td>
              <td style={{ color: 'black' }}>{item.performaceConstraint || 'N/A'}</td>
              <td style={{ color: 'black' }}>{item.TCO || 'N/A'}</td>
              <td style={{ color: 'black' }}>{item.achivedCost || 'N/A'}</td>
              <td style={{ color: 'black' }}>{item.achivedPerformace || 'N/A'}</td>
              <td style={{ color: 'black' }}><button style={{...buttonStyle,backgroundColor: item.state === 'current' ? 'green' : 'red'}}>{item.state}</button></td>
              <td>
                <button
                  onClick={() => toggleRow(index)}
                  style={buttonStyle}
                >
                  {expandedRows.includes(index) ? 'Minimize' : 'Expand'}
                </button>
              </td>
            </tr>
            {expandedRows.includes(index) && (
              <tr style={{backgroundColor:'white'}}>
                <td colSpan="7">
                  <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                    <thead>
                      <tr>
                        <th style={{ backgroundColor: '#349eff', color: '#fff' }}  >Function Name</th>
                        <th style={{ backgroundColor: '#349eff', color: '#fff' }} >Cloud</th>
                        <th style={{ backgroundColor: '#349eff', color: '#fff' }} >Provider</th>
                        <th style={{ backgroundColor: '#349eff', color: '#fff' }} >Memory</th>
                      </tr>
                    </thead>
                    <tbody>
                      {item.memoryConfigurations.map((memoryConfig, subIndex) => (
                        <tr key={subIndex} style={{backgroundColor:'white',border:0}}>
                          <td style={{ color: 'black' }}>{memoryConfig.functionName}</td>
                          <td style={{ color: 'black' }}>{memoryConfig.cloud}</td>
                          <td style={{ color: 'black' }}>{memoryConfig.provider}</td>
                          <td style={{ color: 'black' }}>{memoryConfig.mem}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </td>
              </tr>
            )}
          </React.Fragment>
        ))}
      </tbody>
    </table> : <div>Select the application</div>}
    </div>
    </div>
  );
};

export default OptimizationPage;
