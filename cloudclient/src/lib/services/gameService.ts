import type { Game } from '$lib/models/types';

async function getGames(): Promise<Game[]> {
	try {
		const response = await fetch('http://localhost:8000/api/games/');
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const games: Game[] = await response.json();
		return games;
	} catch (error) {
		console.error('Failed to fetch games:', error);
		return []; // Return an empty array in case of error
	}
}

export { getGames };
