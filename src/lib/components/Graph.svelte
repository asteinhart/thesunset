<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { currentDate, scores } from '../store';
	import { format } from 'date-fns';

	let svgElement: any;
	let tooltip: any;
	let containerElement: HTMLDivElement;
	let selectedDate = $derived(format($currentDate, 'yyyy-MM-dd'));

	const xValues = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15];

	let prepData = Object.entries($scores).map(([key, item]) => ({
		date: key,
		values: xValues.map((timeKey) => item.scores[timeKey] || 0)
	}));

	$inspect(prepData, 'prepData');

	let yMax = $derived(Math.max(...prepData.flatMap((d) => d.values)));
	let yMaxMin = $derived(Math.min(...prepData.map((d) => Math.max(...d.values))));
	let yMin = $derived(Math.min(...prepData.flatMap((d) => d.values.filter((v) => v > 0))));

	console.log('yMin:', yMin);

	onMount(() => {
		drawChart();

		// Add resize listener
		function handleResize() {
			// Debounce the resize to avoid too many redraws
			clearTimeout(resizeTimeout);
			resizeTimeout = setTimeout(() => {
				drawChart();
			}, 50);
		}

		window.addEventListener('resize', handleResize);

		// Cleanup
		return () => {
			window.removeEventListener('resize', handleResize);
			if (tooltip) {
				tooltip.remove();
			}
		};
	});

	let resizeTimeout: any;

	// React to changes in selectedDate and redraw chart
	$effect(() => {
		// Trigger redraw when selectedDate changes
		selectedDate;
		if (svgElement && containerElement) {
			drawChart();
		}
	});

	// Function to draw/redraw the chart
	function drawChart() {
		if (!svgElement || !containerElement) return;

		// Clear previous chart
		d3.select(svgElement).selectAll('*').remove();

		// Get container dimensions dynamically
		const container = containerElement;
		const containerWidth = container ? container.clientWidth : 600;

		const margin = { top: 20, right: 20, bottom: 60, left: 30 };
		const width = Math.max(300, containerWidth - margin.left - margin.right); // Min width 300px, subtract some padding
		const height = Math.max(250, Math.min(400, width * 1.2)); // Responsive height with aspect ratio

		const svg = d3
			.select(svgElement)
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom);

		// Create tooltip if it doesn't exist
		if (!tooltip) {
			tooltip = d3
				.select('body')
				.append('div')
				.attr('class', 'tooltip')
				.style('position', 'absolute')
				.style('padding', '8px 12px')
				.style('background', '#f8f9fa')
				.style('color', '#333')
				.style('border', '2px solid black')
				.style('border-radius', '8px')
				.style('font-family', 'system-ui, -apple-system, sans-serif')
				.style('font-size', '14px')
				.style('font-weight', '500')
				.style('box-shadow', '0 4px 8px rgba(0, 0, 0, 0.15)')
				.style('pointer-events', 'none')
				.style('white-space', 'nowrap')
				.style('opacity', 0);
		}

		const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

		// Scales
		const xScale = d3.scaleLinear().domain([-30, 15]).range([0, width]);

		const yScale = d3
			.scaleLinear()
			.domain([Math.max(yMin - 10, 0), yMax + 10])
			.range([height, 0]);

		const colorScale = d3
			.scaleLinear<string>()
			.domain([yMaxMin, yMax])
			.range(['#fdf29a', '#fb918f']) // yellow to red
			.interpolate(d3.interpolateHsl); // Use HSL for better color transitions

		// X axis - only show specific labels
		const displayTicks = [-30, -20, -10, 0, 10];
		const displayLabels = ['-30min', '-20', '-10', 'Sunset', '+10'];

		g.append('g')
			.attr('transform', `translate(0,${height})`)
			.call(
				d3
					.axisBottom(xScale)
					.tickValues(displayTicks)
					.tickFormat((d, i) => displayLabels[i])
					.tickSizeOuter(0) // Removes the outer domain ticks
			)
			.selectAll('text')
			.style('font-family', 'system-ui, -apple-system, sans-serif')
			.style('font-size', '12px')
			.style('font-weight', '500')
			.style('fill', '#333');

		// Y axis (no ticks or labels)
		g.append('g')
			.call(
				d3
					.axisLeft(yScale)
					.tickSize(0)
					.tickFormat(() => '')
			)
			.selectAll('text')
			.style('font-family', 'system-ui, -apple-system, sans-serif');

		// Y axis label
		g.append('text')
			.attr('transform', 'rotate(-90)')
			.attr('y', 0 - margin.left)
			.attr('x', 0 - height / 2)
			.attr('dy', '1em')
			.style('text-anchor', 'middle')
			.style('font-family', 'system-ui, -apple-system, sans-serif')
			.style('font-size', '14px')
			.style('font-weight', '500')
			.style('fill', '#333')
			.text('Sunset Intensity');

		// Line generator
		const line = d3
			.line<number>()
			.x((d, i) => xScale(xValues[i]))
			.y((d) => yScale(d))
			.defined((d) => d !== 0) // Handle undefined/null values
			.curve(d3.curveCatmullRom.alpha(0.5));
		//.curve(d3.curveBasis); // ← Added this line

		// Draw lines
		g.selectAll('.line')
			.data(prepData)
			.enter()
			.append('g')
			.attr('class', 'line-group')
			.each(function (d, i) {
				const group = d3.select(this);

				// Create invisible buffer for easier mouse interaction
				group
					.append('path')
					.attr('class', 'line-buffer')
					.attr('fill', 'none')
					.attr('stroke', 'transparent')
					.attr('stroke-width', 20) // Wide invisible buffer
					.attr('d', line(d.values))
					.style('cursor', 'pointer');

				// Create visible line
				group
					.append('path')
					.attr('class', 'line-visible')
					.attr('fill', 'none')
					.attr('stroke', () => {
						const maxVal = d3.max(d.values) || 0;
						return d.date === selectedDate ? colorScale(maxVal as number) : 'grey';
					})
					.attr('stroke-width', d.date === selectedDate ? 5 : 1.5)
					.attr('stroke-opacity', d.date === selectedDate ? 1 : 0.2)
					.attr('d', line(d.values))
					.style('pointer-events', 'none'); // Disable pointer events on visible line
			})
			.on('mouseover', function (event, d) {
				// Change opacity to 0.75 on hover
				d3.select(this).select('.line-visible').attr('stroke-opacity', 0.75);

				// Show tooltip
				const maxValue = d3.max(d.values) || 0;

				tooltip.transition().duration(200).style('opacity', 0.9);
				tooltip
					.html(
						`<span style="background: ${colorScale(maxValue as number)}; color: #333; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 8px;">${Math.round(maxValue)}</span> ${d.date}`
					)
					.style('left', event.pageX + 10 + 'px')
					.style('top', event.pageY - 28 + 'px');
			})
			.on('mouseout', function (event, d) {
				// Restore original opacity
				const originalOpacity = d.date === selectedDate ? 1 : 0.2;
				d3.select(this).select('.line-visible').attr('stroke-opacity', originalOpacity);

				// Hide tooltip
				tooltip.transition().duration(500).style('opacity', 0);
			})
			.on('click', function (event, d) {
				// Update selected date
				currentDate.set(new Date(d.date + 'T00:00:00'));
				// Re-render the graph with the new selected date
				svg
					.selectAll('.line-visible')
					.attr('stroke', (lineData: any) => {
						const maxVal = d3.max(lineData.values) || 0;
						return lineData.date === selectedDate ? colorScale(maxVal as number) : 'grey';
					})
					.attr('stroke-width', (lineData: any) => (lineData.date === selectedDate ? 4 : 2))
					.attr('stroke-opacity', (lineData: any) => (lineData.date === selectedDate ? 1 : 0.2));
			});
	}
</script>

<div class="graph-container" bind:this={containerElement}>
	<svg bind:this={svgElement}></svg>
</div>

<style>
	.graph-container {
		width: 100%;
		height: auto;
		overflow: hidden;
		display: flex;
		justify-content: center;
	}

	svg {
		max-width: 100%;
		display: block;
	}

	/* Mobile responsiveness */
	@media (max-width: 768px) {
		.graph-container {
			padding: 0;
		}
	}

	@media (max-width: 480px) {
		.graph-container {
			overflow-x: auto;
			overflow-y: hidden;
		}

		svg {
			min-width: 320px; /* Ensure minimum usable width */
		}
	}
</style>
