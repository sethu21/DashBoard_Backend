import { getSensorData as fetchSensorData } from '../models/sensorModel.js';

export const getSensorData = async (req, res) => {
    try {
        const port = parseInt(req.params.port);
        if (![1, 2, 3].includes(port)) {
            return res.status(400).json({ error: "Invalid port number. Use 1, 2, or 3." });
        }
        
        const data = await fetchSensorData(port);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
