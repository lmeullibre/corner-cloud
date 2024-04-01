<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { isAuthenticated, logout as logoutStore } from '$lib/stores/authStore';
	import gameStore from '$lib/stores/gameStore';
	import type { Game } from '$lib/models/types';

	let username = 'User';
	let games: Game[] = [];

	onMount(() => {
		if (!$isAuthenticated) {
			goto('/');
		}

		gameStore.loadGames();
	});

	gameStore.subscribe((data) => {
		games = data;
	});

	const logout = () => {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		logoutStore();
		goto('/login');
	};

	const handleGameClick = (game: Game) => {
		if (!game.coming_soon) {
			goto(`/play?game_id=${game.id}`); // Append the game ID as a query parameter
		}
	};
</script>

<main class="min-h-screen bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white p-8">
	<div class="max-w-6xl mx-auto">
		<h1 class="text-3xl font-bold mb-6">Dashboard</h1>
		<p class="mb-6">Welcome, {username}! You have successfully logged in.</p>
		<div class="flex overflow-x-auto space-x-4 py-4">
			{#each games as game}
				<button
					class="flex-none w-60 h-40 bg-white dark:bg-gray-700 rounded-lg shadow-lg p-4 cursor-pointer hover:bg-blue-100 dark:hover:bg-gray-600"
					on:click={() => handleGameClick(game)}
					class:opacity-50={game.coming_soon}
					class:hover:bg-blue-100={!game.coming_soon}
					class:dark:hover:bg-gray-600={!game.coming_soon}
				>
					<h3 class="text-lg font-semibold">{game.name}</h3>
					<p class="text-sm">{game.coming_soon ? 'Coming Soon' : 'Available Now'}</p>
				</button>
			{/each}
		</div>
		<button
			on:click={logout}
			class="mt-4 px-4 py-2 bg-red-500 hover:bg-red-700 text-white font-semibold rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-75"
		>
			Log out
		</button>
	</div>
</main>
