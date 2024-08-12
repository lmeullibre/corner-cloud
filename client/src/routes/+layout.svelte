<script lang="ts">
	import { QueryClientProvider } from '@tanstack/svelte-query';
	import queryClient from '$lib/queryClient';
	import '../app.css'; // Import the Tailwind CSS file
</script>

<QueryClientProvider client={queryClient}>
	<slot />
</QueryClientProvider>
