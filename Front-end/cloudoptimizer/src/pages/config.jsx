import React, { useEffect, useState } from 'react';
import axios from 'axios';



const ConfigPage = () => {
  const [isAddConfig,setAddConfig] = useState(false);
  const [existingConfigurations,setExistingConfigurations]=useState()
  const userID = '647ccafb9ffc37a91aaad558'

  const [config, setConfig] = useState({
    cloudType: '',
    publicProvider: '',
    publicAccessKey: '',
    publicSecretKey: '',
    region: '',
    privateProvider: '',
    privateHost: ''
   });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prevConfig) => ({...prevConfig,[name]: value}));
  };

  //Add data to backend
  const handleSubmit = async(e) => {
    e.preventDefault();

    //filter data to submit
    let finalConfig = {};
    if (config.cloudType === 'public') {
      finalConfig = {
        cloudType: config.cloudType,
        publicProvider: config.publicProvider,
        publicAccessKey: config.publicAccessKey,
        publicSecretKey: config.publicSecretKey,
        region: config.region
      };
    } else if (config.cloudType === 'private') {
      finalConfig = {
        cloudType: config.cloudType,
        privateProvider: config.privateProvider,
        privateHost: config.privateHost
      };
    }else if (config.cloudType ==="hybrid"){
      finalConfig=config
    }

    let reqBody=[...existingConfigurations,finalConfig]
    

    try {
      console.log(reqBody)
      const response = await axios.post(`http://127.0.0.1:5000/user/cloudCongif/647ccafb9ffc37a91aaad558`, reqBody);
      console.log("res",response)
    } catch (error) {
      console.error('Error:', error);
    }
 };

  //Get User Data
  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    console.log(existingConfigurations)
  }, [existingConfigurations]);

  const fetchData = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/users/${userID}`);
        setExistingConfigurations(response.data.user.cloudConfig)
    } catch (error) {
        console.error('Error:', error);
    }
  };


  //Styles
  const buttonStyle = {
    padding: '10px 20px',
    margin: '5px',
    backgroundColor: '#349eff',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  };

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

  return (
    <div>
      {isAddConfig ?  (
      <div style={{ marginRight: '500px', marginLeft: '500px', marginTop: '100px' }}>
      <h2 style={{ marginBottom: '10px' }}>Configure details</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="cloudType" style={labelStyle}>Cloud Type:</label>
          <select
            id="cloudType"
            name="cloudType"
            value={config.cloudType}
            onChange={handleChange}
            style={inputStyle}
          >
            <option value="">Select Cloud Type</option>
            <option value="public">Public</option>
            <option value="private">Private</option>
            <option value="hybrid">Hybrid</option>
          </select>
        </div>

        {config.cloudType === 'public' && (
          <>
            <div>
              <label htmlFor="publicProvider" style={labelStyle}>Public Provider:</label>
              <input
                type="text"
                id="publicProvider"
                name="publicProvider"
                value={config.publicProvider}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="publicAccessKey" style={labelStyle}>Public Access Key:</label>
              <input
                type="text"
                id="publicAccessKey"
                name="publicAccessKey"
                value={config.publicAccessKey}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="publicSecretKey" style={labelStyle}>Public Secret Key:</label>
              <input
                type="text"
                id="publicSecretKey"
                name="publicSecretKey"
                value={config.publicSecretKey}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="region" style={labelStyle}>Region:</label>
              <input
                type="text"
                id="region"
                name="region"
                value={config.region}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
          </>
        )}

        {config.cloudType === 'hybrid' && (
          <>
            <div>
              <label htmlFor="publicProvider" style={labelStyle}>Public Provider:</label>
              <input
                type="text"
                id="publicProvider"
                name="publicProvider"
                value={config.publicProvider}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="publicAccessKey" style={labelStyle}>Public Access Key:</label>
              <input
                type="text"
                id="publicAccessKey"
                name="publicAccessKey"
                value={config.publicAccessKey}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="publicSecretKey" style={labelStyle}>Public Secret Key:</label>
              <input
                type="text"
                id="publicSecretKey"
                name="publicSecretKey"
                value={config.publicSecretKey}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="region" style={labelStyle}>Region:</label>
              <input
                type="text"
                id="region"
                name="region"
                value={config.region}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
            <div>
              <label htmlFor="privateProvider" style={labelStyle}>Private Provider:</label>
              <input
                type="text"
                id="privateProvider"
                name="privateProvider"
                value={config.privateProvider}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>

            <div>
              <label htmlFor="Private Host" style={labelStyle}>Private Cloud Host:</label>
              <input
                type="text"
                id="privateHost"
                name="privateHost"
                value={config.privateHost}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
          </>
        )}

        {config.cloudType === 'private' && (
          <>
            <div>
              <label htmlFor="Private Provider" style={labelStyle}>Private Provider:</label>
              <input
                type="text"
                id="privateProvider"
                name="privateProvider"
                value={config.privateProvider}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>

            <div>
              <label htmlFor="Private Host" style={labelStyle}>Private Cloud Host:</label>
              <input
                type="text"
                id="privateHost"
                name="privateHost"
                value={config.privateHost}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
          </>
        )}

        <button  style={buttonStyle} onClick={handleSubmit}> Add New Config</button>

        {/*Navigate*/}
        <button style={buttonStyle}
          onClick={() => setAddConfig(false)}>
          View Configuration
        </button>

      </form>
    </div>) : 
    
    <div  style={{ marginRight: '500px', marginLeft: '10px', marginTop: '20px' }}>
      <h2 style={{ marginBottom: '10px' }}>View Configuration Details</h2>
      
      {existingConfigurations && <div>

      <table style={{ borderCollapse: 'collapse',marginLeft:'15%', marginTop: '20px', width: '100%' }}>
        <thead>
          <tr>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Cloud Type</th>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Provider</th>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Access Key</th>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Secret Key</th>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Region</th>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Private Credentials</th>
            <th style={{ backgroundColor: '#349eff', color: '#fff', padding: '10px' }}>Host</th>
          </tr>
        </thead>
        <tbody>
          {existingConfigurations.map((config, index) => (
            <tr key={index}>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{config.cloudType}</td>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{config.provider}</td>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{config.accessKey || 'NA'}</td>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>xxxxxxx</td>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{config.region || 'NA'}</td>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{config.privateKey || 'NA'}</td>
              <td style={{ border: '1px solid #ddd', padding: '10px',whiteSpace: 'nowrap' }}>{config.host || 'NA'}</td>
            </tr>
          ))}
        </tbody>
      </table> </div>}
      {/*Navigate*/}
      <button
        style={{...buttonStyle,marginTop:'1%'}}
        onClick={() => setAddConfig(true)}
      >
        Add Configuration
      </button>

    </div> }

    </div>
   
  );
};

export default ConfigPage;
