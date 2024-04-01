import { writable } from 'svelte/store';
import type { Game } from '$lib/models/types';
import { getGames } from '$lib/services/gameService';

const games = writable<Game[]>([]);

async function loadGames() {
	const fetchedGames = await getGames();
	games.set(fetchedGames);
}

export default {
	subscribe: games.subscribe,
	loadGames
};
