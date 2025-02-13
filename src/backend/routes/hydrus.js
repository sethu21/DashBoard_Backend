import express from 'express';
import { executeHydrus } from '../controllers/hydrusController.js';

const router = express.Router();

router.post('/run', executeHydrus);

export default router;
