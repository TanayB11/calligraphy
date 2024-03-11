<script>
	let comment = '';
</script>

<svelte:head>
	<title>Calligraphy</title>
	<meta name="description" content="Calligraphy - Helps you write" />
</svelte:head>

<main class="max-w-3xl mx-auto mt-20">
	<h1 class="text-6xl font-bold">Calligraphy ✍️</h1>

	<div class="bg-white rounded-lg shadow-md overflow-hidden my-6">
		<div class="md:flex">
			<div class="w-full p-4 flex justify-between items-center">
				<textarea
					class="form-textarea mt-2 mx-4 block w-full text-gray-600 dark:text-gray-400 rounded-md"
					bind:value={comment}
				/>
				<div class="flex justify-between items-center">
					<div class="flex -space-x-1 overflow-hidden">
						<div class="flex flex-col -space-y-1">
							<span class="block h-2 w-2 rounded-full bg-purple-500"></span>
							<span class="block h-2 w-2 rounded-full bg-pink-500"></span>
							<span class="block h-2 w-2 rounded-full bg-orange-500"></span>
							<span class="block h-2 w-2 rounded-full bg-gray-500"></span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</main>

<style>
	h1 {
		font-family: 'Canela Deck', serif;
	}

	textarea {
		font-family: 'Canela Text Light', serif;
	}
</style>
