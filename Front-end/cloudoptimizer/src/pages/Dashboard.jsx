import React, { useEffect, useState } from 'react'

import { Link } from 'react-router-dom'

import Chart from 'react-apexcharts'

import { useSelector } from 'react-redux'

import StatusCard from '../components/status-card/StatusCard'

import Table from '../components/table/Table'

import Badge from '../components/badge/Badge'

import statusCards from '../assets/JsonData/status-card-data.json'

import axios from 'axios';


//Required Data
const functionsTypewiseChartData = {
    options: {
      labels: ['CPU', 'Network', 'Disk'],
      colors: ['#6ab04c', '#2980b9', '#9b59b6'],
      chart: {
        background: 'transparent'
      },
      legend: {
        position: 'bottom'
      }
    }
  };

//Required For all Functions Data
const allFunctionsHeader=["Function","Category","Application","Date","Status"]

const renderAllFunctionsHead = (item, index) => (
    <th key={index}>{item}</th>
)

const renderAllFunctionsBody = (item, index) => (
    <tr key={index}>
        <td>{item.name}</td>
        <td>{item.category}</td>
        <td>{item.applicationName}</td>
        <td>{item.date}</td>
        <td>
            <Badge type={functionStatus[item.status]} content={item.status} />
        </td>
    </tr>
)

const functionStatus = {
    "Deployed in Public Cloud": "primary",
    "Deployed in Private Cloud": "primary",
    "Deployed in Hybrid Cloud": "primary",
    "Pending": "warning"
}

const Dashboard = ({location}) => {
    const [user,setUser] = useState()
    const [cardCounts,setCardCounts]= useState([])
    const [functionsTypeWise,setFunctionstypewise]=useState([0,0,0])
    const [allFunctionsOfUser,setAllFunctionsOfUser]=useState([])
    const [chartFn,setChartFn] = useState();

    const userID = '647ccafb9ffc37a91aaad558'
    useEffect(() => {
        fetchData();
        fetchData2();
      }, []);

    useEffect(()=>{
        console.log(allFunctionsOfUser);
    },[allFunctionsOfUser])

    //Get all Functions data
    const fetchData2 = async () =>{
        try {
            const responseOfAllFunctionsRequest= await axios.get(`http://127.0.0.1:5000/application/functions/${userID}`);
            setAllFunctionsOfUser(responseOfAllFunctionsRequest.data)
        }
        catch (error){
            console.error('Error:', error);
        }
    } 

    //Get User Data
    const fetchData = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/users/${userID}`);
        setUser(response.data.user)
        //set Function Counts
        setCardCounts([response.data.user.totalApplications,response.data.user.totalFunctions,response.data.user.totalPrivateFunctions,response.data.user.totalPublicFunctions])
        //set pichart data
        let functionsTypeWisetemp =functionsTypewiseChartData.options.labels.map(fn=>(response.data.user.functionsTypeWise[fn]))
        functionsTypeWisetemp =functionsTypeWisetemp.map(value => (value === undefined ? 0 : value));
        setFunctionstypewise(functionsTypeWisetemp)
    } catch (error) {
        console.error('Error:', error);
    }
    };
    //End of Requests
    const themeReducer = useSelector(state => state.ThemeReducer.mode)

    //chartData
    const [publicCloudRTData,setPublicCloudRTData] = useState([0]);
    const [publicCloudMemData,setPublicCloudMemData]=useState([0]);
    const [privateCloudRTData,setPrivateCloudRTData] = useState([0]);
    const [privateCloudMemData,setPrivateCloudMemData] = useState([0]);

    const handleChangeChartFn =(Appfn)=>{
        let app =Appfn.split('-')[0];
        let fn =Appfn.split('-')[1];
        let selectedFunction = allFunctionsOfUser.find((func) =>func.applicationName === app && func.name === fn);
        console.log(selectedFunction);

        if(selectedFunction.publicResponseTimes){
            let publicMemValues = selectedFunction.publicResponseTimes.map(obj => obj.mem).sort((a, b) => a - b);
            let rtValues = selectedFunction.publicResponseTimes.sort((a, b) => a.mem - b.mem).map(obj => obj.rt);
            let formattedList = rtValues.map(rt => rt.toFixed(2));
            setPublicCloudMemData(publicMemValues);setPublicCloudRTData(formattedList)
        }else{
            setPublicCloudMemData([]);setPublicCloudRTData([]);
        }

        if(selectedFunction.privateResponseTimes){
            let privateMemValues = selectedFunction.privateResponseTimes.map(obj => obj.mem).sort((a, b) => a - b);
            let rtValues = selectedFunction.privateResponseTimes.sort((a, b) => a.mem - b.mem).map(obj => obj.rt);
            let formattedList = rtValues.map(rt => rt.toFixed(2));
            setPrivateCloudMemData(privateMemValues);setPrivateCloudRTData(formattedList)
        }else{
            setPrivateCloudMemData([]);setPrivateCloudRTData([]);
        }    
    }

    const chartOptions = {
        series: [{
            name: 'Public Cloud',
            data: publicCloudRTData
        }, {
            name: 'Private Cloud',
            data: privateCloudRTData
        }],
        options: {
            color: ['#6ab04c', '#2980b9'],
            chart: {
                background: 'transparent'
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            xaxis: {
                categories: [...publicCloudMemData,...privateCloudMemData],
                labels: {
                    rotate: -90,
                    trim: true,
                    minHeight: undefined,
                    maxHeight: 120,
                    style: {
                      fontSize: '12px',
                    },
                  },
                  title: {
                    text: 'Memory sizes',
                    offsetY: -20,
                    style: {
                      fontWeight: 500,
                    },
                  },
            },
            legend: {
                position: 'top'
            },
            grid: {
                show: true
            }
        }
    }


    return (
        <div>
            <h2 className="page-header">Dashboard</h2>
            <div className="row">
                <div className="col-5">
                    {/* Start of 4 Cards */}
                    <div className="row">
                        {
                            statusCards.map((item, index) => (
                                <div className="col-6" key={index}>
                                    <StatusCard
                                        icon={item.icon}
                                        count={cardCounts[index]}
                                        title={item.title}
                                    />
                                </div>
                            ))
                        }
                    </div>
                     {/* End of of 4 Cards */}
                </div>

                <div className="col-7">
                    <div className="card full-height">
                        {/* chart */}

                        {allFunctionsOfUser.length >0 ? 
                        <select
                            style={buttonStyle}
                            placeholder='Select function'
                            value={chartFn}
                            onChange={(e) => handleChangeChartFn(e.target.value)}
                            >
                            <option value="">Function</option>
                            
                            {allFunctionsOfUser.map((item,index) => (
                                <option key={index} value={`${item.applicationName}-${item.name}`}>
                                {`${item.applicationName} - ${item.name}`}
                                </option>
                            ))}
                        </select> : null}

                        <Chart
                            options={themeReducer === 'theme-mode-dark' ? {
                                ...chartOptions.options,
                                theme: { mode: 'dark' }
                            } : {
                                ...chartOptions.options,
                                theme: { mode: 'light' }
                            }}
                            series={chartOptions.series}
                            type='line'
                            height='120%'
                        />
                    </div>
                </div>

                <div className="col-5" style={{marginTop : -160}}>
                    <div className="card">
                        <div className="card__header">
                        <h3>Functions Typewise</h3>
                        </div>
                        <div className="card__body">
                        <Chart
                            options={functionsTypewiseChartData.options}
                            series={functionsTypeWise}
                            type="pie"
                            height="445"
                        />
                        </div>
                    </div>
                </div>

                <div className="col-7">
                    <div className="card">
                        <div className="card__header">
                            <h3>Recent Functions</h3>
                        </div>
                        <div className="card__body">
                        {allFunctionsOfUser.length > 0 ? (
                            <Table
                                limit="5"
                                headData={allFunctionsHeader}
                                renderHead={(item, index) => renderAllFunctionsHead(item, index)}
                                bodyData={allFunctionsOfUser}
                                renderBody={(item, index) => renderAllFunctionsBody(item, index)}
                            />
                        ) : (
                            <p>Loading...</p>
                            )}
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    )
}

const buttonStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '5px 15px',
    backgroundColor: '#349eff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
};

export default Dashboard
