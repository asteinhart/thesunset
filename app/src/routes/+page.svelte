<script lang="ts">
	import '../app.css';
	import { getSunsetImage, formatDate } from '$lib/utils.ts';
	import { onMount } from 'svelte';

	let sunsetDate = $state(formatDate(new Date()));
	let sunsetImage = $derived(getSunsetImage(sunsetDate));

	$inspect(sunsetDate);
</script>

<div class="content">
	<h2>Sunsets for {sunsetDate}</h2>
	<img src={sunsetImage} alt="" />

	<div>
		Choose a different date
		<input type="date" bind:value={sunsetDate} />
	</div>
</div>

<style>
	h2 {
		display: -webkit-box;
		display: flex;
		-webkit-box-pack: center;
		justify-content: center;
		-webkit-box-orient: vertical;
		-webkit-box-direction: normal;
		flex-direction: column;
		width: 100%;
		margin: 0 auto 4rem;
		text-align: center;
		text-transform: capitalize;
		font-family: 'Savate', sans-serif;
		font-size: var(--44px);
		padding: 3rem 0 0;
		z-index: 100;
		position: relative;
		overflow: hidden;
		min-height: 15rem;
	}

	h2:after {
		font-family: 'Savate', sans-serif;
		position: absolute;
		font-weight: 900;
		font-size: 200px;
		text-align: center;
		left: 50%;
		-webkit-transform: translate(-50%, -10%);
		transform: translate(-50%, -10%);
		text-transform: uppercase;
		pointer-events: none;
		z-index: -1;
		letter-spacing: -0.5rem;
	}

	.content h2:after {
		content: 'Sunsets';
		background: linear-gradient(to bottom, var(--light-yellow) 15%, var(--dark-orange));
		-webkit-text-fill-color: transparent;
		-webkit-background-clip: text;
		background-clip: text;
		opacity: 0.5;
	}

	.content {
		background: linear-gradient(to bottom, var(--light-yellow) 15%, var(--dark-orange) 100%);
		height: auto;
	}
</style>
