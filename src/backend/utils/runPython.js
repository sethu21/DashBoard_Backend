import { spawn } from 'child_process';

export const runPythonScript = (scriptPath, args = []) => {
    return new Promise((resolve, reject) => {
        console.log(`Running Python script: ${scriptPath} with args:`, args);

        const pythonProcess = spawn('python', [scriptPath, ...args]);

        let output = '';
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
            console.log(`Python Output: ${output}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data.toString()}`);
            reject(data.toString());
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(`Python script exited with code ${code}`);
                reject(`Script exited with code ${code}`);
            } else {
                resolve(output);
            }
        });
    });
};
