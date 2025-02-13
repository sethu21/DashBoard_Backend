import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import sensorRoutes from './routes/sensors.js';
import hydrusRoutes from './routes/hydrus.js';

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());

// API Routes
app.use('/api/sensors', sensorRoutes);
app.use('/api/hydrus', hydrusRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
