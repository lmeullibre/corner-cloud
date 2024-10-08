<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';
	import Guacamole from 'guacamole-common-js';

	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { generateGuacamoleToken, type ConnectionDetails } from '$lib/GuacamoleTokenService';

	const GUACAMOLE_TUNNEL = import.meta.env.VITE_GUACAMOLE_TUNNEL;
	const loginMessage = writable('');

	const connectionStatus = writable('');

	let guacamoleClient: Guacamole.Client;
	let remoteDesktopContainer: HTMLElement;
	let cleanupKeyboardListeners: (() => void) | null = null;

	let slug: string = $page.params.slug;
	console.log(slug);
	onMount(() => {
		const connectionDetails: ConnectionDetails = {
			game_id: slug
		};
		generateAndInitializeGuacamole(connectionDetails);
	});

	onDestroy(() => {
		if (cleanupKeyboardListeners) {
			cleanupKeyboardListeners();
		}
		guacamoleClient?.disconnect();
	});

	async function generateAndInitializeGuacamole(connectionDetails: ConnectionDetails) {
		try {
			const token = await generateGuacamoleToken(connectionDetails);
			initializeGuacamoleClient(token);
			loginMessage.set('Login successful');
		} catch (error) {
			console.error('Error initializing remote desktop:', error);
			loginMessage.set('Login failed: Unable to initialize remote desktop.');
		}
	}

	const resizeDisplay = () => {
		if (guacamoleClient) {
			const display = guacamoleClient.getDisplay().getElement();
			const screenWidth = window.innerWidth;
			const screenHeight = window.innerHeight;
			guacamoleClient.getDisplay().scale(screenWidth / display.offsetWidth);
			display.style.width = `${screenWidth}px`;
			display.style.height = `${screenHeight}px`;
		}
	};

	function initializeGuacamoleClient(token: string) {
		guacamoleClient = new Guacamole.Client(
			new Guacamole.WebSocketTunnel(GUACAMOLE_TUNNEL + `?token=${encodeURIComponent(token)}`)
		);

		cleanupKeyboardListeners = setupKeyboardListeners();
		setupClientStateChangeListener();

		window.addEventListener('resize', resizeDisplay);
		resizeDisplay();

		guacamoleClient.connect();
	}

	function setupKeyboardListeners() {
		const keyboard = new Guacamole.Keyboard(document.body);
		keyboard.onkeydown = (keysym) => guacamoleClient?.sendKeyEvent(1, keysym);
		keyboard.onkeyup = (keysym) => guacamoleClient?.sendKeyEvent(0, keysym);

		return () => {
			keyboard.onkeydown = null;
			keyboard.onkeyup = null;
		};
	}

	function setupClientStateChangeListener() {
		guacamoleClient.onstatechange = (state) => {
			if (!remoteDesktopContainer) return;

			switch (state) {
				case Guacamole.Client.State.CONNECTED:
					connectionStatus.set('CONNECTED');

					const displayElement = guacamoleClient.getDisplay().getElement();
					displayElement.style.zIndex = '1';
					remoteDesktopContainer.appendChild(displayElement);
					guacamoleClient.getDisplay().showCursor(true);
					break;
				case Guacamole.Client.State.DISCONNECTED:
					connectionStatus.set('DISCONNECTED');

					remoteDesktopContainer.innerHTML = '';
					loginMessage.set('You successfully ended the session. Thanks for playing!');
					break;
				case Guacamole.Client.State.IDLE:
					remoteDesktopContainer.innerHTML = '';
					break;
			}
		};
	}
</script>

<main class="relative min-h-screen flex items-center justify-center">
	<div bind:this={remoteDesktopContainer} id="remote-desktop-container" class="z-10"></div>
	{#if $connectionStatus === 'DISCONNECTED'}
		<div
			class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center p-4 bg-opacity-80 rounded-lg"
		>
			<p class="text-lg">
				{$loginMessage}
			</p>
			<button
				class="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700"
				on:click={() => goto('/dashboard')}
			>
				Go to Dashboard
			</button>
		</div>
	{/if}
</main>
