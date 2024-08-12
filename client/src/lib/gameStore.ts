import { writable } from 'svelte/store';
import type { Game } from './types';

// Create a writable store to hold the game data
export const gameStore = writable<Game | null>(null);
