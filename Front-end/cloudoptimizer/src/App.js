import AboutPage from './pages/AboutPage';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import FunctionalitiesPage from './pages/Functionalities';

import { Routes } from 'react-router-dom';
import { Route } from 'react-router-dom';
import { BrowserRouter } from "react-router-dom";


function App() {
  return (
   <BrowserRouter>
   <Routes>
      <Route path="/" element={<HomePage/>}></Route>
       <Route path="about"  element={<AboutPage/>} />
       <Route path="login"  element={<LoginPage/>} />
       <Route path="join"  element={<RegisterPage/>} />
       <Route path="features"  element={<FunctionalitiesPage/>} />
   </Routes>
 </BrowserRouter>

  );
}

export default App;
