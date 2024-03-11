<script>
	import { onMount } from 'svelte';

	let textarea;
	let highlights;
	let container;
	let backdrop;

	onMount(() => {
		textarea.addEventListener('input', handleInput);
	});

	function handleInput() {
		// Auto-expand the textarea
		textarea.style.height = 'auto';
		textarea.style.height = `${textarea.scrollHeight}px`;

		// Auto-expand the container
		container.style.height = 'auto';
		container.style.height = `${textarea.scrollHeight}px`;

		// Auto-expand the backdrop
		backdrop.style.height = 'auto';
		backdrop.style.height = `${textarea.scrollHeight}px`;

		const text = textarea.value;
		const highlightedText = applyHighlights(text);
		highlights.innerHTML = highlightedText;
	}

	function applyHighlights(text) {
		return text.replace(/\n$/g, '\n\n').replace(/[A-Z].*?\b/g, '<mark>$&</mark>');
	}
</script>

<div class="container" bind:this={container}>
	<div class="backdrop" bind:this={backdrop}>
		<div class="highlights" bind:this={highlights}></div>
	</div>
	<textarea bind:this={textarea} name="text"
		>This demo shows how to highlight bits of text within a textarea. Alright, that's a lie. You
		can't actually render markup inside a textarea. However, you can fake it by carefully
		positioning a div behind the textarea and adding your highlight markup there. JavaScript takes
		care of syncing the content and scroll position from the textarea to the div, so everything
		lines up nicely. Hit the toggle button to peek behind the curtain. And feel free to edit this
		text. All capitalized words will be highlighted.</textarea
	>
</div>

<style>
	@import url(https://fonts.googleapis.com/css?family=Open+Sans);

	:global(*, *::before, *::after) {
		box-sizing: border-box;
	}

	:global(body) {
		margin: 30px;
		background-color: #f0f0f0;
	}

	.container,
	.backdrop,
	textarea {
		box-sizing: border-box;
		width: 460px;
		height: 180px;
	}

	.highlights,
	textarea {
		padding: 10px;
		font:
			20px/28px 'Open Sans',
			sans-serif;
		letter-spacing: 1px;
	}

	.container {
		display: block;
		margin: 0 auto;
		transform: translateZ(0);
		-webkit-text-size-adjust: none;
	}

	.backdrop {
		position: absolute;
		z-index: 1;
		border: 2px solid #685972;
		background-color: #fff;
		overflow: auto;
		pointer-events: none;
		transition: transform 1s;
	}

	.highlights {
		white-space: pre-wrap;
		word-wrap: break-word;
		color: transparent;
	}

	textarea {
		display: block;
		position: absolute;
		z-index: 2;
		margin: 0;
		border: 2px solid #74637f;
		border-radius: 0;
		color: #444;
		background-color: transparent;
		overflow: hidden; /* Disabled scrolling */
		resize: none;
		transition: transform 1s;
	}

	:global(mark) {
		border-radius: 3px;
		color: transparent;
		background-color: #b1d5e5;
	}

	:global(.perspective .backdrop) {
		transform: perspective(1500px) translateX(-125px) rotateY(45deg) scale(0.9);
	}

	:global(.perspective textarea) {
		transform: perspective(1500px) translateX(155px) rotateY(45deg) scale(1.1);
	}

	textarea:focus {
		outline: none;
		box-shadow: 0 0 0 2px #c6aada;
	}
</style>
