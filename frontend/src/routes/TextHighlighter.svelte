<script>
	import { onMount } from 'svelte';
	import Popup from './Popup.svelte';

	let textarea;
	let highlights;
	let container;
	let backdrop;
	let popupVisible = false;
	let popupMessage = '';
	let selectedText = '';

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

		document.addEventListener('keydown', async (e) => {
			if (e.key === 'S') {
				selectedText = window.getSelection().toString();
				if (selectedText) {
					const simileData = await fetchSimile(selectedText);
					showPopupWithMessage(`Simile: ${simileData.completion}`);
				}
			}
		});
	});

	async function fetchCritique(text) {
		const response = await fetch('http://localhost:8000/ml/critique_openai/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ prompt: text })
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		// Parse the 'completion' field from the response to get the actual critique data
		const critiqueData = JSON.parse(data.completion);
		console.log(critiqueData); // Log it to ensure it's structured as expected
		return critiqueData;
	}

	async function fetchSimile(text) {
		const response = await fetch('http://localhost:8000/ml/simile/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ prompt: text })
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	}

	async function fetchScene(text) {
		const response = await fetch('http://localhost:8000/ml/scene/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ prompt: text })
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	}

	async function fetchPOV(text) {
		const response = await fetch('http://localhost:8000/ml/pov/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ prompt: text })
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	}

	function debounce(func, wait) {
		let timeout;
		return function (...args) {
			const later = () => {
				clearTimeout(timeout);
				func(...args);
			};
			clearTimeout(timeout);
			timeout = setTimeout(later, wait);
		};
	}

	let debouncedFetchCritique = debounce(async () => {
		const text = textarea.value;
		try {
			const critiqueData = await fetchCritique(text);
			const highlightedText = applyHighlights(text, critiqueData);
			highlights.innerHTML = highlightedText;
			attachMarkEventListeners(); // Re-attach event listeners to marks
		} catch (error) {
			console.error('Failed to fetch critique:', error);
		}
	}, 3000); // 3000 milliseconds = 3 seconds

	async function handleInput() {
		// Auto-expand the textarea
		textarea.style.height = 'auto';
		const height = Math.max(textarea.scrollHeight, 180);
		textarea.style.height = `${height}px`;

		// Auto-expand the container
		container.style.height = `${height}px`;

		// Auto-expand the backdrop
		backdrop.style.height = `${height}px`;

		debouncedFetchCritique();
	}

	function applyHighlights(text, critiqueData) {
		let highlightedText = text;
		critiqueData.sentences.forEach((sentence) => {
			const { quote, critiques } = sentence;
			// Example: Change color based on critique type (simplified for brevity)
			const color = critiques.factChecking ? 'yellow' : 'lightblue';
			highlightedText = highlightedText.replace(
				quote,
				`<mark style="background-color: ${color};" data-critique="${critiques.description}">${quote}</mark>`
			);
		});
		return highlightedText;
	}

	function attachMarkEventListeners() {
		const marks = highlights.querySelectorAll('mark');
		marks.forEach((mark) => {
			mark.style.cursor = 'pointer';
			mark.addEventListener('click', () => {
				const critique = mark.getAttribute('data-critique');
				showPopupWithMessage(critique);
			});
		});
	}

	function showPopupWithMessage(message) {
		popupMessage = message;
		popupVisible = true;
	}

	function handleAccept() {
		console.log('Accepted');
		popupVisible = false;
	}

	function handleReject() {
		console.log('Rejected');
		popupVisible = false;
	}

	async function displaySimile() {
		if (selectedText) {
			const simileData = await fetchSimile(selectedText);
			showPopupWithMessage(`Simile: ${simileData.completion}`);
		}
	}

	async function displayScene() {
		if (selectedText) {
			const sceneData = await fetchScene(selectedText);
			showPopupWithMessage(`Scene: ${sceneData.completion}`);
		}
	}

	async function displayPOV() {
		if (selectedText) {
			const povData = await fetchPOV(selectedText);
			showPopupWithMessage(`POV: ${povData.completion}`);
		}
	}
</script>

<Popup {popupMessage} {popupVisible} onAccept={handleAccept} onReject={handleReject} />

<div class="container" bind:this={container}>
	<div class="backdrop" bind:this={backdrop}>
		<div class="highlights" bind:this={highlights}></div>
	</div>
	<textarea bind:this={textarea} name="text"></textarea>
	<div class="action-buttons">
		<div class="circle simile" on:click={displaySimile}></div>
		<div class="circle scene" on:click={displayScene}></div>
		<div class="circle pov" on:click={displayPOV}></div>
		<span class="label simile-label">Simile</span>
		<span class="label scene-label">Scene</span>
		<span class="label pov-label">POV</span>
	</div>
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
		cursor: pointer; /* Ensure marks are clickable */
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

	.instructions {
		margin-top: 10px;
		font-size: 14px;
		color: #666;
	}

	.action-buttons {
		position: absolute;
		right: -100px; /* Adjust based on layout */
		top: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.circle {
		width: 30px;
		height: 30px;
		border-radius: 50%;
		margin: 10px 0;
		cursor: pointer;
		transition: opacity 0.3s;
	}
	.simile {
		background-color: #007bff;
	}
	.scene {
		background-color: #6f42c1;
	}
	.pov {
		background-color: #e83e8c;
	}

	.label {
		opacity: 0;
		transition: opacity 0.3s;
		color: white;
		font-size: 14px;
		margin-left: 10px;
		white-space: nowrap;
	}
	.simile:hover ~ .simile-label,
	.scene:hover ~ .scene-label,
	.pov:hover ~ .pov-label {
		opacity: 1;
	}
</style>
