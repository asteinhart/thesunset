<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { currentDate } from '../store';
	import { format } from 'date-fns';

	let svgElement: any;
	let tooltip: any;
	let containerElement: HTMLDivElement;
	let selectedDate = $derived(format($currentDate, 'MM-dd-yyyy'));
	const data = [
		{
			date: '07-01-2025',
			values: [10, 15, 20, 25, 35, 45, 50, 60, 75, 85, 80, 70, 60, 45, 35, 25, 15]
		},
		{
			date: '07-02-2025',
			values: [8, 12, 15, 20, 25, 55, 65, 75, 85, 90, 85, 75, 65, 50, 35, 20, 12]
		},
		{
			date: '07-03-2025',
			values: [15, 20, 30, 35, 40, 35, 40, 50, 65, 70, 75, 80, 70, 60, 50, 40, 25]
		},
		{
			date: '07-04-2025',
			values: [12, 18, 25, 30, 42, 55, 68, 78, 88, 92, 87, 75, 62, 48, 32, 22, 15]
		},
		{
			date: '07-05-2025',
			values: [20, 25, 28, 35, 45, 52, 60, 72, 82, 88, 85, 78, 65, 52, 38, 28, 18]
		},
		{
			date: '07-06-2025',
			values: [5, 8, 12, 18, 28, 38, 48, 62, 75, 85, 82, 70, 55, 40, 25, 15, 8]
		},
		{
			date: '07-07-2025',
			values: [18, 22, 28, 32, 40, 48, 58, 68, 78, 85, 80, 72, 60, 45, 32, 25, 18]
		},
		{
			date: '07-08-2025',
			values: [14, 18, 24, 30, 38, 46, 56, 66, 76, 82, 78, 68, 56, 42, 30, 20, 14]
		},
		{
			date: '07-09-2025',
			values: [16, 20, 26, 34, 44, 54, 64, 74, 84, 90, 86, 76, 64, 50, 36, 26, 16]
		},
		{
			date: '07-10-2025',
			values: [22, 28, 34, 40, 48, 58, 68, 78, 88, 94, 90, 82, 70, 56, 42, 30, 22]
		},
		{
			date: '07-11-2025',
			values: [12, 16, 22, 28, 36, 46, 56, 66, 76, 86, 82, 74, 62, 48, 34, 24, 16]
		},
		{
			date: '07-12-2025',
			values: [24, 30, 36, 42, 50, 60, 70, 80, 90, 96, 92, 84, 72, 58, 44, 32, 24]
		},
		{
			date: '07-13-2025',
			values: [8, 12, 18, 24, 32, 42, 52, 62, 72, 82, 78, 70, 58, 44, 30, 20, 12]
		}
	];

	const xValues = [-16, -14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16];
	const xLabels = [
		'-16min',
		'-14min',
		'-12min',
		'-10min',
		'-8min',
		'-6min',
		'-4min',
		'-2min',
		'Sunset',
		'+2min',
		'+4min',
		'+6min',
		'+8min',
		'+10min',
		'+12min',
		'+14min',
		'+16min'
	];

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
		const xScale = d3.scaleLinear().domain([-16, 16]).range([0, width]);

		const yScale = d3.scaleLinear().domain([0, 100]).range([height, 0]);

		// Color interpolation for sunset theme
		const maxValues = data.map((d) => d3.max(d.values) || 0);
		const minValue = d3.min(maxValues) || 0;
		const maxValue = d3.max(maxValues) || 100;

		const colorScale = d3
			.scaleLinear<string>()
			.domain([minValue, maxValue])
			.range(['#fdf29a', '#fb918f']) // yellow to red
			.interpolate(d3.interpolateHsl); // Use HSL for better color transitions

		// X axis - only show specific labels
		const displayTicks = [-16, -10, -4, 0, 4, 10, 16];
		const displayLabels = ['-16min', '-10', '-4', 'Sunset', '+4', '+10', '+16'];

		g.append('g')
			.attr('transform', `translate(0,${height})`)
			.call(
				d3
					.axisBottom(xScale)
					.tickValues(displayTicks)
					.tickFormat((d, i) => displayLabels[i])
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
			.y((d) => yScale(d));

		// Draw lines
		g.selectAll('.line')
			.data(data)
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
					.attr('stroke-width', d.date === selectedDate ? 5 : 2)
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
						`<span style="background: #ffc107; color: #333; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 8px;">${maxValue}</span> ${d.date}`
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
				currentDate.set(new Date(d.date));
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
