<script lang="ts">
	import '../app.css';

	import Header from '$lib/components/Header.svelte';
	import Calendar from '$lib/components/Calendar.svelte';
	import Graph from '$lib/components/Graph.svelte';
	import Highlights from '$lib/components/Highlights.svelte';

	import { getSunsetImage, formatDate } from '$lib/utils.ts';
	import { onMount } from 'svelte';
	import { currentDate } from '$lib/store';
	import { format } from 'date-fns';

	let sunsetDate = $state(formatDate($currentDate));
	let sunsetImage = $derived.by(() => getSunsetImage(sunsetDate));

	$effect(() => {
		// Update the sunset date whenever the current date changes
		sunsetDate = formatDate($currentDate);
		sunsetImage = getSunsetImage(sunsetDate);
	});

	let active = $state<'calendar' | 'chart' | null>('calendar');

	// let currentSunsetTime = $derived(() => {
	// 	const date = new Date(sunsetDate);
	// 	return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	// });
	let currentSunsetTime = $state('8:35pm Tuesday, July 5th, 2025');

	// let timing = $derived(() => {
	// 	const date = new Date(sunsetDate);
	// 	return `Sunset on ${date.toLocaleDateString()} at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
	// });
	let timing = $state('Peak 12 minutes after the Sunset');

	//let testCurrentDate = $derived(format($currentDate, 'MM-dd-yyyy'));

	$inspect('currnetDate', $currentDate);
	$inspect('sunset date', $currentDate);
	$inspect('path', sunsetImage);
</script>

<Header />

<div class="content">
	<div class="section">
		<div class="settings">
			<div class="controls">
				<button
					class="toggle-btn py-2 px-4 border rounded-l font-semibold transition-colors"
					class:bg-[#fba58b]={active === 'calendar'}
					class:text-white={active === 'calendar'}
					class:border-[#fba58b]={active === 'calendar'}
					class:bg-transparent={active !== 'calendar'}
					class:text-[#fba58b]={active !== 'calendar'}
					class:hover:bg-[#fba58b]={active !== 'calendar'}
					class:hover:text-white={active !== 'calendar'}
					onclick={() => (active = 'calendar')}
					>Calendar
				</button><button
					class="chart-btn py-2 px-4 border border-l-0 rounded-r font-semibold transition-colors"
					class:bg-[#fba58b]={active === 'chart'}
					class:text-white={active === 'chart'}
					class:border-[#fba58b]={active === 'chart'}
					class:bg-transparent={active !== 'chart'}
					class:text-[#fba58b]={active !== 'chart'}
					class:hover:bg-[#fba58b]={active !== 'chart'}
					class:hover:text-white={active !== 'chart'}
					onclick={() => (active = 'chart')}>Chart</button
				>
			</div>
			<div class="mt-4">
				{#if active === 'chart'}
					<Graph />
				{:else}
					<Calendar />
				{/if}
			</div>
		</div>
		<div class="image">
			<div class="image-container">
				<div class="image-header">
					<h3>{currentSunsetTime}</h3>
					<p>{timing}</p>
					<!-- <p>{$currentDate}</p> -->
				</div>
				{#if sunsetImage}
					<img src={sunsetImage} alt="Sunset for {sunsetDate}" class="full-image" />
				{/if}
			</div>
		</div>
	</div>

	<div class="highlights-section">
		<Highlights />
	</div>
</div>

<style>
	.section {
		display: flex;
		width: 100%;
		height: 75vh;
		gap: 0 1rem 0 0; /* Only gap on the right side between settings and image */
	}

	.settings {
		flex: 2; /* 2/5 of the space */
		padding: 2rem 0 2rem 2rem; /* Remove right padding */
		min-width: 0; /* Allows flex item to shrink below content size */
	}

	.image {
		flex: 3; /* 3/5 of the space */
		padding: 2rem;
		min-width: 0; /* Allows flex item to shrink below content size */
	}

	.image-container {
		display: flex;
		flex-direction: column;
		height: 100%;
	}

	.image-header {
		margin-bottom: 1rem;
	}

	.image-header h3 {
		margin: 0 0 0.5rem 0;
		font-size: 1.5rem;
	}

	.image-header p {
		margin: 0;
		color: #666;
	}

	.full-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
		border-radius: 8px;
		flex: 1;
	}

	.highlights-section {
		margin-top: 2rem;
		padding: 2rem;
	}

	/* Mobile styles */
	@media (max-width: 950px) {
		.section {
			flex-direction: column; /* Stack vertically */
			height: auto;
		}

		.settings {
			flex: none; /* Remove flex grow on mobile */
			padding: 1rem;
			order: 2; /* Settings appear second */
		}

		.image {
			flex: none; /* Remove flex grow on mobile */
			padding: 1rem;
			order: 1; /* Image appears first */
		}

		.full-image {
			width: 100%;
			height: 25vh;
			object-fit: cover;
		}

		.image-header h3 {
			font-size: 1.25rem;
		}

		.highlights-section {
			padding: 1rem;
		}
	}

	/* Tablet styles */
	@media (max-width: 1024px) and (min-width: 769px) {
		.settings,
		.image {
			padding: 1.5rem;
		}
	}
</style>
