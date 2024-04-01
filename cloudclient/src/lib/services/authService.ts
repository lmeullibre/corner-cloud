interface LoginResponse {
	access: string;
	refresh: string;
}

export async function login(username: string, password: string): Promise<LoginResponse | null> {
	const apiBaseUrl: string | undefined = import.meta.env.VITE_API_BASE_URL;
	try {
		const response: Response = await fetch(`${apiBaseUrl}/api/token/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, password })
		});

		if (response.ok) {
			const data: LoginResponse = await response.json();
			return data;
		} else {
			console.error('Login failed');
			return null;
		}
	} catch (error) {
		console.error('Error logging in:', error);
		return null;
	}
}
