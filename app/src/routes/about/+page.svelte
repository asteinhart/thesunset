<script>
	import '../../app.css';
	import diagram from '$lib/images/diagram.png';
	import diagram_mobile from '$lib/images/diagram_mobile.png';
</script>

<main>
	<div class="header">
		<div class="header-left">
			<a href="https://austinsteinhart.com" class="author-link">Austin Steinhart</a>
		</div>
	</div>
	<div class="article">
		<div class="title-block">
			<div class="title">Never Miss the Sunset Again</div>
			<div class="subtitle">
				Using a small camera and some code, enjoy last nights' sunset every day, all day.
			</div>
			<p class="byline">By <a href="austinsteinhart.com">Austin Steinhart</a> | Summer 2025</p>
			<hr />
		</div>
		<div class="body">
			<div class="prose">
				<p>
					After missing the sunset one night and only seeing the splendor of it all over instagram
					later in the evening, I dreamed up a digital photo frame that displayed the best moment of
					the sunset from the previous night. Thus, each day the frame showed the best moment of the
					sunset from the previous night and after the current day's sunset finished, it updated for
					the next 24 hours with the most current sunset.
				</p>
				<p>
					A few years and a computer science degree later, this project has come alive. Click below
					to see the latest sunset or keep reading to learn more about how I made this project come
					to life.
				</p>
				<a href="/" class="sunset-button"> See the latest sunset </a>
				<p>With this project, I wanted to:</p>
				<ul>
					<li>Make something I thought was cool</li>
					<li>Build a full stack* app and not overcomplicate the design</li>
					<li>Learn a few new tools / technologies</li>
				</ul>

				<p>
					As someone newer to the engineering world, this was an opportunity to go through a full
					design and implementation. I look forward to hearing about improvements to the app!
				</p>

				<p>
					I used some tools I have enjoyed learning (Svelte, AWS), added on a few new ones
					(TypeScript, Raspberry Pi, OpenCV), and got some more practice writing object oriented
					code.
				</p>
			</div>
			<div class="section">How it works</div>
			<div class="works-img">
				<img src={diagram} alt="diagram of how the app works" />
			</div>

			<div class="subsection">1.Take snapshots of the sunset every day</div>
			<div class="prose">
				<p>
					A cron job runs on the Raspberry Pi each day at 4:00pm ET. Using the Python package
					<code>astral</code>, I check what the time the sunset is and take a picture using a
					Raspberry Pi every 2 minutes starting 20 minutes before the sunset and continuing for 20
					minutes after the sunset for a total of 20 images. I save these locally on the microSD
					card on the Raspberry Pi.
				</p>
			</div>

			<div class="subsection">2. Score each snapshot and save the best image</div>
			<div class="prose">
				<p>
					Using the Python packages <code>Pillow</code> (a fork of the no longer maintained original
					Python Imaging Library PIL) and <code>OpenCV</code>, I compute a series of metrics from
					simply what is the average amount of red in every pixel to what is the percentage of
					pixels that fall within color ranges for sunset hues. This is an area where a machine
					learning model could possibly be helpful but since we are simply comparing the same scene
					over time in this project, I believe this simpler approach yields acceptable results.
				</p>

				<p>
					After an image is selected, the best image is uploaded to an S3 bucket along with some
					metadata and the rest of the files are removed from the Raspberry Pi to ensure there are
					no memory issues down the road. AWS permissions are the trickiest part of an overall
					simple process, but LLMs are pretty good these days at explaining the process and creating
					the permission files needed.
				</p>

				<p>
					This project lent itself to an Object Oriented approach. I created a `SunsetDetector`
					class with adapters to change the scoring and saving methods. Thus, in the future if I
					want to explore new scoring methods or a different image storing platform, most of the
					code will stay the same and I will just have to change the underlying scoring and saving
					function used.
				</p>
			</div>
			<div class="subsection">3. Single Page Application with Svelte</div>
			<div class="prose">
				<p>
					As a dedicated fan of type hints in Python, this project was a good excuse to finally
					switch over to TypeScript from JavaScript. I also continued to build my experience with
					Svelte 5 spent some extra time learning more about AWS S3 configurations and permissions.
				</p>

				<p>
					Since the images are stored on S3, I can simply make the bucket public for read access
					(bots pls ignore) removing the need for any backend and allowing me to host the app on
					GitHub Pages for free. This was my first time hosting a Svelte app on GitHub pages and
					found the process straightforward once I understood the proper build configuration.
				</p>
			</div>
			<div class="section">Future Work</div>
			<div class="prose">
				<p>There are two main areas for improvement:</p>
				<ul>
					<li>
						Explore better methods to determine the "best" sunset. While my simple scoring system
						works, more sophisticated computer vision techniques or even a machine learning model
						trained on sunset aesthetics could improve selection quality.
					</li>
					<li>
						Find collaborators to run the pipeline in different cities and add their images to this
						workflow. This would create a network of sunset captures from across the world!
					</li>
				</ul>

				<p>
					I don't consider myself primarily a data scientist, but I have enough experience to know
					that a more robust analysis of color distribution, cloud formations, and overall
					composition could yield better results than my current metrics.
				</p>

				<p>
					However, this was primarily a short passion project to keep me busy before starting a new
					job, and it works pretty well as is. Once I actually get a digital picture frame, there
					will be some additional work to figure out how to automate picture uploads and display
					rotations.
				</p>
			</div>

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
	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid #ddd;
		font-weight: bold;
	}
	.author-link {
		font-family: 'Open Sans', sans-serif;
		font-size: 1.2rem;
		color: #333;
		text-decoration: none;
	}
	.article {
		padding: 2rem 1rem;
	}
	.title-block {
		width: 50%;
		margin: auto;
	}
	.title {
		font-family: 'Open Sans', sans-serif;
		font-size: 2.5rem;
		font-weight: bold;
		text-align: left;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		font-family: 'Open Sans', sans-serif;
		font-size: 1.3rem;
		text-align: left;
		margin-bottom: 1rem;
	}

	.byline {
		font-size: 0.9rem;
		margin: auto;
		margin-bottom: 1rem;
		color: #666;
	}

	.byline a {
		color: #666;
		text-decoration: none;
	}
	.byline a:hover {
		text-decoration: underline;
	}

	/* Add this to your existing style section */
	.sunset-button {
		display: block;
		padding: 8px 24px;
		margin: 20px auto;
		background: linear-gradient(to right, #fba58b, #fdf29a);
		color: #494949;
		text-decoration: none;
		border-radius: 8px;
		font-weight: bold;
		text-align: center;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		transition:
			transform 0.2s,
			box-shadow 0.2s;
		width: fit-content;
	}

	.sunset-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
	}

	.section {
		font-family: 'Open Sans', sans-serif;
		font-size: 1.5rem;
		font-weight: bold;
		margin: auto;
		margin-top: 2rem;
		margin-bottom: 1rem;
		width: 50%;
	}

	.subsection {
		font-family: 'Open Sans', sans-serif;
		font-size: 1.2rem;
		font-weight: bold;
		margin: auto;
		margin-top: 2rem;
		margin-bottom: 1rem;
		width: 50%;
	}

	.works-img {
		display: flex;
		justify-content: center;
	}

	.works-img img {
		width: 50%;
		margin: auto;
		display: block;
	}

	.body {
		line-height: 1.6;
	}

	.prose {
		width: 50%;
		margin: auto;
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
