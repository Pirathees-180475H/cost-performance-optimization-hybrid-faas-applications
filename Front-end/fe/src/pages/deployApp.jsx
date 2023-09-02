import React from 'react';
import { useEffect, useState } from 'react'
import axios from 'axios';

const DeploymentPage = () => {
  const [applicationsOfUser,setApplicationsOfUser] = useState([]);
  const [selectedApplicationId, setSelectedApplicationId] = useState('');
  const [selectedCloudType, setSelectedCloudType] = useState('');
  const userID = '647ccafb9ffc37a91aaad558'
  const [deploymentProgress, setDeploymentProgress] = useState([]);
  const [feedbackList, setFeedbackList] = useState([]);
  const [invocations,setInvocations] = useState(5)
  const [publicStepSize,setPublicStepSize] = useState(128);
  const [privateStepSize,setPrivateStepSize] = useState(128);
  const [publicMemoryList, setPublicMemoryList] = useState({
    upperLimit: '',
    lowerLimit: '',
  });

  const [privateMemoryList, setPrivateMemoryList] = useState({
    upperLimit: '',
    lowerLimit: '',
  });

  const [errorMessage,setErrorMessage] = useState(null);

  const hideErrorMessage =()=>{
    setErrorMessage(null);
  }

  useEffect(() => {
    fetchData();
  }, []);

  //Get Application data
  const fetchData = async () =>{
    try {
        const responseOfApplicationsRequest= await axios.get(`http://127.0.0.1:5000/application/user/${userID}`);
        setApplicationsOfUser(responseOfApplicationsRequest.data.applications) 
    }
    catch (error){
        console.error('Error:', error);
    }
  } 

  const handlepublicCloudStepSize=(e) =>{
    setPublicStepSize(e.target.value)
  }

  const handleprivateCloudStepSize =(e) =>{
    setPrivateStepSize(e.target.value)
  }

  const handleDeploy =async() => {
    //Set alerts before starts deployment
    if(!selectedApplicationId) {setErrorMessage("Please select application")}
    if(!selectedCloudType) {setErrorMessage("Please Select Cloud Platform")}
    if(selectedCloudType=='public' &&(!publicMemoryList.lowerLimit || !publicMemoryList.upperLimit || !publicStepSize)){setErrorMessage("Please public set memory config")}
    if(selectedCloudType=='private' &&(!privateMemoryList.lowerLimit || !privateMemoryList.upperLimit || !privateStepSize)){setErrorMessage("Please set private memory config")}
    if(selectedCloudType=='hybrid' &&(!publicMemoryList.lowerLimit || !publicMemoryList.upperLimit || !publicStepSize||!privateMemoryList.lowerLimit || !privateMemoryList.upperLimit || !privateStepSize)){setErrorMessage("Please set hybrid memory config")}

    // Clear previous feedback and progress
    setFeedbackList([]);
    setDeploymentProgress(["Deployment Started"]);

    // Start spinner
    const interval = setInterval(() => {}, 1000);

    //Deploy in public cloud
    if(selectedCloudType=='public'){
      setDeploymentProgress(["Public Deployment started"]);
      try {
        const response = await axios.post(`http://127.0.0.1:5000/application/deploy/public/${selectedApplicationId}`, {});
      } catch (error) {
        if(error.response && error.response.data && error.response.data.message){setErrorMessage(error.response.data.message)}
      }
      setDeploymentProgress(["Public Deployment finished"])
    }

    //Deploy in private cloud
    if(selectedCloudType=='private'){
      setDeploymentProgress(["Private Deployment started"]);
      try {
        const response = await axios.post(`http://127.0.0.1:5000/application/deploy/private/${selectedApplicationId}`, {});
      } catch (error) {
        if(error.response && error.response.data && error.response.data.message){setErrorMessage(error.response.data.message)}
      }
      setDeploymentProgress(["Private Deployment finished"]);
    }

    //Deploy in hybrid cloud
    if(selectedCloudType=='hybrid'){
      setDeploymentProgress(["Hybrid Deployment started"]);
      try {
        const response = await axios.post(`http://127.0.0.1:5000/application/deploy/hybrid/${selectedApplicationId}`, {});
      } catch (error) {
        if(error.response && error.response.data && error.response.data.message){setErrorMessage(error.response.data.message)}
      }
      setDeploymentProgress(["Hybrid Deployment finished"]);
    }

    //Start Invocations
    setDeploymentProgress(["Invocation Started"]);

    //Invocation in Public cloud
    if(selectedCloudType=='public'){
      //setUp public request body
      let upper=parseInt(publicMemoryList.upperLimit) ; let lower=parseInt(publicMemoryList.lowerLimit) ; let currentMem=lower;let publicMems=[] ;   
      if (lower <= upper && parseInt(publicStepSize) > 0) {
        while (currentMem <= upper) {
          publicMems.push(currentMem);
          currentMem += publicStepSize;
        }
      }
      setDeploymentProgress(["Public Invocation started"]);
      try {
        const response = await axios.put(`http://127.0.0.1:5000/application/invoke/public/${selectedApplicationId}`, {
          'publicMemList':publicMems,
          'invocationCount':invocations
        });
      } catch (error) {
        if(error.response && error.response.data && error.response.data.message){setErrorMessage(error.response.data.message)}
      }
      setDeploymentProgress(["Public Invocation completed"]);
    }


    if(selectedCloudType =='private'){
      //setUp private request body
      let upper=parseInt(privateMemoryList.upperLimit) ; let lower=parseInt(privateMemoryList.lowerLimit) ; let currentMem=lower;let privateMems=[] ;   
      if (lower <= upper && parseInt(privateStepSize) > 0) {
        while (currentMem <= upper) {
          privateMems.push(currentMem);
          currentMem += publicStepSize;
        }
      }
      setDeploymentProgress(["Private Invocation started"]);
      try {
        const response = await axios.put(`http://127.0.0.1:5000/application/invoke/private/${selectedApplicationId}`, {
          'privateMemList':privateMems,
          'invocationCount':invocations
        });
      } catch (error) {
        if(error.response && error.response.data && error.response.data.message){setErrorMessage(error.response.data.message)}
      }
      setDeploymentProgress(["Private Invocation completed"]);

    }

    if(selectedCloudType =='hybrid'){
      //setUp public request body
      let upperPub=parseInt(publicMemoryList.upperLimit) ; let lowerPub=parseInt(publicMemoryList.lowerLimit) ; let currentMemPub=lowerPub;let publicMems=[] ;   
      if (lowerPub <= upperPub && parseInt(publicStepSize) > 0) {
        while (currentMemPub <= upperPub) {
          publicMems.push(currentMemPub);
          currentMemPub += publicStepSize;
        }
      }
       //setUp private request body
       let upper=parseInt(privateMemoryList.upperLimit) ; let lower=parseInt(privateMemoryList.lowerLimit) ; let currentMem=lower;let privateMems=[] ;   
       if (lower <= upper && parseInt(privateStepSize) > 0) {
         while (currentMem <= upper) {
           privateMems.push(currentMem);
           currentMem += publicStepSize;
         }
       }
       
       setDeploymentProgress(["Hybrid Invocation started"]);
       try {
         const response = await axios.put(`http://127.0.0.1:5000/application/invoke/hybrid/${selectedApplicationId}`, {
           'publicMemList':publicMems,
           'privateMemList':privateMems,
           'invocationCount':invocations
         });
       } catch (error) {
         if(error.response && error.response.data && error.response.data.message){setErrorMessage(error.response.data.message)}
       }
       setDeploymentProgress(["Hybrid Invocation completed"]);


    }


    // Stop spinner and set end response
    clearInterval(interval);
    setDeploymentProgress([]);

    //Show feedback list after completion of deployment and invocation
    try {
      const response = await axios.get(`http://127.0.0.1:5000/applicationStatus/${selectedApplicationId}`);
      const feedbacks = response.data;
      setFeedbackList([...feedbacks, "Deployment Completed!"]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  

  return (
    <div>
        <h3 style={headerStyle}>Deployment Page</h3>
        <p style={textStyle}>Select an application and deploy type to begin deployment.</p>
        
        {errorMessage && (
            <div style={messageStyle}>
              {errorMessage}
              <span style={closeButtonStyle} onClick={hideErrorMessage}>
                    &times;
                  </span>
                </div>
        )}

      <div style={ctaContainerStyle}>
        <div>
          <select
            style={inputStyle}
            value={selectedApplicationId}
            onChange={(e) => setSelectedApplicationId(e.target.value)}
          >
            <option value="">Select Application</option>
            {applicationsOfUser.map((item) => (
              <option key={item.id} value={item.id}>
                {item.applicationName}
              </option>
            ))}
          </select>

          <select
            style={inputStyle}
            value={selectedCloudType}
            onChange={(e) => setSelectedCloudType(e.target.value)}
          >
            <option value="">Select Deploy Type</option>
            <option value="public">Public</option>
            <option value="private">Private</option>
            <option value="hybrid">Hybrid</option>
          </select>

          <input
            type="number"
            style={inputStyle}
            placeholder="No of Invocation"
            value={invocations}
            onChange={(e) => setInvocations(e.target.value)}
          />
        {selectedCloudType=="public" || selectedCloudType=='hybrid' ? 
        <div>
              <input
                type="number"
                style={inputStyle}
                placeholder="Public Memory Lower Limit"
                value={publicMemoryList.lowerLimit}
                onChange={(e) =>
                  setPublicMemoryList((prevState) => ({
                    ...prevState,
                    lowerLimit: e.target.value,
                  }))
                }
              />

             <input
                type="number"
                style={inputStyle}
                placeholder="Public Memory Upper Limit"
                value={publicMemoryList.upperLimit}
                onChange={(e) =>
                  setPublicMemoryList((prevState) => ({
                    ...prevState,
                    upperLimit: e.target.value,
                  }))
                }
              />
            
              <label htmlFor="stepSizeSelect">Step Size:</label>
                <select
                style={inputStyle}
                value={publicStepSize}
                onChange={handlepublicCloudStepSize}
              >
                <option value={128}>128</option>
                <option value={256}>256</option>
              </select>
        </div> : null}

        {selectedCloudType=='private' || selectedCloudType=='hybrid' ? 
        <div>
              
              <input
                type="number"
                style={inputStyle}
                placeholder="Private Memory Lower Limit"
                value={privateMemoryList.lowerLimit}
                onChange={(e) =>
                  setPrivateMemoryList((prevState) => ({
                    ...prevState,
                    lowerLimit: e.target.value,
                  }))
                }
              />
              <input
                type="number"
                style={inputStyle}
                placeholder="Private Memory Upper Limit"
                value={privateMemoryList.upperLimit}
                onChange={(e) =>
                  setPrivateMemoryList((prevState) => ({
                    ...prevState,
                    upperLimit: e.target.value,
                  }))
                }
              />
              <label htmlFor="stepSizeSelect">Step Size:</label>
              <select
                style={inputStyle}
                value={privateStepSize}
                onChange={handleprivateCloudStepSize}
              >
                <option value={128}>128</option>
                <option value={256}>256</option>
              </select>

        </div> : null}


        <button onClick={handleDeploy} style={buttonStyle}>
          Deploy
        </button>
        </div>

      </div>

      {deploymentProgress.length > 0 && (
        <div style={{ textAlign: 'center' }}>
            <div style={spinnerInnerStyle}>{deploymentProgress}</div>
          <div style={spinnerStyle}>
          </div>
        </div>
      )}

      {feedbackList.length > 0 && (
        <div style={feedbackContainerStyle}>
          <h4>Feedbacks</h4>
          <ul style={feedbackListStyle}>
            {feedbackList.map((feedback, index) => (
              <li key={index} style={feedbackListItemStyle}>{feedback}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};



export default DeploymentPage;


//Styles
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
  flexDirection: 'column',
};


const spinnerSize = 400;


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

const spinnerInnerStyle = {
  position: 'relative',
  fontSize: 28,
  top: 225,
  textAlign: 'center',
  justifyContent: 'center',
  alignItems: 'center',
  color: '#349eff',
  animation: 'none',
};

const feedbackContainerStyle = {
  textAlign: 'center',
  marginTop: '20px',
};

const feedbackListStyle = {
  listStyle: 'none',
  padding: 0,
};

const feedbackListItemStyle = {
  marginBottom: '10px',
  fontSize: '18px',
  color: '#555',
};

const spinnerStyle = {
  width: `${spinnerSize}px`,
  height: `${spinnerSize}px`,
  borderRadius: '50%',
  border: '8px solid #f3f3f3',
  borderTop: '8px solid #349eff',
  animation: 'spin 1s infinite linear',
  position: 'relative',
  margin: '0 auto',
  // marginTop: `calc(50vh - ${spinnerSize / 2}px)`,
};

const inputStyle = {
  marginRight: '10px',
  marginTop: '10px',
  backgroundColor: '#eee',
  border: '1px solid #000',
  padding: '5px',
  borderRadius: '5px',
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