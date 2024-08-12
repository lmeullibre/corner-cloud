import axios from 'axios';
import { createQuery } from '@tanstack/svelte-query';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type User = {
	username: string;
	email: string;
	first_name: string;
	last_name: string;
	isStaff: boolean;
};

export const fetchUserData = async (): Promise<User> => {
	const accessToken = localStorage.getItem('accessToken');
	if (!accessToken) {
		throw new Error('No access token found');
	}

	const response = await axios.get(`${API_BASE_URL}/api/users/me/`, {
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});
	return response.data;
};

export const useUserQuery = () => {
	return createQuery<User, Error>({
		queryKey: ['user'],
		queryFn: fetchUserData
	});
};
