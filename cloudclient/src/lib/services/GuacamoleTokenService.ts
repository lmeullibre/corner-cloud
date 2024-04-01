import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL; // Ensure this is set in your .env file

export interface ConnectionDetails {
	game_id: string;
}

export async function generateGuacamoleToken(
	connectionDetails: ConnectionDetails
): Promise<string> {
	try {
		const token = localStorage.getItem('access_token'); // Adjust according to where you store the token
		if (!token) {
			throw new Error('No access token found');
		}

		const url = new URL(`${API_URL}/api/generate-guacamole-token-expert/`);
		url.searchParams.append('game_id', connectionDetails.game_id); // Append the game_id as a query parameter

		const response = await axios.post(
			url.toString(),
			{},
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				}
			}
		);

		return response.data.guacamoleToken;
	} catch (error) {
		console.error('Error generating Guacamole token:', error);
		throw error;
	}
}
