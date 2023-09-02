import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useParams } from 'react-router-dom';

const DefinedGraph = ({ nodes, links, pageFrom }) => {
	console.log(nodes, links)
	const svgRef = useRef(null);
	const [labels, setLabels] = useState([]);
	const [allNodes, setAllNodes] = useState(nodes);
	const [allLinks, setAllLinks] = useState(links);

	const addNode = () => {
		const newNodeId = prompt('Enter the ID of the new node:');
		if (newNodeId) {
			const newNode = { id: newNodeId, x: 500, y: 200 };
			setAllNodes([...allNodes, newNode]);
		}
	};

	const addLink = () => {
		const sourceNode = prompt('Enter the ID of the source node:');
		const targetNode = prompt('Enter the ID of the target node:');
		const weight = prompt('Enter the weight of the link:');
		if (sourceNode && targetNode && weight) {
			const newLink = { source: sourceNode, target: targetNode, weight: parseFloat(weight) };
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

	useEffect(() => {
		const width = 800;
		const height = 600;

		const svg = d3.select(svgRef.current)
			.attr('width', width)
			.attr('height', height);

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
			{pageFrom === 'appPage' ? null : (
				{/* <div>
					<button onClick={addLink}
						style={{
							backgroundColor: '#349eff',
							color: '#ffffff',
							marginRight: '10px',
							padding: '8px 16px',
							border: 'none',
							borderRadius: '4px',
							fontSize: '16px',
							cursor: 'pointer',
							boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
						}}
					>Add Link</button>
					<button onClick={addNode}
						style={{
							backgroundColor: '#349eff',
							color: '#ffffff',
							marginRight: '10px',
							padding: '8px 16px',
							border: 'none',
							borderRadius: '4px',
							fontSize: '16px',
							cursor: 'pointer',
							boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
						}}
					>Add Node</button>
				</div> */}
			)}
			<div>
				<svg ref={svgRef}></svg>
			</div>

			{/* <button onClick={addLabel}>Add Label</button> */}
		</div>
	);
};

export default DefinedGraph;
