<script lang="ts">
	import { getSunsetImage } from '../utils';
	import { format } from 'date-fns';
	import { currentDate } from '$lib/store';
	import { formatDate } from '$lib/utils.ts';

	// Sample highlight dates - you can make this dynamic later
	const highlights = [
		{ date: '7/1/25', formattedDate: '07-01-2025' },
		{ date: '6/23/25', formattedDate: '06-23-2025' },
		{ date: '2/7/23', formattedDate: '02-07-2023' },
		{ date: '10/5/26', formattedDate: '10-05-2026' },
		{ date: '7/7/25', formattedDate: '07-07-2025' },
		{ date: '3/15/24', formattedDate: '03-15-2024' },
		{ date: '8/22/25', formattedDate: '08-22-2025' },
		{ date: '12/3/23', formattedDate: '12-03-2023' },
		{ date: '5/18/26', formattedDate: '05-18-2026' },
		{ date: '9/11/24', formattedDate: '09-11-2024' },
		{ date: '4/30/25', formattedDate: '04-30-2025' },
		{ date: '11/14/23', formattedDate: '11-14-2023' },
		{ date: '6/8/26', formattedDate: '06-08-2026' },
		{ date: '1/25/24', formattedDate: '01-25-2024' },
		{ date: '7/4/25', formattedDate: '07-04-2025' }
	];

	// Function to handle clicking a highlight image
	function handleHighlightClick(formattedDate: string) {
		// Convert the formatted date string to a Date object
		const [month, day, year] = formattedDate.split('-').map(Number);
		const clickedDate = new Date(year, month - 1, day); // month is 0-indexed
		currentDate.set(clickedDate);

		// Smooth scroll to top
		window.scrollTo({
			top: 0,
			behavior: 'smooth'
		});
	}
</script>

<div class="highlights-container">
	<div class="highlights-header">
		<h2>Highlights</h2>
	</div>

	<div class="highlights-scroll">
		{#each highlights as highlight}
			<div class="highlight-item">
				<div class="highlight-date">{highlight.date}</div>
				<div
					class="highlight-image"
					onclick={() => handleHighlightClick(highlight.formattedDate)}
					role="button"
					tabindex="0"
					onkeydown={(e) => e.key === 'Enter' && handleHighlightClick(highlight.formattedDate)}
				>
					{#if getSunsetImage(highlight.formattedDate)}
						<img
							src={getSunsetImage(formatDate(highlight.formattedDate))}
							alt="Sunset for {highlight.date}"
						/>
					{:else}
						<div class="placeholder-image"></div>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.highlights-container {
		width: 100%;
		margin-bottom: 2rem;
	}

	.highlights-header {
		margin-bottom: 1rem;
		padding-bottom: 0.5rem;
		border-bottom: 2px solid #333;
	}

	.highlights-header h2 {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 400;
		color: #333;
		text-align: left;
	}

	.highlights-scroll {
		display: flex;
		gap: 1rem;
		overflow-x: auto;
		padding: 0.5rem 0;
		scrollbar-width: none; /* Firefox */
		-ms-overflow-style: none; /* Internet Explorer 10+ */
	}

	.highlights-scroll::-webkit-scrollbar {
		display: none; /* WebKit */
	}

	.highlight-item {
		flex: 0 0 auto;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		min-width: 150px;
	}

	.highlight-date {
		font-size: 0.9rem;
		font-weight: 500;
		color: #333;
		margin-bottom: 0.5rem;
		text-align: left;
	}

	.highlight-image {
		width: 150px;
		height: 100px;
		border-radius: 8px;
		overflow: hidden;
		background-color: #f0f0f0;
		cursor: pointer;
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	.highlight-image:hover {
		transform: scale(1.05);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.highlight-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.placeholder-image {
		width: 100%;
		height: 100%;
		background-color: #d1d5db;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	/* Mobile responsiveness */
	@media (max-width: 950px) {
		.highlights-header h2 {
			font-size: 1.5rem;
		}

		.highlights-scroll {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 1rem;
			overflow-x: visible;
			padding: 0.5rem 0;
		}

		.highlight-item {
			min-width: auto;
			width: 100%;
		}

		.highlight-image {
			width: 100%;
			height: 80px;
		}

		.highlight-date {
			font-size: 0.8rem;
		}
	}

	@media (max-width: 480px) {
		.highlights-scroll {
			grid-template-columns: 1fr 1fr;
			gap: 0.75rem;
		}

		.highlight-item {
			min-width: auto;
			width: 100%;
		}

		.highlight-image {
			width: 100%;
			height: 70px;
		}
	}
</style>
