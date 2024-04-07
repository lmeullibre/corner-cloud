<script lang="ts">
	import { goto } from '$app/navigation';
	import '../../app.css';
	import { login as loginService } from '../../lib/services/authService';
	import { login as loginStore, logout } from '../../lib/stores/authStore';

	let username: string = '';
	let password: string = '';
	let isRegistering = false;
	async function handleSubmit(): Promise<void> {
		const data = await loginService(username, password);
		if (data) {
			if (data) {
				// Assuming `data` contains `access` and `refresh` tokens
				localStorage.setItem('access_token', data.access);
				localStorage.setItem('refresh_token', data.refresh);

				loginStore(data.access); // Optionally update your store, if needed for client-side state

				console.log('Logged in successfully');
				goto('/dashboard'); // Redirect to the dashboard or another route
			} else {
				console.error('Login failed');
				// Optionally, update the UI to show an error message
			}
		} else {
			console.error('Login failed');
		}
	}
</script>

<main class="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
	<div class="w-full max-w-md mx-auto">
		<form
			on:submit|preventDefault={handleSubmit}
			class="max-w-lg mx-auto my-10 p-8 space-y-6 bg-white rounded-lg shadow-md dark:bg-gray-800 dark:text-gray-300"
		>
			<div>
				<label for="username" class="block text-lg font-medium text-gray-700 dark:text-gray-300"
					>Username</label
				>
				<div class="mt-1">
					<input
						id="username"
						name="username"
						type="text"
						required
						bind:value={username}
						class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-500"
						placeholder="Your username"
					/>
				</div>
			</div>

			<div>
				<label for="password" class="block text-lg font-medium text-gray-700 dark:text-gray-300"
					>Password</label
				>
				<div class="mt-1">
					<input
						id="password"
						name="password"
						type="password"
						required
						bind:value={password}
						class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-500"
						placeholder="••••••••"
					/>
				</div>
			</div>

			<div class="flex items-center justify-between">
				<div class="text-sm">
					<a
						href="#"
						class="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
					>
						Forgot your password?
					</a>
				</div>
			</div>

			<div>
				<button
					type="submit"
					class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-600"
				>
					<span class="absolute left-0 inset-y-0 flex items-center pl-3">
						<!-- Heroicons: login icon -->
					</span>
					Log in
				</button>
			</div>
		</form>
	</div>
</main>
