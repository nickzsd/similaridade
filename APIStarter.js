import express from 'express';
import { spawn } from 'child_process';

const app = express();

const port = 3000;

function runPythonScript() {
    const pythonProcess = spawn("python", ["controller/similarity.py"]);

    let output = "";

    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Erro: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        console.log(`Processo Python finalizado com código ${code}`);
        console.log(`Saída do Python: ${output}`);
    });
}

runPythonScript();

app.get("/", (req, res) => {
    res.send("Servidor Express está funcionando!");
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
