<script>
	export let popupMessage = '';
	export let popupVisible = false;
	export let handleAccept = () => {};
	export let handleReject = () => {};
</script>

{#if popupVisible}
	<div class="popup">
		<p>{popupMessage}</p>
		<button on:click={handleAccept}>Accept</button>
		<button on:click={handleReject}>Reject</button>
	</div>
{/if}

<style>
	.popup {
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
