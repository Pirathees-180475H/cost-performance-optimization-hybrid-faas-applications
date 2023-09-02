import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

const SignupPage = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const history = useHistory();

	const handleSignup = (e) => {
		e.preventDefault();
		// Perform signup logic here
		// ...

		// Redirect to the home page after successful signup
		history.push('/login');
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

	return (
		<div>
			<style>{loginStyles}</style>
			<div className="container">
				<div className="card">
					<div className="top-row">
						<p>Sign Up</p>
					</div>
					<form onSubmit={handleSignup}>
						<div className="card-details">
							<input
								type="text"
								placeholder="Username"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
							/>
						</div>
						<div className="card-details">
							<input
								type="password"
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
						</div>
						<div className="card-details">
							<input
								type="password"
								placeholder="Confirm Password"
								value={confirmPassword}
								onChange={(e) => setConfirmPassword(e.target.value)}
							/>
						</div>
						<button type="submit" className="sign-in">
							Sign Up
						</button>
					</form>
				</div>
			</div>
		</div>
	);
};

export default SignupPage;
