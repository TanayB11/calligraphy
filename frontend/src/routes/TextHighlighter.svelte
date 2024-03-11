<script>
	import { onMount } from 'svelte';

	let textarea;
	let highlights;
	let container;
	let backdrop;

	onMount(() => {
		textarea.addEventListener('input', handleInput);
		textarea.addEventListener('focus', () => {
			textarea.style.pointerEvents = 'auto';
		});
		textarea.addEventListener('blur', () => {
			textarea.style.pointerEvents = 'none';
		});
		textarea.style.pointerEvents = 'none';

		// Dynamically manage pointer-events for marks
		textarea.addEventListener('mousemove', (e) => {
			const rect = textarea.getBoundingClientRect();
			const x = e.clientX - rect.left; // x position within the element.
			const y = e.clientY - rect.top; // y position within the element.
			const elementAtPoint = document.elementFromPoint(x, y);

			if (elementAtPoint && elementAtPoint.tagName === 'MARK') {
				textarea.style.pointerEvents = 'none';
			} else {
				textarea.style.pointerEvents = 'auto';
			}
		});

		textarea.addEventListener('mouseleave', () => {
			textarea.style.pointerEvents = 'auto';
		});
	});

	function handleInput() {
		// Auto-expand the textarea
		textarea.style.height = 'auto';
		const height = Math.max(textarea.scrollHeight, 180);
		textarea.style.height = `${height}px`;

		// Auto-expand the container
		container.style.height = `${height}px`;

		// Auto-expand the backdrop
		backdrop.style.height = `${height}px`;

		const text = textarea.value;
		const highlightedText = applyHighlights(text);
		highlights.innerHTML = highlightedText;
	}

	function applyHighlights(text) {
		const highlightedText = text.replace(/\n$/g, '\n\n').replace(/[A-Z].*?\b/g, '<mark>$&</mark>');

		// make all marks clickable
		const marks = highlights.querySelectorAll('mark');
		marks.forEach((mark) => {
			mark.addEventListener('click', () => {
				alert(mark.textContent);
			});
		});

		return highlightedText;
	}
</script>

<div class="container" bind:this={container}>
	<div class="backdrop" bind:this={backdrop}>
		<div class="highlights" bind:this={highlights}></div>
	</div>
	<textarea bind:this={textarea} name="text">This is a test</textarea>
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
		pointer-events: auto; /* Allow clicks to pass through to marks */
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
		pointer-events: auto; /* Re-enable pointer events when focused */
	}
</style>
