import axios from 'axios';
import { createMutation } from '@tanstack/svelte-query';
import { writable } from 'svelte/store';
import { goto } from '$app/navigation';

export type LoginResponse = {
	access: string;
	refresh: string;
};

export type LoginError = {
	detail: string;
};

export type LoginVariables = {
	username: string;
	password: string;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const login = async ({ username, password }: LoginVariables): Promise<LoginResponse> => {
	try {
		const response = await axios.post(
			`${API_BASE_URL}/api/users/login/`,
			{ username, password },
			{
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);

		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			const errorData: LoginError = error.response.data;
			throw new Error(errorData.detail || 'Login failed');
		}
		throw new Error('Login failed');
	}
};

export const createLoginMutation = (navigate: (url: string) => void) => {
	const loginError = writable<string>('');

	const loginMutation = createMutation<LoginResponse, Error, LoginVariables>({
		mutationFn: login,
		onSuccess: (data) => {
			console.log('Login successful', data);
			localStorage.setItem('accessToken', data.access);
			localStorage.setItem('refreshToken', data.refresh);
			navigate('/dashboard');
		},
		onError: (error: Error) => {
			loginError.set(error.message);
		}
	});

	return { loginMutation, loginError };
};
