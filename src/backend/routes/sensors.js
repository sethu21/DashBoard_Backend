import express from 'express';
import { getSensorDataPort1, getSensorDataPort2, getSensorDataPort3 } from '../controllers/sensorsController.js';

const router = express.Router();

router.get('/port1', getSensorDataPort1);
router.get('/port2', getSensorDataPort2);
router.get('/port3', getSensorDataPort3);

export default router;
