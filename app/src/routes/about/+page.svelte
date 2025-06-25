<script>
	// You can add any script logic here if needed
</script>

<main>
	<div class="article">
		<div class="title">Never Miss the Sunset Again</div>
		<div class="subtitle">
			Using a small camera and some code, enjoy last nights' sunset every day, all day.
		</div>
		<p class="byline">By <a href="austinsteinhart.com">Austin Steinhart</a> | Summer 2025</p>

		<div class="body">
			<p>
				Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies
				tincidunt, nisl nisl aliquam nisl, eget ultricies nisl nisl sit amet nisl. Nullam auctor,
				nisl eget ultricies tincidunt, nisl nisl aliquam nisl, eget ultricies nisl nisl sit amet
				nisl.
			</p>

			<p>
				Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
				quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
			</p>

			<!-- Add more paragraphs as needed -->
			<div class="diagram-container">
				<h3>How It Works</h3>
				<div class="diagram">
					<!-- Each row contains sun visualization with time label and image -->
					<div class="sunset-row">
						<div class="sunset-visual sun-pos-1">
							<div class="time">Sunset -20 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-20m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-2">
							<div class="time">Sunset -15 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-15m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-3">
							<div class="time">Sunset -10 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-10m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-4">
							<div class="time">Sunset -5 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-5m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-5">
							<div class="time">Sunset</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">Sunset</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-6">
							<div class="time">Sunset +5 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+5m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-7">
							<div class="time">Sunset +10 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+10m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-8">
							<div class="time">Sunset +15 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+15m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-9">
							<div class="time">Sunset +20 min</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+20m</div></div>
					</div>
				</div>
				<p class="diagram-caption">
					Camera captures images every 5 minutes, from 20 minutes before sunset to 20 minutes after.
				</p>
			</div>
		</div>
	</div>
</main>

<style>
	.article {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 2rem 1rem;
	}

	.title {
		font-size: 2.5rem;
		font-weight: bold;
		text-align: center;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		font-size: 1.5rem;
		text-align: center;
		margin-bottom: 1rem;
		width: 60%;
	}

	.byline {
		font-style: italic;
		margin-bottom: 2rem;
	}

	.body {
		width: 60%;
		line-height: 1.6;
	}

	.diagram-container {
		margin: 3rem 0;
		width: 100%;
	}

	.diagram {
		display: flex;
		width: 100%;
		margin: 1.5rem 0;
	}

	.time {
		font-size: 0.9rem;
		color: #555;
		position: absolute;
		left: 0;
		top: -20px;
		width: 100%;
	}

	.diagram {
		display: flex;
		flex-direction: column;
		width: 100%;
		gap: 0;
	}

	.sunset-row {
		display: flex;
		align-items: center;
		margin-bottom: 1rem;
	}

	.sunset-visual {
		position: relative;
		height: 50px;
		width: 30%;
		margin-right: 1rem;
		padding-top: 20px;
	}

	.horizon-line {
		position: absolute;
		width: 100%;
		height: 2px;
		background-color: #333;
		top: 50%;
		z-index: 2;
	}

	.sun {
		position: absolute;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background: linear-gradient(to bottom, #ff7e00, #ff3300);
		z-index: 1;
		left: 50%;
		transform: translateX(-50%);
	}

	/* Sun positions */
	.sun-pos-1 .sun {
		top: 30%;
	}
	.sun-pos-2 .sun {
		top: 35%;
	}
	.sun-pos-3 .sun {
		top: 40%;
	}
	.sun-pos-4 .sun {
		top: 45%;
	}
	.sun-pos-5 .sun {
		top: 50%;
	}
	.sun-pos-6 .sun {
		top: 52%;
	}
	.sun-pos-7 .sun {
		top: 54%;
	}
	.sun-pos-8 .sun {
		top: 56%;
	}
	.sun-pos-9 .sun {
		top: 58%;
	}

	.thumbnail {
		width: 30%;
		aspect-ratio: 4/3;
		border: 1px solid #ddd;
		border-radius: 4px;
		overflow: hidden;
	}

	.placeholder-img {
		width: 100%;
		height: 100%;
		background-color: #f0f0f0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.8rem;
		color: #666;
	}

	.diagram-caption {
		font-style: italic;
		text-align: center;
		font-size: 0.9rem;
		margin-top: 1rem;
	}

	/* Responsive adjustments for smaller screens */
	@media (max-width: 768px) {
		.body {
			width: 90%;
		}
		.subtitle {
			width: 90%;
		}
		.sunset-row {
			flex-direction: column;
			align-items: center;
		}
		.time,
		.sunset-visual,
		.thumbnail {
			width: 100%;
			margin-bottom: 1rem;
		}

		.thumbnail {
			width: 80%;
		}

		.sunset-visual {
			margin: 0;
		}

		.time {
			text-align: center;
			font-size: 0.9rem;
		}
	}
</style>
