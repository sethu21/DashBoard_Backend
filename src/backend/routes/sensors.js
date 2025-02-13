import express from 'express';
import { getSensorData } from '../controllers/sensorsController.js';

const router = express.Router();

router.get('/:port', getSensorData); // Fetch data for a specific port

export default router;
