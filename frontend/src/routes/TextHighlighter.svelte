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
	let caretPosition = 0;
	let showActions = false;

	onMount(() => {
		textarea.addEventListener('input', handleInput);
		textarea.addEventListener('keypress', checkCaretPosition);
		textarea.addEventListener('mousedown', checkCaretPosition);
		textarea.addEventListener('touchstart', checkCaretPosition);
		textarea.addEventListener('input', checkCaretPosition);
		textarea.addEventListener('paste', checkCaretPosition);
		textarea.addEventListener('cut', checkCaretPosition);
		textarea.addEventListener('mousemove', checkCaretPosition);
		textarea.addEventListener('select', checkCaretPosition);
		textarea.addEventListener('selectstart', checkCaretPosition);
		document.addEventListener('keydown', async (e) => {
			if (e.key === 'S') {
				selectedText = window.getSelection().toString();
				if (selectedText) {
					const simileData = await fetchSimile(selectedText);
					showPopupWithMessage(`Simile: ${simileData.completion}`, 0, 0, true); // Pass true to show action buttons
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
			const color = critiques.factChecking ? '#FFA07A' : 'lightblue';
			// get start and end index of quote
			const startIndex = textarea.value.indexOf(quote);
			const endIndex = startIndex + quote.length;
			highlightedText = highlightedText.replace(
				quote,
				`<mark style="background-color: ${color};" data-critique="${critiques.description}" data-start-index="${startIndex}" data-end-index="${endIndex}">${quote}</mark>`
			);
		});
		return highlightedText;
	}

	function attachMarkEventListeners() {
		const marks = highlights.querySelectorAll('mark');
		marks.forEach((mark) => {
			mark.style.cursor = 'pointer';
			mark.addEventListener('click', (event) => {
				const critique = mark.getAttribute('data-critique');
				const rect = mark.getBoundingClientRect();
				showPopupWithMessage(critique, rect.left, rect.bottom, false); // Pass false to hide action buttons
			});
			mark.addEventListener('mouseenter', (event) => {
				const critique = mark.getAttribute('data-critique');
				const rect = mark.getBoundingClientRect();
				showPopupWithMessage(critique, rect.left, rect.bottom + 20, false); // Use the left and bottom position of the mark, 20px below, pass false to hide action buttons
			});
		});
	}

	function showPopupWithMessage(message, x, y, sa = true) {
		showActions = sa;
		popupMessage = message;
		popupVisible = true;
		// Set the position of the popup
		document.querySelector('.popup').style.left = `${x}px`;
		document.querySelector('.popup').style.top = `${y}px`; // Adjusted to the new position
		// Update the Popup component to receive the showActions parameter
		// This might involve setting a reactive variable or store that the Popup component can access
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
			showPopupWithMessage(`Simile: ${simileData.completion}`, 0, 0, true); // Pass true to show action buttons
		}
	}

	async function displayScene() {
		if (selectedText) {
			const sceneData = await fetchScene(selectedText);
			showPopupWithMessage(`Scene: ${sceneData.completion}`, 0, 0, true); // Pass true to show action buttons
		}
	}

	async function displayPOV() {
		if (selectedText) {
			const povData = await fetchPOV(selectedText);
			showPopupWithMessage(`POV: ${povData.completion}`, 0, 0, true); // Pass true to show action buttons
		}
	}

	function checkCaretPosition() {
		console.log('stuff happening');
		const newPosition = textarea.selectionStart;
		if (newPosition !== caretPosition) {
			caretPosition = newPosition;
			console.log('caretPosition', caretPosition);
			printMarkAtCursor();
		}
	}

	function printMarkAtCursor() {
		const marks = highlights.querySelectorAll('mark');
		marks.forEach((mark) => {
			const startIndex = parseInt(mark.getAttribute('data-start-index'));
			const endIndex = parseInt(mark.getAttribute('data-end-index'));
			if (caretPosition >= startIndex && caretPosition <= endIndex) {
				const critique = mark.getAttribute('data-critique');
				const rect = mark.getBoundingClientRect();
				showPopupWithMessage(critique, rect.left, window.scrollY + rect.bottom, false); // Adjust for scrolling, pass false to hide action buttons
			}
		});
	}
</script>

<Popup {popupMessage} {popupVisible} {handleAccept} {handleReject} {showActions} />

<div class="container" bind:this={container}>
	<div class="backdrop" bind:this={backdrop}>
		<div class="highlights" bind:this={highlights}></div>
	</div>
	<textarea bind:this={textarea} name="text"></textarea>
	<div class="action-buttons">
		<button class="circle simile" on:click={displaySimile}></button>
		<button class="circle scene" on:click={displayScene}></button>
		<button class="circle pov" on:click={displayPOV}></button>
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
		background-color: #ffa07a;
		cursor: pointer; /* Ensure marks are clickable */
	}

	textarea:focus {
		outline: none;
		box-shadow: 0 0 0 2px #c6aada;
		pointer-events: auto; /* Re-enable pointer events when focused */
	}

	.action-buttons {
		position: absolute;
		right: 0px; /* Adjust based on layout */
		top: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: 0; /* Remove margin on top */
	}
	.circle {
		width: 20px; /* Make circles smaller */
		height: 20px; /* Make circles smaller */
		border-radius: 50%;
		margin: 5px 0; /* Decrease margin between circles */
		cursor: pointer;
		transition: opacity 0.3s;
		border: none;
		background-color: inherit;
		padding: 0;
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
		opacity: 0; /* Start as invisible */
		transition: opacity 0.3s;
		color: white; /* Default color, will be overridden */
		font-size: 14px;
		margin-left: 10px; /* Adjust as needed */
		white-space: nowrap;
		position: absolute; /* Position label next to the circle */
		right: -80px; /* Adjust based on layout */
	}
	.circle:hover + .label,
	.circle:focus + .label {
		opacity: 1; /* Show label on hover or focus */
	}
</style>
