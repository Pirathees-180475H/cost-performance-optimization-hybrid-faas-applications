import React from 'react';
import { useHistory } from 'react-router-dom';

import cloudImage from '../assets/images/c1.png';

const teamMembers = [
	{
		name: 'John Doe',
		position: 'Founder',
		description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	},
	{
		name: 'Jane Smith',
		position: 'Designer',
		description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	},
	{
		name: 'Mark Johnson',
		position: 'Developer',
		description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	},
	// Add more team members here
];

const AboutUs = () => {
	const history = useHistory();

	const cardStyles = {
		width: '300px',
		padding: '20px',
		margin: '20px',
		borderRadius: '10px',
		boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
		transition: 'transform 0.3s',
	};

	const hoverStyles = {
		transform: 'translateY(-10px)',
	};

	const LogoutStyles = {
		margin: '10px',
		padding: '10px 20px',
		borderRadius: '5px',
		border: 'none',
		backgroundColor: '#349eff',
		color: '#fff',
		cursor: 'pointer',
	};

	const createAccountStyles = {
		margin: '10px',
		padding: '10px 20px',
		borderRadius: '5px',
		border: 'none',
		backgroundColor: '#F44336',
		color: '#fff',
		cursor: 'pointer',
	};

	const handleLogout = () => {
		// Implement your Logout logic here
		// Navigate to the '/Logout' page
		history.push('/login');
	};

	const handleCreateAccount = () => {
		// Implement your create account logic here
		// Navigate to the '/signup' page
		history.push('/signup');
	};

	return (
		<div style={{ textAlign: 'center' }}>
			<h1 style={{ fontSize: '32px', marginBottom: '20px' }}>About Us</h1>

			<div style={{ maxWidth: '100%', height: '400px', margin: '0 auto' }}>
				<img src={cloudImage} alt="Cloud" style={{ width: '100%', height: '100%', objectFit: 'cover', marginBottom: '20px' }} />
			</div>

			<div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: '50px' }}>
				{teamMembers.map((member, index) => (
					<div key={index} style={{ ...cardStyles, ...hoverStyles }} className="card">
						<h2 style={{ fontSize: '24px', marginBottom: '10px' }}>{member.name}</h2>
						<h3 style={{ fontSize: '16px', color: '#666', marginBottom: '10px' }}>{member.position}</h3>
						<p style={{ fontSize: '14px' }}>{member.description}</p>
					</div>
				))}
			</div>
			{/* <button style={LogoutStyles} onClick={handleLogout}>Logout</button> */}
			{/* <p style={{ color: '#666', margin: '10px' }}>Don't you have an account? <a href="/signup" style={{ color: '#349eff' }}>Create Account</a></p> */}
		</div>
	);
};

export default AboutUs;
