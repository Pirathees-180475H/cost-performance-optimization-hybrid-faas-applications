import React from 'react'

import { Route, Switch } from 'react-router-dom'

import Dashboard from '../pages/Dashboard'
import Applications from '../pages/MyApps'
import DefinedGraph from '../pages/DefinedGraph'
import NewApp from '../pages/CreateNewApp'
import AppPage from '../pages/Application'
import LoginPage from '../pages/Login'
import SignupPage from '../pages/SignUp'
import EditableGraph from '../pages/EditableGraph'
import AboutUs from '../pages/aboutus'
import LandingPage from '../pages/LandingPage'
import ConfigPage from '../pages/config'
import DeploymentPage from '../pages/deployApp'
import OptimizationPage from '../pages/optimizeApp'

const Routes = () => {
    return (
        <Switch>
            <Route path='/login' exact component={LoginPage} />
            <Route path='/signup' exact component={SignupPage} />
            <Route path='/dashboard' exact component={Dashboard} />
            <Route path='/my_apps' component={Applications} />
            <Route path='/create_app' component={NewApp} />
            <Route path='/definedGraph' component={DefinedGraph} />
            <Route path='/edit_graph' component={EditableGraph}/>
            <Route path="/application/:applicationId" component={AppPage} />
            <Route path='/config' component={ConfigPage} />
            <Route path='/deploy_app' component={DeploymentPage} />
            <Route path='/optimize_app' component={OptimizationPage} />

            <Route path='/' component={LandingPage} />
        
        </Switch>
    )
}

export default Routes
