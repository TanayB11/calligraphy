<script>
	import TextHighlighter from './TextHighlighter.svelte';

	let highlights = '';

	function applyHighlights(text) {
		return text.replace(/\n$/g, '\n\n').replace(/[A-Z].*?\b/g, '<mark></mark>');
	}

	function handleInput(event) {
		const text = event.target.value;
		const highlightedText = applyHighlights(text);
		highlights = highlightedText;
		console.log(highlightedText);
	}
</script>

<svelte:head>
	<title>Calligraphy</title>
	<meta name="description" content="Calligraphy - Helps you write" />
</svelte:head>

<main class="max-w-3xl mx-auto mt-20">
	<h1 class="text-6xl font-bold">Calligraphy ✍️</h1>

	<TextHighlighter />
</main>

<style>
	h1 {
		font-family: 'Canela Deck', serif;
	}
</style>
