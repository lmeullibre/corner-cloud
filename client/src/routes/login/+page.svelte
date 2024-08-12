<script lang="ts">
	import { createLoginMutation } from '$lib/login';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let username: string = '';
	let password: string = '';

	const { loginMutation, loginError } = createLoginMutation(goto);

	onMount(() => {
		// Clear error on component mount
		loginError.set('');
	});
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
	<div class="p-8 bg-white shadow-md rounded-md">
		<h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
		{#if $loginError}
			<div class="text-red-500 text-sm mb-4">{$loginError}</div>
		{/if}
		<div class="mb-4">
			<input
				type="text"
				class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
				placeholder="Username"
				bind:value={username}
				disabled={$loginMutation.status === 'pending'}
			/>
		</div>
		<div class="mb-4">
			<input
				type="password"
				class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
				placeholder="Password"
				bind:value={password}
				disabled={$loginMutation.status === 'pending'}
			/>
		</div>
		<div>
			<button
				class="w-full px-4 py-2 bg-indigo-500 text-white rounded-md hover:bg-indigo-600"
				on:click={() => $loginMutation.mutate({ username, password })}
				disabled={$loginMutation.status === 'pending' || !username || !password}
			>
				Login
			</button>
		</div>
		<div>
			{$loginMutation.status === 'pending'
				? 'Logging in...'
				: $loginMutation.status === 'error'
					? $loginMutation.error.message
					: ''}
		</div>
	</div>
</div>
