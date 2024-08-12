import { createQuery } from '@tanstack/svelte-query';
import axios from 'axios';
import { API_BASE_URL } from './user';
import type { Game } from './types';

const fetchGames = async () => {
	const accessToken = localStorage.getItem('accessToken');
	if (!accessToken) {
		throw new Error('No access token found');
	}
	const response = await axios.get(`${API_BASE_URL}/api/games/`, {
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});
	return response.data;
};

export const useGamesQuery = () => {
	return createQuery<Game[], Error>({
		queryKey: ['games'],
		queryFn: fetchGames
	});
};
