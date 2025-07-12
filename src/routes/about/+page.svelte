<script>
	import '../../app.css';
	import diagram from '$lib/images/diagram.png';
	import diagram_mobile from '$lib/images/diagram_mobile.png';
	import Header from '$lib/components/Header.svelte';

	let windowWidth = $state(0);
	let isMobile = $derived(windowWidth < 768);
</script>

<svelte:window bind:innerWidth={windowWidth} />

<svelte:head>
	<title>About the Last Night's Sunset</title>
	<meta
		name="description"
		content="About the Last Night's Sunset project, how it works, and the technologies used."
	/>
	<meta
		name="keywords"
		content="sunset, photography, computer vision, raspberry pi, daily sunset, automated photography"
	/>
	<meta name="author" content="Austin Steinhart" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta name="theme-color" content="#fba58b" />
	<meta name="robots" content="index, follow" />
	<link rel="canonical" href="https://thesunset.austinsteinhart.com/about" />

	<!-- Open Graph / Facebook -->
	<meta property="og:title" content="About the Last Night's Sunset" />
	<meta
		property="og:description"
		content="About the Last Night's Sunset project, how it works, and the technologies used."
	/>
	<meta property="og:image" content="https://thesunset.austinsteinhart.com/favicon.png" />
	<meta property="og:url" content="https://thesunset.austinsteinhart.com/about" />
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content="About the Last Night's Sunset" />
	<meta property="og:locale" content="en_US" />

	<!-- Twitter -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="About the Last Night's Sunset" />
	<meta
		name="twitter:description"
		content="Never miss the sunset again. View the best sunset photo from last night, captured automatically with computer vision scoring."
	/>
	<meta name="twitter:image" content="https://thesunset.austinsteinhart.com/favicon.png" />
</svelte:head>

<main>
	<Header />
	<div class="article">
		<div class="title-block">
			<div class="title">Never Miss the Sunset Again</div>
			<div class="subtitle">
				Using a small camera and some code, enjoy the sunset from last night every day, all day.
			</div>
			<p class="byline">By <a href="austinsteinhart.com">Austin Steinhart</a> | Summer 2025</p>
			<hr class="divider" />
		</div>
		<div class="body">
			<div class="prose">
				<p>
					After missing the sunset one night and only seeing its splendor over Instagram later in
					the evening, I dreamed up a digital photo frame that displayed the best moment of the
					sunset from the previous night. The frame would show the best moment of the sunset from
					the previous night, and after the current day's sunset finished, it would update for the
					next 24 hours with the most current sunset.
				</p>
				<p>
					A few years and one computer science degree later, this project has come alive. Click
					below to see the latest sunset or keep reading to learn more about how I made this project
					come to life.
				</p>
				<a href="/" class="sunset-button"> See the latest sunset </a>
				<p>With this project, I wanted to:</p>
				<ul class="list-disc list-inside">
					<li>Make something I thought was cool</li>
					<li>Build a full stack app and not overcomplicate the design</li>
					<li>Learn a few new tools / technologies</li>
				</ul>

				<p>
					As someone new to the engineering world, this was an opportunity to go through full design
					and implementation. I look forward to hearing about improvements to the app!
				</p>

				<p>
					I used some tools I have enjoyed learning (Svelte, AWS), added on a few new ones
					(TypeScript, Raspberry Pi, OpenCV), and got some more practice writing object-oriented
					code.
				</p>
			</div>
			<div class="section">How it works</div>
			<div class="works-img">
				<img src={isMobile ? diagram_mobile : diagram} alt="diagram of how the app works" />
			</div>

			<div class="subsection">1. Take snapshots of the sunset every day</div>
			<div class="prose">
				<p>
					Using the Python package <code>astral</code>, I check what the time of sunset is and
					schedule a Python script to run using the <code>schedule</code> package. The script takes a
					picture using a Raspberry Pi every 5 minutes starting 20 minutes before sunset and continuing
					for 20 minutes after sunset for a total of 9 images. I temporarily save these locally on the
					SD card on the Raspberry Pi.
				</p>
				<p>
					A short aside. Holy s*** was the Raspberry Pi a pain to get set up. A friend found one on
					the street and gave it to me so at least it was free. A short chronicle of my woes
					follows.
				</p>
				<p class="aside">
					Start by trying to download the OS on a provided SD card. The Raspberry Pi OS is now 5GB
					but the old SD card it came with only is 4GB. Get new SD card. Load on the OS. Plug in Pi,
					try to SSH in, nothing happens. Plug into a monitor to see whats happening. Confirm
					everything is working (yay) but realize you need to log in the first time meaning you need
					a keyboard. Track down a USB keyboard to log in. Log in (yay). Try to connect to WIFI and
					realize you have an old Pi that does not have a built in WIFI adapter. Realize your kit
					includes one. Plug in and connect to WIFI (yay) for two minutes. However, then adapter
					gets too hot and stops working. Get new WIFI adapter. Connect to WIFI again (yay).
					Generate SSH key for GitHub and clone repo (yay). Try to get UV working. Realize Pi does
					not play nice with UV. Eventually give up and just use venv. Have issue with new version
					of Python Imaging Library (PIL) called pillow, which seems to be a known issue. Find fix.
					Finally get everything working and can run the full script (yay).
				</p>
			</div>

			<div class="subsection">2. Score each snapshot and save the best image</div>
			<div class="prose">
				<p>
					Using the Python packages <code>Pillow</code> (a fork of the no longer maintained original
					Python Imaging Library PIL) and <code>OpenCV</code>, I compute a series of metrics, from
					simply the average amount of red in every pixel to the percentage of pixels that fall
					within color ranges for sunset hues. This is an area where a machine learning model could
					possibly be helpful, but since I'm simply comparing the same scene over time in this
					project, I believe this simpler approach yields acceptable results.
				</p>
				<p>Let's see some examples.</p>
			</div>

			<div class="diagram-container">
				<div class="diagram">
					<!-- Each row contains sun visualization with time label and image -->

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-1">
							<div class="time">20 min before Sunset</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-20m</div></div>
						<div class="thumbnail"><div class="placeholder-img">-20m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-2">
							<div class="time">15 min before</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-15m</div></div>
						<div class="thumbnail"><div class="placeholder-img">-15m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-3">
							<div class="time">10 min before</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-10m</div></div>
						<div class="thumbnail"><div class="placeholder-img">-10m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-4">
							<div class="time">5 min before</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">-5m</div></div>
						<div class="thumbnail"><div class="placeholder-img">-5m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-5">
							<div class="time">Sunset</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">Sunset</div></div>
						<div class="thumbnail"><div class="placeholder-img">Sunset</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-6">
							<div class="time">5 min after Sunset</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+5m</div></div>
						<div class="thumbnail"><div class="placeholder-img">+5m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-7">
							<div class="time">10 min after</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+10m</div></div>
						<div class="thumbnail"><div class="placeholder-img">+10m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-8">
							<div class="time">15 min after</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+15m</div></div>
						<div class="thumbnail"><div class="placeholder-img">+15m</div></div>
					</div>

					<div class="sunset-row">
						<div class="sunset-visual sun-pos-9">
							<div class="time">20 min after</div>
							<div class="horizon-line"></div>
							<div class="sun"></div>
						</div>
						<div class="thumbnail"><div class="placeholder-img">+20m</div></div>
						<div class="thumbnail"><div class="placeholder-img">+20m</div></div>
					</div>
				</div>
				<p class="diagram-caption">
					Camera captures images every 5 minutes from 20 minutes before to 20 minutes after sunset.
				</p>
			</div>
			<div class="prose">
				<p>
					After an image is selected, the best image is uploaded to an S3 bucket along with some
					metadata and the rest of the files are removed from the Raspberry Pi to ensure there are
					no memory issues down the road. AWS permissions are the trickiest part of an otherwise
					simple process, but LLMs are quite good these days at explaining the process and creating
					the permission files needed.
				</p>

				<p>
					This project lent itself to an object-oriented approach. I created a `SunsetDetector`
					class with adapters to modify the scoring and saving methods. Therefore, in the future if
					I want to explore new scoring methods or a different image storing platform, most of the
					code will stay the same and I will just have to change the underlying scoring and saving
					function used.
				</p>
			</div>
			<div class="subsection">3. Single Page Application with Svelte</div>
			<div class="prose">
				<p>
					As someone who loves type hints in Python, this project was a good excuse to finally
					switch over to TypeScript from JavaScript. I also continued to build my experience with
					Svelte 5 and spent some extra time learning more about AWS S3 configurations and
					permissions.
				</p>

				<p>
					Since the images are stored on S3, I can simply make the bucket public for read access
					(bots pls ignore), removing the need for a backend. Therefore, I can use a simple Svelte
					application to display the images and metadata. The Svelte app fetches the images from the
					S3 bucket and displays them on the page. I still have free credits from Heroku from a
					previous project, so I am hosting the Svelte app there.
				</p>
			</div>
			<div class="section">Future Work</div>
			<div class="prose">
				<p>There are two main areas for improvement:</p>
				<ul class="list-disc list-inside ml-4 space-y-2">
					<li>
						Explore better methods to determine the "best" sunset. While my simple scoring system
						works well, more sophisticated computer vision techniques or even a machine learning
						model trained on sunset aesthetics could improve selection quality.
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
					However, this was primarily a passion project to keep me busy before starting a new job,
					and it works pretty well as is. Once I actually get a digital picture frame, there will be
					some additional work to figure out how to automate picture uploads and display rotations.
				</p>
				<p>That's all for now, maybe I will do an update with an analysis</p>
			</div>
		</div>
		<a href="/" class="sunset-button"> See the latest sunset </a>
	</div>
</main>

<style>
	p {
		font-family: 'Public Sans', sans-serif;
		padding-block: 0.5rem;
	}

	.aside {
		font-style: italic;
		color: #555;
		margin-left: 1rem;
		font-size: small;
	}
	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid #ddd;
		font-weight: bold;
	}
	.author-link {
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
		font-size: 2.5rem;
		font-weight: bold;
		text-align: left;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		font-size: 1.3rem;
		text-align: left;
		margin-bottom: 0.5rem;
	}

	.byline {
		font-size: 0.9rem;
		margin: auto;
		color: #666;
	}

	.divider {
		margin-bottom: 0.5rem;
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
		margin-top: 1.5rem;
		margin-bottom: 0.5rem;
		width: 50%;
	}

	.subsection {
		font-family: 'Open Sans', sans-serif;
		font-size: 1.2rem;
		font-weight: bold;
		margin: auto;
		margin-top: 1rem;
		margin-bottom: 0.2rem;
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
		margin: auto;
		width: 60%;
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
		margin-bottom: 0.5rem;
		justify-content: center;
		gap: 1rem;
	}

	.sunset-visual {
		position: relative;
		height: 50px;
		width: 20%;
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
		.title-block {
			width: 90%;
		}
		.title {
			font-size: 1.8em;
		}
		.subtitle {
			font-size: 1rem;
			width: 100%;
		}
		.section,
		.subsection,
		.prose {
			width: 95%;
		}
		.works-img img {
			width: 95%;
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
