import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import {useHistory} from 'react-router-dom';
import axios from 'axios';


const LoginPage = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [showWarning, setShowWarning] = useState(false);
	const history =useHistory();
	const [data,setData] = useState('');


	const handleLogin = async(e) => {
		e.preventDefault();
		try {
			const response = await axios.post('http://127.0.0.1:5000/login', {
			name: username,
			password: password
			});
			setData(response.data)	
			if (response.data.id) {
				history.push('/dashboard',{'user_id':response.data.id})
			} else {
				setShowWarning(true);
			}

		} catch (error) {
			console.error('Error:', error);
		}

	};

	const handleSignup = () => {
		// Redirect to the signup page
		window.location.href = '/signup';
	};

	const loginStyles = `
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.card {
  background-color: #349eff;
  width: 300px;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.top-row {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.top-row p {
  color: white;
  font-size: 18px;
}

.card-details {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.card-details.warning {
  border: 1px solid #f44336;
}

.card-details i {
  margin-right: 10px;
  color: white;
}

.card-details input {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 3px;
}

.card-details.warning input {
  border: 1px solid #f44336;
}

.bx-error-circle {
  color: #f44336;
}

.forget {
  color: white;
  margin-top: 10px;
  font-size: 14px;
}

.sign-in {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #349eff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.sign-up {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  background-color: white;
  color: #349eff;
  font-weight: bold;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
`;

	// Inside the component
	return (
		<div>
			<style>{loginStyles}</style>
			<div className="container">
				<div className="card">
					<div className="top-row">
						<p>Login</p>
					</div>
					<form onSubmit={handleLogin}>
						<div className={`card-details ${showWarning ? 'warning' : ''}`}>
							<i className="bx bxs-user"></i>
							<input
								type="text"
								placeholder="Username"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
							/>
							{showWarning && <span className="bx bx-error-circle"></span>}
						</div>
						<div className={`card-details ${showWarning ? 'warning' : ''}`}>
							<i className="bx bxs-lock-alt"></i>
							<input
								type="password"
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
						</div>
						{showWarning && <p className="forget">{data.message}</p>}
					
						<button type="submit" className="sign-in">
							Login
						</button>
					</form>
					<button className="sign-up" onClick={handleSignup}>
						Create account
					</button>
				</div>
			</div>
		</div>
	);

};

export default LoginPage;
