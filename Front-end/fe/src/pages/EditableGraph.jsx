import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useParams } from 'react-router-dom';
import Modal from 'react-modal';
import { useHistory, link } from 'react-router-dom';
import axios from 'axios';


const EditableGraph = ({ location }) => {
	// console.log(location.state['functionList']);
	const history = useHistory(); // Move the useHistory hook here
	let userId="647ccafb9ffc37a91aaad558"; 
	let application=null
	if(location.state['application']){application=location.state['application']}

	const fnList = Array.isArray(location.state['application'].functions) ? (location.state['application'].functions) : [];
	const nodes = fnList.map((fn, index) => ({
		id: fn.functionShortName,
		x: (index * 100) + 100,
		y: Math.floor(Math.random() * 3 + 1) * 100
	}));

	// console.log(nodes)
	const svgRef = useRef(null);
	const [allNodes, setAllNodes] = useState(nodes);
	const [allLinks, setAllLinks] = useState([]);
	const [errorMessage,setErrorMessage] = useState(null);
	const [successMessage,setSuccessMessage] = useState(null);

	// const addNode = () => {
	// 	const newNodeId = prompt('Enter the ID of the new node:');
	// 	if (newNodeId) {
	// 		const newNode = { id: newNodeId, x: 500, y: 200 };
	// 		setAllNodes([...allNodes, newNode]);
	// 	}
	// };


	const [modalOpen, setModalOpen] = useState(false);
	const [sourceNode, setSourceNode] = useState('');
	const [targetNode, setTargetNode] = useState('');
	const [linkWeight, setLinkWeight] = useState(0);
	const [customLinkWeight, setCustomLinkWeight] = useState('');

	const openModal = () => {
		setModalOpen(true);
	};

	const closeModal = () => {
		setModalOpen(false);
	};

	const handleSourceNodeChange = (event) => {
		setSourceNode(event.target.value);
	};

	const handleTargetNodeChange = (event) => {
		setTargetNode(event.target.value);
	};

	const handleLinkWeightChange = (event) => {
		const selectedWeight = event.target.value;
		if (selectedWeight === 'custom') {
			setLinkWeight('custom');
		} else {
			setLinkWeight(parseFloat(selectedWeight));
		}
	};

	const handleCustomLinkWeightChange = (event) => {
		setCustomLinkWeight(parseFloat(event.target.value));
	};


	const handleAddLink = () => {
		closeModal();
		const weight = linkWeight === 'custom' ? customLinkWeight : linkWeight;
		if (sourceNode && targetNode && weight) {
			const newLink = { source: sourceNode, target: targetNode, weight: weight };
			setAllLinks([...allLinks, newLink]);
		}
	};
	// const addLabel = () => {
	// 	const nodeId = prompt('Enter the ID of the node to label:');
	// 	const label = prompt('Enter the label for the node:');
	// 	if (nodeId && label) {
	// 		const newLabel = { nodeId, label };
	// 		setLabels([...labels, newLabel]);
	// 	}
	// };

	//Handle App Register
	const handleAppRegister =async()=>{
		//Convert it to required format
		let edges = allLinks.map(({source, target, weight}) => {
		const sourceIndex = parseInt(source.substring(1));
		const targetIndex = parseInt(target.substring(1));
		return [sourceIndex, targetIndex, weight];
		});

		//attach edge with it 
		application.edges = edges;
  
		try {
			console.log(typeof application.functionsCount)
			const response = await axios.post(`http://127.0.0.1:5000/application/${userId}`, application);
			console.log(response.data)
			if(response.data.status=="Error") {setErrorMessage(response.data.message)}
			if(response.data.status=="Success"){setSuccessMessage(response.data.message)}

		  } catch (error) {
			console.error('Error:', error);
		}
	}

	const hideMessage =()=>{
		setErrorMessage(null)
		setSuccessMessage(null)
	}

	useEffect(() => {
		console.log(allLinks)
	}, [allLinks])

	useEffect(() => {
		const width = 1300;
		const height = 700;

		const svg = d3.select(svgRef.current)
			.attr('height', height)
			.attr('width', width);

		const nodes = allNodes

		const links = allLinks

		const link = svg.append('g')
			.selectAll('line')
			.data(links.filter((link) => link.source !== link.target))
			.enter()
			.append('line')
			.attr('marker-end', 'url(#arrowhead)')
			.style('stroke', '#333')
			.style('stroke-width', 4);

		const selfLoop = svg
			.append('g')
			.selectAll('path')
			.data(links.filter((link) => link.source === link.target))
			.enter()
			.append('path')
			.attr('d', (d) => {
				const x = 0;
				const y = 0;
				const radiusX = 15; // X-axis radius
				const radiusY = 50; // Y-axis radius
				return `M${x - radiusX},${y}A${radiusX},${radiusY} 0 1,0 ${x + radiusX},${y}`;
			})
			.style('fill', 'none')
			.style('stroke', '#333')
			.style('stroke-width', 4)
			.attr('marker-end', 'url(#arrowhead-self-loop)');

		// Append the arrowhead marker to the defs section
		svg
			.append('defs')
			.append('marker')
			.attr('id', 'arrowhead-self-loop')
			.attr('viewBox', '-10 -10 25 25')
			.attr('refX', 36)
			.attr('refY', 28)
			.attr('markerWidth', 8)
			.attr('markerHeight', 6)
			.attr('orient', 'auto')
			.append('path')
			.attr('d', 'M-10,-6 L0,0 L-10,6')
			.attr('fill', '#333')
			.attr('transform', 'rotate(-30)');




		const selfLoopText = svg.append('g')
			.selectAll('text')
			.data(links.filter((link) => link.source === link.target))
			.enter()
			.append('text')
			.attr('x', (d) => getNodePosition(d.source).x)
			.attr('y', (d) => getNodePosition(d.source).y + 65)
			.attr('text-anchor', 'middle')
			.style('fill', '#000000')
			.style('font-size', '14px')
			.style('stroke', 'white')
			.style('stroke-width', '0.5px')
			.style('font-weight', 'bold') // Add font-weight
			.style('font-weight', '900')
			.text((d) => d.weight)
			.on('dblclick', handleLinkTextDoubleClick);

		const node = svg.append('g')
			.selectAll('circle')
			.data(nodes)
			.enter()
			.append('circle')
			.attr('r', 20)
			.style('fill', '#349eff')
			.call(d3.drag()
				.on('start', dragStarted)
				.on('drag', dragged)
				.on('end', dragEnded));

		const nodeLabels = svg.append('g')
			.selectAll('text')
			.data(nodes)
			.enter()
			.append('text')
			.text((d) => d.id)
			.attr('x', (d) => d.x)
			.attr('y', (d) => d.y + 6)
			.style('text-anchor', 'middle')
			.style('fill', '#000000')
			.style('font-size', '20px')
			.call(d3.drag()
				.on('start', dragStarted)
				.on('drag', dragged)
				.on('end', dragEnded));

		const linkText = svg
			.append('g')
			.selectAll('text')
			.data(links.filter((d) => getNodePosition(d.source).x !== getNodePosition(d.target).x))
			.enter()
			.append('text')
			.attr('text-anchor', 'middle')
			.text((d) => d.weight)
			.attr('x', (d) => (getNodePosition(d.source).x + getNodePosition(d.target).x) / 2)
			.attr('y', (d) => (getNodePosition(d.source).y + getNodePosition(d.target).y) / 2 - 7)
			.style('fill', '#000000')
			.style('font-size', '14px')
			.style('stroke', 'white')
			.style('stroke-width', '0.5px')
			.style('font-weight', 'bold') // Add font-weight
			.style('font-weight', '900')
			.on('dblclick', handleLinkTextDoubleClick);

		link
			.attr('x1', (d) => getNodePosition(d.source).x)
			.attr('y1', (d) => getNodePosition(d.source).y)
			.attr('x2', (d) => getNodePosition(d.target).x)
			.attr('y2', (d) => getNodePosition(d.target).y);

		node
			.attr('cx', (d) => d.x)
			.attr('cy', (d) => d.y);

		selfLoop.attr('transform', (d) => {
			const x = getNodePosition(d.source).x;
			const y = getNodePosition(d.source).y;
			return `translate(${x},${y})`;
		});

		function getNodePosition(nodeId) {
			const foundNode = nodes.find((node) => node.id === nodeId);
			return foundNode ? { x: foundNode.x, y: foundNode.y } : { x: 0, y: 0 };
		}

		function dragStarted(event, d) {
			d3.select(this).raise().classed('active', true);
		}

		function dragged(event, d) {
			d3.select(this).attr('cx', d.x = event.x).attr('cy', d.y = event.y);
			updateLinks();
			updateLinkTexts();
			updateSelfLoops();
			updateNodeLabels();
		}

		function dragEnded(event, d) {
			d3.select(this).classed('active', false);
		}

		function updateLinks() {
			link
				.attr('x1', (d) => getNodePosition(d.source).x)
				.attr('y1', (d) => getNodePosition(d.source).y)
				.attr('x2', (d) => getNodePosition(d.target).x)
				.attr('y2', (d) => getNodePosition(d.target).y);
		}

		function updateLinkTexts() {
			linkText
				.filter((d) => getNodePosition(d.source).x !== getNodePosition(d.target).x)
				.attr('x', (d) => (getNodePosition(d.source).x + getNodePosition(d.target).x) / 2)
				.attr('y', (d) => (getNodePosition(d.source).y + getNodePosition(d.target).y) / 2 - 7);

			selfLoopText
				.attr('x', (d) => getNodePosition(d.source).x)
				.attr('y', (d) => getNodePosition(d.source).y + 65);
		}

		function updateSelfLoops() {
			selfLoop.attr('transform', (d) => {
				const x = getNodePosition(d.source).x;
				const y = getNodePosition(d.source).y;
				return `translate(${x},${y})`;
			});
		}

		function updateNodeLabels() {
			nodeLabels
				.attr('x', (d) => d.x)
				.attr('y', (d) => d.y + 6);
		}

		function handleLinkTextDoubleClick(event, d) {
			const { x, y } = event.target.getBoundingClientRect();
			const textElement = d3.select(event.target);

			const foreignObject = linkText
				.append('foreignObject')
				.attr('x', x)
				.attr('y', y)
				.attr('width', 60)
				.attr('height', 20);

			const input = foreignObject
				.append('xhtml:input')
				.style('width', '100%')
				.style('height', '100%')
				.style('padding', '0px')
				.style('margin', '0px')
				.style('border', 'none')
				.style('outline', 'none')
				.style('font-size', '16px')
				.attr('contentEditable', true)
				.text(textElement.text())
				.on('blur', handleInputBlur);

			input.node().focus();

			textElement.style('display', 'none');

			function handleInputBlur() {
				const newText = input.node().value;
				textElement.text(newText);
				textElement.style('display', 'block');
				foreignObject.remove();
			}
		}

		const arrowhead = svg.append('defs')
			.append('marker')
			.attr('id', 'arrowhead')
			.attr('viewBox', '-10 -10 20 20')
			.attr('refX', 25)
			.attr('refY', 0)
			.attr('markerWidth', 4)
			.attr('markerHeight', 4)
			.attr('orient', 'auto')
			.append('path')
			.attr('d', 'M-10,-10 L0,0 L-10,10')
			.attr('fill', '#333');

		return () => {
			svg.selectAll('*').remove();
		};
	}, [allNodes, allLinks]);

	return (
		<div>
			<p style={instructions}>
				Please interact with the graph (You can adjust the nodes) element to perform certain actions, and use the "Add Link" button to create new links between nodes.
			</p>
			

			<div style={{ display: 'flex', justifyContent: 'space-between' }} >
				<button  style={buttonStyle} onClick={() => history.push('/create_app',{application})}> Back to  app</button>
				<button onClick={openModal} style={buttonStyle}>Add Link</button>
			</div>

			{errorMessage && (
			<div style={messageStyle}>
				{errorMessage}
				<span style={closeButtonStyle} onClick={hideMessage}>
					&times;
					</span>
				</div>
			)}

			{successMessage && (
			<div style={{...messageStyle, backgroundColor:'green'}}>
				{successMessage}
				<span style={closeButtonStyle} onClick={hideMessage}>
					&times;
					</span>
				</div>
			)}

			{/* Render the rest of the component */}

			<Modal isOpen={modalOpen} onRequestClose={closeModal} style={modalStyle}>
				<h2 style={{ marginBottom: '20px' }}>Add Link</h2>
				<div style={{ marginBottom: '20px' }}>
					<label style={{ marginBottom: '10px' }}>Source Node:</label>
					<select value={sourceNode} onChange={handleSourceNodeChange} style={selectStyle}>
						<option value="">Select a source node</option>
						{allNodes.map((node) => (
							<option key={node.id} value={node.id}>
								{node.id}
							</option>
						))}
					</select>
				</div>
				<div style={{ marginBottom: '20px' }}>
					<label style={{ marginBottom: '10px' }}>Target Node:</label>
					<select value={targetNode} onChange={handleTargetNodeChange} style={selectStyle}>
						<option value="">Select a target node</option>
						{allNodes.map((node) => (
							<option key={node.id} value={node.id}>
								{node.id}
							</option>
						))}
					</select>
				</div>
				<div style={{ marginBottom: '20px' }}>
					<label style={{ marginBottom: '10px' }}>Link Weight:</label>
					<select value={linkWeight} onChange={handleLinkWeightChange} style={selectStyle}>
						<option value="0.25">0.25</option>
						<option value="0.5">0.5</option>
						<option value="0.75">0.75</option>
						<option value="custom">Custom</option>
					</select>
					{linkWeight === 'custom' && (
						<input
							type="number"
							value={customLinkWeight}
							onChange={handleCustomLinkWeightChange}
							style={{ ...inputStyle, marginTop: '10px' }}
							placeholder="Enter"
						/>
					)}
				</div>

				<div>
					<button onClick={handleAddLink} style={buttonStyle}>
						Add Link
					</button>
					<button onClick={closeModal} style={buttonStyle}>
						Cancel
					</button>
				</div>
			</Modal>


			<div
				style={{
					overflow: 'auto',
					backgroundColor: '#eee',
					width: '100%',
					height: '100%',
					marginTop: '10px'
				}}
			>
				<svg ref={svgRef}></svg>
			</div>

			<button onClick={handleAppRegister}style={{...buttonStyle,backgroundColor:"green"}}>Register App</button>

		</div>
	);
};

// Button Style
const buttonStyle = {
	padding: '10px 20px',
	margin: '5px',
	backgroundColor: '#349eff',
	color: '#fff',
	border: 'none',
	borderRadius: '4px',
	cursor: 'pointer',
};
const selectStyle = {
	width: '150px',
	padding: '8px',
	borderRadius: '4px',
	border: '1px solid #ccc',
	backgroundColor: '#fff',
};
const inputStyle = {
	width: '30%',
	padding: '8px',
	marginLeft: '5px',
	borderRadius: '4px',
	border: '1px solid #ccc',
};
const instructions = {
	fontSize: '16px',
	color: '#555',
	marginBottom: '20px',
	marginLeft: '10px',
	// textAlign: 'center',
	fontStyle: 'italic',
	fontWeight: 400,
	textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)',
	letterSpacing: '1px'
}

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

// Modal Style
const modalStyle = {
	overlay: {
		backgroundColor: 'rgba(0, 0, 0, 0.5)',
		display: 'flex',
		alignItems: 'center',
		justifyContent: 'center',
	},
	content: {
		position: 'relative',
		top: 'auto',
		left: 'auto',
		right: 'auto',
		bottom: 'auto',
		maxWidth: '300px',
		width: '90%',
		padding: '30px',
		border: 'none',
		borderRadius: '8px',
		boxShadow: '0 2px 10px rgba(0, 0, 0, 0.3)',
		backgroundColor: '#fff',
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
		textAlign: 'center',
	},
};


export default EditableGraph;
