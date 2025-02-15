import pool from '../database.js';

export const getSensorData = async (port) => {
    if (![1, 2, 3].includes(port)) {
        throw new Error("Invalid port number");
    }
    const query = `SELECT "timestamp", water_content, soil_temp, bulk_ec FROM port${port} ORDER BY "timestamp" DESC LIMIT 100`;
    const { rows } = await pool.query(query);
    return rows;
};
