<script lang="ts">
	import { onMount } from 'svelte';
	import { format, differenceInDays } from 'date-fns';

	import { initRows, fullMonthYear, arrDays, updateRows } from '../datapicker';
	import { currentDate, scores } from '../store';

	const minMaxScore = $derived(Math.min(...Object.values($scores).map((d) => d.max_score || 0)));
	const maxMaxScore = $derived(Math.max(...Object.values($scores).map((d) => d.max_score || 0)));

	const findCutoffs = () => {
		const value = (maxMaxScore - minMaxScore) / 5; // Divide the range into 5 equal parts
		return [
			minMaxScore,
			minMaxScore + value,
			minMaxScore + value * 2,
			minMaxScore + value * 3,
			minMaxScore + value * 4
		];
	};

	const cutoffs = $derived(findCutoffs());

	let rows = $state(initRows()),
		selectedMonth = $state(+format(new Date(), 'MM')),
		selectedYear = $state(+format(new Date(), 'yyyy')),
		selectedFullDate = $state(format(new Date(), 'MM-dd-yyyy'));

	function lookupColor(score: number, cutoffs: number[]): string {
		// create 5 bands of colors between min and max

		if (score >= cutoffs[4]) {
			return 'bg-[#fb918f]'; // Red
		} else if (score >= cutoffs[3]) {
			return 'bg-[#fba58b]'; // dark orange
		} else if (score >= cutoffs[2]) {
			return 'bg-[#ffd497]'; // light orange
		} else if (score >= cutoffs[1]) {
			return 'bg-[#fdf29a]'; // dark yellow
		} else if (score >= cutoffs[0]) {
			return 'bg-[#fff9c9]'; // Light Yellow
		} else {
			return 'bg-gray-100'; // Default light grey color
		}
	}

	function createDateColors($scores: {}): Record<string, string> {
		const dateColors: Record<string, string> = {};
		Object.entries($scores).forEach(([date, scoreData]) => {
			const dateKey = format(new Date(date + 'T00:00:00'), 'yyyy-MM-dd');

			const score = scoreData.max_score || 0;
			const color = lookupColor(score, cutoffs);

			dateColors[dateKey] = color;
		});
		return dateColors;
	}

	let dateColors = $derived(createDateColors($scores));

	// Function to get color for a specific date
	function getDateColor(year: number, month: number, day: number): string {
		const dateKey = `${year}-${padNumber(month)}-${padNumber(day)}`;
		return dateColors[dateKey] || 'bg-gray-100'; // Default light grey color
	}

	/**
	 * Navigate months
	 */
	function previousMonth() {
		selectedMonth--;

		if (selectedMonth <= 0) {
			selectedMonth = 12;
			selectedYear--;
		}
		rows = updateRows(selectedMonth, selectedYear);
	}

	function nextMonth() {
		selectedMonth++;

		if (selectedMonth > 12) {
			selectedMonth = 1;
			selectedYear++;
		}

		rows = updateRows(selectedMonth, selectedYear);
	}

	function padNumber(num: number): string {
		return num.toString().padStart(2, '0');
	}

	function selectDate(y: number, m: number, d: number): void {
		// add leading zero to single digit days and months
		let d_str = padNumber(d);
		let m_str = padNumber(m);

		// update selectedFullDate
		selectedFullDate = format(new Date(`${y}-${m_str}-${d_str}T12:00:00`), 'MM-dd-yyyy');
	}

	function setDate(y: number, m: number, d: number): void {
		// add leading zero to single digit days and months
		let d_str = padNumber(d);
		let m_str = padNumber(m);

		// update selectedFullDate
		currentDate.set(new Date(`${y}-${m_str}-${d_str}T12:00:00`));
	}

	/**
	 * Lifecycle methods
	 */
	onMount(() => {
		rows = updateRows(selectedMonth, selectedYear);
	});

	$effect(() => {
		// Update calendar when currentDate changes
		if ($currentDate) {
			const newDate = new Date($currentDate);
			let month = +format(newDate, 'MM');
			let year = +format(newDate, 'yyyy');
			selectDate(year, month, +format(newDate, 'dd'));
		}
	});
</script>

<main>
	<div class="relative flex items-center justify-center">
		<div id="datepicker" class="relative z-20 w-full max-w-[540px] h-full shadow-lg">
			<div class="w-full">
				<div class="w-full">
					<div class="flex items-center justify-between">
						<!-- Month year -->
						<span class="text-lg font-bold text-black"
							>{fullMonthYear(selectedMonth, selectedYear)}</span
						>
						<div class="flex items-center">
							<!-- bnt previous -->
							<button
								type="button"
								onclick={previousMonth}
								aria-label="View previous month"
								class="text-gray-800 dark:text-gray-200 previous-month"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="icon icon-tabler icon-tabler-chevron-left"
									width="24"
									height="24"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									fill="none"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<path stroke="none" d="M0 0h24v24H0z" fill="none" />
									<polyline points="15 6 9 12 15 18" />
								</svg>
							</button>
							<!-- bnt next -->
							<button
								type="button"
								onclick={nextMonth}
								aria-label="View next month"
								class="ml-3 text-gray-800 dark:text-gray-200 next-month"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="icon icon-tabler icon-tabler-chevron-right"
									width="24"
									height="24"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									fill="none"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<path stroke="none" d="M0 0h24v24H0z" fill="none" />
									<polyline points="9 6 15 12 9 18" />
								</svg>
							</button>
						</div>
					</div>
					<div class="flex items-center justify-between pt-6 overflow-x-auto day-table">
						<table class="w-full">
							<thead>
								<tr>
									{#each arrDays() as day}
										<th>
											<div class="flex justify-center w-full">
												<p class="text-base font-medium text-center">
													{day}
												</p>
											</div>
										</th>
									{/each}
								</tr>
							</thead>

							<tbody>
								{#each rows as col}
									<tr>
										{#each col as d}
											<td>
												{#if d}
													<div class="flex justify-center w-full px-1 py-1 cursor-pointer">
														<button
															onclick={() => {
																setDate(selectedYear, selectedMonth, d);
																selectDate(selectedYear, selectedMonth, d);
															}}
															class="text-center text-black border-none w-14 h-14 hover:border-solid hover:border-4 hover:border-black cursor-pointer {getDateColor(
																selectedYear,
																selectedMonth,
																d
															)}"
															class:active-day-button={differenceInDays(
																new Date(`${selectedFullDate}`),
																new Date(
																	`${selectedYear}-${padNumber(selectedMonth)}-${padNumber(d)}T00:00:00`
																)
															) === 0}
														>
															{d}
														</button>
													</div>
												{/if}
											</td>
										{/each}
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					<!-- Legend -->
					<div class=" p-3 rounded-lg">
						<div class="flex items-center space-x-4 items-start">
							<!-- No sunset -->
							<div class="flex items-center space-x-1">
								<div class="w-4 h-4 bg-gray-100 border border-gray-300 rounded"></div>
								<span class="text-xs text-gray-600 self-start">No Sunset</span>
							</div>
							<!-- Sunset quality gradient -->
							<div class="flex items-center space-x-1 items-start">
								<div class="flex flex-col items-center space-y-1">
									<div class="flex space-x-1">
										<div class="w-4 h-4 bg-[#fff9c9] rounded"></div>
										<div class="w-4 h-4 bg-[#fdf29a] rounded"></div>
										<div class="w-4 h-4 bg-[#ffd497] rounded"></div>
										<div class="w-4 h-4 bg-[#fba58b] rounded"></div>
										<div class="w-4 h-4 bg-[#fb918f] rounded"></div>
									</div>
									<div class="w-full flex justify-center">
										<svg width="60" height="12" viewBox="0 0 60 12" class="text-gray-400">
											<path
												d="M2 6 L58 6 M52 2 L58 6 L52 10"
												stroke="currentColor"
												stroke-width="2"
												fill="none"
											/>
										</svg>
									</div>
								</div>
								<div class="flex flex-col items-center">
									<span class="text-xs text-gray-600">Nicer Sunset</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- <footer>
		<div class="flex items-center justify-center py-10 text-gray-600 dark:text-gray-400">
			<a
				href="https://zachpatrick.com/blog/build-a-custom-datepicker-with-svelte"
				target="_blank"
				class="underline hover:text-black dark:hover:text-white">Built by Zach Patrick</a
			>&nbsp;&nbsp;<a
				href="https://github.com/zpthree/svelte-datepicker"
				target="_blank"
				rel="noopener noreferrer"
				class="hover:text-black dark:hover:text-white"
			>
				<span class="sr-only">View on GitHub</span>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5" viewBox="0 0 496 512"
						fill="currentColor"
						d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3 .3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5 .3-6.2 2.3zm44.2-1.7c-2.9 .7-4.9 2.6-4.6 4.9 .3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3 .7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3 .3 2.9 2.3 3.9 1.6 1 3.6 .7 4.3-.7 .7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3 .7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3 .7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"
					/></svg
				>
			</a>
		</div>
	</footer> -->
</main>

<style>
	/* Base calendar styles */
	#datepicker {
		width: 100%;
		max-width: 540px;
		overflow: hidden;
	}

	/* Prevent horizontal overflow */
	main {
		overflow-x: hidden;
		width: 100%;
	}

	/* Month/year header responsive */
	.text-lg {
		font-size: clamp(0.875rem, 2.5vw, 1.125rem);
	}

	/* Day header responsive */
	.text-base {
		font-size: clamp(0.625rem, 1.8vw, 1rem);
	}

	/* Day buttons responsive - more aggressive scaling */
	.w-14.h-14 {
		width: clamp(2rem, 6vw, 3.5rem);
		height: clamp(2rem, 6vw, 3.5rem);
		font-size: clamp(0.625rem, 2vw, 1rem);
		min-width: 0;
	}

	/* Ensure table doesn't overflow */
	table {
		table-layout: fixed;
		width: 100%;
	}

	/* Tablet styles */
	@media (max-width: 768px) {
		#datepicker {
			max-width: 100%;
			margin: 0;
		}

		.w-full.p-4.md\\:p-8 {
			padding: 0.75rem !important;
		}

		.pt-6 {
			padding-top: 0.75rem !important;
		}

		/* Make table more compact */
		table {
			font-size: 0.75rem;
		}

		.px-1.py-1 {
			padding: 0.125rem !important;
		}

		/* Smaller buttons for tablet */
		.w-14.h-14 {
			width: clamp(1.75rem, 5vw, 2.5rem) !important;
			height: clamp(1.75rem, 5vw, 2.5rem) !important;
			font-size: clamp(0.625rem, 1.8vw, 0.875rem) !important;
		}
	}

	/* Mobile styles */
	@media (max-width: 480px) {
		.w-full.p-4.md\\:p-8 {
			padding: 0.5rem !important;
		}

		.pt-6 {
			padding-top: 0.5rem !important;
		}

		/* Smaller navigation buttons */
		.ml-3 {
			margin-left: 0.25rem !important;
		}

		/* Even more compact table */
		table {
			font-size: 0.625rem;
		}

		.px-1.py-1 {
			padding: 0.0625rem !important;
		}

		/* Adjust day headers */
		th p {
			font-size: 0.625rem !important;
		}

		/* Mobile-specific button sizing */
		.w-14.h-14 {
			width: clamp(1.5rem, 4.5vw, 2rem) !important;
			height: clamp(1.5rem, 4.5vw, 2rem) !important;
			font-size: clamp(0.5rem, 1.5vw, 0.75rem) !important;
		}

		/* Ensure no overflow on mobile */
		.day-table {
			overflow-x: hidden !important;
		}
	}

	/* Very small screens */
	@media (max-width: 360px) {
		.w-full.p-4.md\\:p-8 {
			padding: 0.25rem !important;
		}

		.pt-6 {
			padding-top: 0.25rem !important;
		}

		/* Ultra compact buttons */
		.w-14.h-14 {
			width: 1.25rem !important;
			height: 1.25rem !important;
			font-size: 0.5rem !important;
		}

		/* Minimal spacing */
		.px-1.py-1 {
			padding: 0.03125rem !important;
		}

		/* Smaller navigation icons */
		svg {
			width: 16px !important;
			height: 16px !important;
		}
	}

	/* Extra small screens */
	@media (max-width: 320px) {
		.w-14.h-14 {
			width: 1.125rem !important;
			height: 1.125rem !important;
			font-size: 0.4375rem !important;
		}

		.text-lg {
			font-size: 0.75rem !important;
		}

		th p {
			font-size: 0.5rem !important;
		}
	}
</style>
