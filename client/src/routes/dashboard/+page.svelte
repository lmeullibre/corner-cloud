<script lang="ts">
	import { useUserQuery } from '$lib/user';
	import { useLaunchGameMutation } from '$lib/launchGameMutation';
	import { goto } from '$app/navigation'; // Import the goto function
	import type { Game } from '$lib/types';
	import { useGamesQuery } from '$lib/games';

	const userQuery = useUserQuery();
	const gamesQuery = useGamesQuery();

	const launchGameMutation = useLaunchGameMutation();
	async function handleCardClick(game: Game) {
		try {
			// Trigger the mutation to launch the game with the specific slug
			$launchGameMutation.mutateAsync(game.slug);

			// Navigate to the /play/{slug} route after starting the container
		} catch (error) {
			// Handle the error case, e.g., show an error message
			console.error(error);
		} finally {
			goto(`/play/${game.slug}`);
		}
	}
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
	<div class="p-8 bg-white shadow-md rounded-md w-full max-w-4xl">
		<h2 class="text-2xl font-bold mb-6 text-center">Dashboard</h2>

		<!-- User Query Section -->
		{#if $userQuery.isLoading}
			<div class="space-y-4">
				<div class="w-24 h-6 bg-gray-300 rounded-md mx-auto"></div>
				<div class="w-48 h-4 bg-gray-300 rounded-md mx-auto"></div>
				<div class="w-32 h-4 bg-gray-300 rounded-md mx-auto"></div>
			</div>
		{:else if $userQuery.error}
			<p class="text-red-500">Failed to load user data: {$userQuery.error.message}</p>
		{:else if $userQuery.data}
			<p class="text-center">Welcome, {$userQuery.data.first_name} {$userQuery.data.last_name}!</p>
		{/if}
		{#if $userQuery.isFetching}
			<p>Background Updating...</p>
		{/if}

		<!-- Games Query Section -->
		<h3 class="text-xl font-semibold mt-6 text-center">Your Games</h3>
		{#if $gamesQuery.isLoading}
			<p class="text-center">Loading games...</p>
		{:else if $gamesQuery.error}
			<p class="text-red-500 text-center">Failed to load games: {$gamesQuery.error.message}</p>
		{:else if $gamesQuery.data}
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
				{#each $gamesQuery.data as game}
					<div
						class="bg-white shadow-lg rounded-lg p-6 cursor-pointer hover:shadow-xl transition-shadow"
						on:click={() => handleCardClick(game)}
					>
						<h4 class="text-lg font-bold mb-2">{game.name}</h4>
						<p class="text-gray-600">{game.slug}</p>
					</div>
				{/each}
			</div>
		{/if}
		{#if $gamesQuery.isFetching}
			<p class="text-center mt-4">Updating game list...</p>
		{/if}
	</div>
</div>
