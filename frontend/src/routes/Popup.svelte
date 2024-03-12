<script>
	export let message = '';
	export let visible = false;
	export let onAccept = () => {};
	export let onReject = () => {};
</script>

{#if visible}
	<div class="popup">
		<p>{message}</p>
		<button on:click={onAccept}>Accept</button>
		<button on:click={onReject}>Reject</button>
	</div>
{/if}

<style>
	.popup {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
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
