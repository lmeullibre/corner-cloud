import axios from 'axios';
import { API_BASE_URL } from './user';

export type ConnectionDetails = {
	game_id: string;
};

export async function generateGuacamoleToken(
	connectionDetails: ConnectionDetails
): Promise<string> {
	try {
		const response = await axios.get(
			`${API_BASE_URL}/api/users/generate-guacamole-token/${connectionDetails.game_id}/`,
			{
				headers: {
					Authorization: `Bearer ${localStorage.getItem('accessToken')}`
				}
			}
		);
		return response.data.token;
	} catch (error) {
		throw new Error('Failed to generate Guacamole token');
	}
}
