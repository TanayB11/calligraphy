<script>
	import TextHighlighter from './TextHighlighter.svelte';
</script>

<svelte:head>
	<title>Calligraphy</title>
	<meta name="description" content="Calligraphy - Helps you write" />
</svelte:head>

<main class="w-[460px] mx-auto mt-20">
	<h1 class="text-6xl font-bold mb-8 text-center">Calligraphy ✍️</h1>

	<TextHighlighter />
</main>

<style>
	h1 {
		font-family: 'Canela Deck', serif;
	}
</style>
