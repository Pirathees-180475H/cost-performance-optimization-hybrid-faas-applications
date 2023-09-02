import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useHistory, link } from 'react-router-dom';

const emptyApplication = {
  applicationName: '',
  applicationLocation: '',
  functionsCount: '',
  functions: [],
  edges: []
};

const newFunction = {
  functionName: '',
  functionShortName: '',
  functionType: ''
};

const AddApplicationPage = ({location}) => {

  let backUpApplication=null;
  if(location && location.state && location.state['application']){
     backUpApplication=location.state['application']
  }
  
  const history = useHistory(); // Move the useHistory hook here
  const [application, setApplication] = useState(backUpApplication ? backUpApplication:emptyApplication);
  const [newFunctionData, setNewFunctionData] = useState(newFunction);
  const [message, setMessage] = useState(null);
  const [validityMessage,setValidityMessage]= useState(null)
  let userId="647ccafb9ffc37a91aaad558"; 

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setApplication((prevApplication) => ({
      ...prevApplication,
      [name]: value
    }));
  };

  const handleNewFunctionChange = (e) => {
    const { name, value } = e.target;
    setNewFunctionData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleAddFunction = async() => {

    if (newFunctionData.functionName && newFunctionData.functionShortName && newFunctionData.functionType) {
      setApplication((prevApplication) => ({
        ...prevApplication,
        functions: [...prevApplication.functions, newFunctionData]
      }));
      setNewFunctionData(newFunction);
    } else {
      setMessage('Please fill in function details')
    }

    //Handle application Name validation
    if(!application.applicationName || !application.applicationLocation || !application.functionsCount){
      setMessage('Please fill in Application details')
    }

  };

  const hideMessage=()=>{
    setMessage(null);
  }

  const hideValidityMessage=()=>{
    setValidityMessage(null)
  }

  const handleDeleteFunction = (index) => {
    const updatedFunctions = [...application.functions];
    updatedFunctions.splice(index, 1); // Remove the function at the specified index
    setApplication({ ...application, functions: updatedFunctions });
  };

  //Handle Validity Request
  const handleValidityRequest= async()=>{
    try {
      const response = await axios.post(`http://127.0.0.1:5000/application/validate/${userId}`, application);
      if(response.data!="valid"){
        setValidityMessage(response.data)
      }else{
        setValidityMessage(null)
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  const handleFormSubmit = (e) => {
    e.preventDefault();
    // Perform form submission or other actions
    console.log(application);
  };

  //Styles
  const inputStyle = {
    width: '100%',
    padding: '8px',
    marginBottom: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
  };

  const labelStyle = {
    fontWeight: 'bold',
    marginBottom: '5px',
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

  const buttonStyle = {
    padding: '10px 20px',
    margin: '5px',
    backgroundColor: '#349eff',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
      <div style={{ width: '700px' }}>
        <h2 style={{ marginBottom: '10px', textAlign: 'center' , color:'#349eff' }}>ADD APPLICATION</h2>
        <form onSubmit={handleFormSubmit}>
          <div>
            <label htmlFor="applicationName" style={labelStyle}>Application Name:</label>
            <input
              type="text"
              id="applicationName"
              name="applicationName"
              value={application.applicationName}
              onChange={handleInputChange}
              required
              style={inputStyle}
            />
          </div>
          <div>
            <label htmlFor="applicationLocation" style={labelStyle}>Application Location:</label>
            <input
              type="text"
              id="applicationLocation"
              name="applicationLocation"
              value={application.applicationLocation}
              onChange={handleInputChange}
              required
              style={inputStyle}
            />
          </div>
          <div>
            <label htmlFor="functionsCount" style={labelStyle}>Functions Count:</label>
            <input
              type="number"
              id="functionsCount"
              name="functionsCount"
              value={application.functionsCount}
              onChange={handleInputChange}
              required
              style={inputStyle}
            />
          </div>

           
          {message && (
          <div style={messageStyle}>
            {message}
            <span style={closeButtonStyle} onClick={hideMessage}>
                  &times;
                </span>
              </div>
            )}
            

          <h3 style={{marginTop:'10px',marginBottom:'10px',color:"#349eff"}}>Add Functions</h3>
          <div>
            <label htmlFor="functionName" style={labelStyle}>Function Name:</label>
            <input
              type="text"
              id="functionName"
              name="functionName"
              value={newFunctionData.functionName}
              onChange={handleNewFunctionChange}
              required
              style={inputStyle}
            />
          </div>
          
          <div>
            <label htmlFor="functionShortName" style={labelStyle}>Function Short Name:</label>
            <select
              id="functionShortName"
              name="functionShortName"
              value={newFunctionData.functionShortName}
              onChange={handleNewFunctionChange}
              required
              style={inputStyle}
            >
              <option value="">Select Function Short Name</option>
              {Array.from({ length: Number(application.functionsCount) }, (_, i) => i + 1).map((num) => (
                <option key={num} value={`f${num}`}>{`f${num}`}</option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="functionType" style={labelStyle}>Function Type:</label>
            <select
              id="functionType"
              name="functionType"
              value={newFunctionData.functionType}
              onChange={handleNewFunctionChange}
              required
              style={inputStyle}
            >
              <option value="">Select Function Type</option>
              <option value="CPU">CPU</option>
              <option value="Network">Network</option>
              <option value="Disk">Disk</option>
            </select>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <button type="button" style={buttonStyle} onClick={handleAddFunction}>Add Function</button>
            <button type="button" style={{ ...buttonStyle, background: 'red' }} onClick={handleValidityRequest}>Validate</button>
          </div>

          {validityMessage && (
          <div style={messageStyle}>
            {validityMessage}
            <span style={closeButtonStyle} onClick={hideValidityMessage}>
                  &times;
                </span>
              </div>
            )}
            
         
          <h3 style={{marginBottom:'5px'}}>Functions</h3>
          {application.functions.length > 0 ? (

            <table style={{ borderCollapse: 'collapse', marginTop: '20px', width: '100%' }}>
              <thead>
                <tr>
                  <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' ,borderTopLeftRadius:'10px'}}>Function Name</th>
                  <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Function Short Name</th>
                  <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px'}}>Function Type</th>
                  <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px',borderTopRightRadius:'10px'}}>Remove Function</th>

                </tr>
              </thead>
              <tbody>
                {application.functions.map((func, index) => (
                  <tr key={index}>
                    <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{func.functionName}</td>
                    <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{func.functionShortName}</td>
                    <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{func.functionType}</td>
                    <td style={{ border: '1px solid #ddd', padding: '10px'}}>
                      <button style={{...buttonStyle,marginLeft:'15px',background:'red'}} onClick={() => handleDeleteFunction(index)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

          ) : (
            <p style={{color:'red'}}>No functions added.</p>
          )}

          {application.functions.length > 0 ? (
                  <button onClick={() => history.push('/edit_graph', {application})} style={buttonStyle}>
                    Configure Workflow
                  </button>
                ) : (
                  null
          )}
        </form>
      </div>
    </div>
  );
};

export default AddApplicationPage;
