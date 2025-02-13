import pool from '../database.js';
import { runPythonScript } from '../utils/runPython.js';

export const executeHydrus = async (req, res) => {
    try {
        console.log("Received request to /api/hydrus/run:", req.body);

        const port = parseInt(req.body.port, 10);
        if (![1, 2, 3].includes(port)) {
            return res.status(400).json({ error: "Invalid port number. Use 1, 2, or 3." });
        }

        console.log(`Fetching latest data from port${port}`);

        // Fetch latest sensor data
        const query = `SELECT water_content, soil_temp, bulk_ec FROM port${port} ORDER BY timestamp DESC LIMIT 1`;
        const { rows } = await pool.query(query);
        
        console.log("Query executed. Data fetched:", rows);

        if (rows.length === 0) {
            console.log("No data found for port", port);
            return res.status(404).json({ error: "No sensor data found for the specified port." });
        }

        // Extract data
        const { water_content, soil_temp, bulk_ec } = rows[0];
        console.log("Running HYDRUS with:", { water_content, soil_temp, bulk_ec });

        // Modify HYDRUS input
        await runPythonScript('src/backend/hydrus/modify_input.py', [JSON.stringify({ water_content, soil_temp, bulk_ec })]);

        // Run HYDRUS
        await runPythonScript('src/backend/hydrus/run_hydrus.py');

        // Process HYDRUS results
        const results = await runPythonScript('src/backend/hydrus/process_results.py');

        console.log("HYDRUS Results:", results);
        res.json({ success: true, results: JSON.parse(results) });
    } catch (error) {
        console.error("Error in executeHydrus:", error);
        res.status(500).json({ error: error.message });
    }
};
