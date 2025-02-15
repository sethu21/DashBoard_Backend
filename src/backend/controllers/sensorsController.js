import { getSensorData as fetchSensorData } from '../models/sensorModel.js';

export const getSensorDataPort1 = async (req, res) => {
    try {
        const data = await fetchSensorData(1);
        res.json(data);
    } catch (error) {
        console.error("Error fetching sensor data for port1:", error);
        res.status(500).json({ error: error.message });
    }
};

export const getSensorDataPort2 = async (req, res) => {
    try {
        const data = await fetchSensorData(2);
        res.json(data);
    } catch (error) {
        console.error("Error fetching sensor data for port2:", error);
        res.status(500).json({ error: error.message });
    }
};

export const getSensorDataPort3 = async (req, res) => {
    try {
        const data = await fetchSensorData(3);
        res.json(data);
    } catch (error) {
        console.error("Error fetching sensor data for port3:", error);
        res.status(500).json({ error: error.message });
    }
};
