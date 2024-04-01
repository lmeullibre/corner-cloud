import { writable } from 'svelte/store';
import { browser } from '$app/environment'; // Import the browser check

function checkAuthentication(): boolean {
	// Check if running in the browser before accessing localStorage
	return browser ? !!localStorage.getItem('access_token') : false;
}

export const isAuthenticated = writable<boolean>(checkAuthentication());
export const accessToken = writable<string>(
	browser ? localStorage.getItem('access_token') || '' : ''
);

// Function to call when logging in successfully.
export function login(token: string): void {
	if (browser) {
		localStorage.setItem('access_token', token);
		isAuthenticated.set(true);
		accessToken.set(token);
	}
}

// Function to call when logging out.
export function logout(): void {
	if (browser) {
		localStorage.removeItem('access_token');
		isAuthenticated.set(false);
		accessToken.set('');
	}
}
