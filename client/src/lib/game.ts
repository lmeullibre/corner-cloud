import { createQuery } from '@tanstack/svelte-query';
import axios from 'axios';
import { gameStore } from './gameStore'; // Import the Svelte store
import { get } from 'svelte/store';
import { API_BASE_URL } from './user';
import type { Game } from './types';

export const fetchGame = async (slug: string): Promise<Game> => {
	const accessToken = localStorage.getItem('accessToken');
	if (!accessToken) {
		throw new Error('No access token found');
	}

	const response = await axios.get<Game>(`${API_BASE_URL}/api/games/${slug}/`, {
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});

	return response.data;
};

export const useGameQuery = (slug: string) => {
	console.log('slug', slug);
	// Get the initial data from the Svelte store, if available
	const initialData = get(gameStore);
	console.log('initial data', initialData);

	return createQuery<Game, Error>({
		queryKey: ['game', slug],
		queryFn: async () => {
			// If the game data is already in the store, return it directly
			if (initialData?.slug === slug) {
				return initialData;
			}
			// Otherwise, fetch the game data
			const fetchedGame = await fetchGame(slug);
			// Update the store with the fetched data
			gameStore.set(fetchedGame);
			return fetchedGame;
		},
		staleTime: 1000 * 60 * 5 // 5 minutes
	});
};
