import React from 'react';
import { useHistory } from 'react-router-dom';
import Table from '../components/table/Table';
import { useEffect, useState } from 'react'
import axios from 'axios';

const applicationTableHead = [
  'App Name',
  'Location',
  'No of Functions',
  'Date',
  'Status',
];

const renderHead = (item, index) => <th key={index}>{item}</th>;

const renderBody = (item, index, navigateToDetails) =>(
  <tr key={index} onClick={() => navigateToDetails(item.id)}>
    <td>{item.applicationName}</td>
    <td>{item.applicationLocation}</td>
    <td>{item.functionsCount}</td>
    <td>{item.date}</td>
    <td>{item.status}</td>
  </tr>
);

const Applications = () => {
  const history = useHistory();
  const [applicationsUser,setApplicationsOfUser]=useState([])
  const userID = '647ccafb9ffc37a91aaad558'

  const navigateToDetails = (applicationId) => {
    // Redirect to the details page of the selected application with the applicationId parameter
    history.push(`/application/${applicationId}`);
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    console.log(applicationsUser);
  }, [applicationsUser]); // Add applicationsUser as a dependency


  //Get data
  const fetchData = async () =>{
    try {
        const responseOfApplicationsRequest= await axios.get(`http://127.0.0.1:5000/application/user/${userID}`);
        setApplicationsOfUser(responseOfApplicationsRequest.data.applications) 
        console.log(responseOfApplicationsRequest.data)
    }
    catch (error){
        console.error('Error:', error);
    }
} 
  return (
    <div>
      <h2 className="page-header">Applications</h2>
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card__body">
            {applicationsUser.length > 0 ? (
                <Table
                  limit="10"
                  headData={applicationTableHead}
                  renderHead={(item, index) => renderHead(item, index)}
                  bodyData={applicationsUser}
                  renderBody={(item, index) => renderBody(item, index, navigateToDetails)}
                />
              ) : (
                <p>Loading...</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Applications;
