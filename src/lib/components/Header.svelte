<div class="header">
	<a href="https://austinsteinhart.com" class="name-link">Austin Steinhart</a>
	<h1 class="title">
		<a href="/"
			>Last Night's <span class="sunset-word"
				>Sunset
				<div class="sunset-half-circle"></div></span
			></a
		>
	</h1>
	<a href="/about" class="about">About</a>
</div>

<style>
	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 2rem;
		position: relative;
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);
	}

	.name-link,
	.about {
		text-decoration: none;
		font-weight: 500;
		font-size: 1.1rem;
		color: black;
	}

	.name-link:hover,
	.about:hover {
		text-decoration: underline;
	}

	.title {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 600;
		position: absolute;

		left: 50%;
		transform: translateX(-50%);
	}

	.title a {
		text-decoration: none;
		color: inherit;
	}

	.title a:hover {
		text-decoration: none;
	}

	.sunset-word {
		position: relative;
		display: inline-block;
	}

	.sunset-half-circle {
		position: absolute;
		top: 40%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 80px;
		height: 40px;
		background: linear-gradient(to right, #fba58b, #fdf29a);
		border-radius: 40px 40px 0 0;
		z-index: -1;
		opacity: 0.8;
	}

	/* Mobile styles */
	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			padding: 1rem;
			gap: 0.5rem;
		}

		.title {
			position: static;
			transform: none;
			order: 1;
			font-size: 1.25rem;
		}

		.sunset-half-circle {
			width: 60px;
			height: 30px;
			border-radius: 30px 30px 0 0;
		}

		.name-link {
			order: 2;
			font-size: 1rem;
		}

		.about {
			order: 3;
			font-size: 1rem;
		}
	}

	/* Small mobile styles */
	@media (max-width: 480px) {
		.header {
			padding: 0.75rem;
		}

		.title {
			font-size: 1.1rem;
		}

		.sunset-half-circle {
			width: 50px;
			height: 25px;
			border-radius: 25px 25px 0 0;
		}

		.name-link,
		.about {
			font-size: 0.9rem;
		}
	}
</style>
