const express = require("express");
const { spawn } = require("child_process");

const app = express();

app.get("/run-python", (req, res) => {
    const pythonProcess = spawn("python", ["controller/similarity.py"]);

    let output = "";

    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Erro: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        console.log(`Processo finalizado com código ${code}`);
        res.send(`Saída do Python: ${output}`);
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});