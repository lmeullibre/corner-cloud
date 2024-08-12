import { createMutation } from '@tanstack/svelte-query';
import axios from 'axios';
import { API_BASE_URL } from './user';

export const launchGame = async (slug: string) => {
	const accessToken = localStorage.getItem('accessToken');
	if (!accessToken) {
		throw new Error('No access token found');
	}
	const response = await axios.post(
		`${API_BASE_URL}/api/games/${slug}/launch/`,
		{},
		{
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		}
	);
	return response.data;
};

// Update the mutation to correctly handle arguments
export const useLaunchGameMutation = () => {
	return createMutation({
		mutationFn: launchGame
	});
};
