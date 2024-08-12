import { createQuery, Query } from '@tanstack/svelte-query';
import axios from 'axios';
import { API_BASE_URL } from './user'; // Adjust the import based on where your API_BASE_URL is defined
import type { GameStatus } from './types';

export const fetchStatus = async (slug: string): Promise<GameStatus> => {
	const accessToken = localStorage.getItem('accessToken');
	if (!accessToken) {
		throw new Error('No access token found');
	}

	const response = await axios.get<GameStatus>(`${API_BASE_URL}/api/games/${slug}/check-status`, {
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});

	return response.data;
};

export const useFetchStatusQuery = (slug: string) => {
	return createQuery<GameStatus, Error>({
		queryKey: ['containerStatus', slug],
		queryFn: () => fetchStatus(slug),
		refetchInterval: (query: Query<GameStatus, Error, GameStatus>) => {
			const { data, error } = query.state;
			// Stop polling if there's an error or if the game is ready
			if (error || data?.status === 'ready' || data?.status === 'error') {
				return false; // Stop polling
			}
			return 5000; // Continue polling every 5 seconds if not ready
		}
	});
};
