const { spawn } = require('child_process');

const pythonProcess = spawn('python', ['controller/similarity.py']);

pythonProcess.stdout.on('data', (data) => {
    console.log(`Saída: ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`Erro: ${data}`);
});

pythonProcess.on('close', (code) => {
    console.log(`Processo finalizado com código ${code}`);
});
