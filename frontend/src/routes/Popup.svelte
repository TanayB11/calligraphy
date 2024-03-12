<script>
	export let popupMessage = '';
	export let popupVisible = false;
	export let handleAccept = () => {};
	export let handleReject = () => {};
	export let showActions = true; // New prop to control the visibility of action buttons
</script>

{#if popupVisible}
	<div class="popup">
		<p>{popupMessage}</p>
		{#if showActions}
			<!-- Conditionally render buttons based on showActions prop -->
			<button on:click={handleAccept}>Accept</button>
			<button on:click={handleReject}>Reject</button>
		{/if}
	</div>
{/if}

<style>
	.popup {
		width: 200px; /* Adjust the width as needed */
		position: absolute; /* Ensure this is absolute */
		transform: translate(-50%, 0); /* Adjust as needed for centering */
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		z-index: 10;
	}
	button {
		margin: 10px;
	}
</style>
