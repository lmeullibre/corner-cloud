<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { useFetchStatusQuery } from '$lib/gameStatusQuery';
	import { gameStore } from '$lib/gameStore';
	import { useGameQuery } from '$lib/game';

	const { slug } = $page.params; // Get the game slug from the route params
	const statusQuery = useFetchStatusQuery(slug);
	const gameQuery = useGameQuery(slug); // Fetch the game data using the slug

	// Update the store when the game data is fetched
	$: if ($gameQuery.isSuccess) {
		gameStore.set($gameQuery.data); // Update the store with the game's data
	}

	// Function to handle the Play button click
	function handlePlayClick() {
		goto(`/play/${slug}/game`);
	}

	$: if ($statusQuery.data?.status === 'ready') {
		console.log('Game is ready!');
	}
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
	<div class="p-8 bg-white shadow-md rounded-md">
		<h2 class="text-2xl font-bold mb-6 text-center">
			{#if $gameQuery.isLoading}
				Loading game data...
			{:else if $gameQuery.isError}
				Error: {$gameQuery.error?.message}
			{:else if $gameQuery.isSuccess}
				Playing: {$gameQuery.data.name}
			{/if}
		</h2>

		{#if $statusQuery.isLoading}
			<p>Loading status...</p>
		{:else if $statusQuery.isError}
			<p class="text-red-500">Error: {$statusQuery.error?.message}</p>
		{:else if $statusQuery.data}
			{#if $statusQuery.data.status === 'error'}
				<p class="text-red-500">Container does not exist or failed to retrieve status.</p>
			{:else if $statusQuery.data.status === 'starting'}
				<p>Container is starting...</p>
			{:else if $statusQuery.data.status === 'stopped'}
				<p class="text-red-500">The container has stopped unexpectedly.</p>
			{:else if $statusQuery.data.status === 'ready'}
				<p>Container is ready!</p>
				<!-- Display the Play button when the container is ready -->
				<div class="text-center mt-4">
					<button
						on:click={handlePlayClick}
						class="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700"
					>
						Play
					</button>
				</div>
			{/if}
		{/if}
	</div>
</div>
