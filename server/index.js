import express from 'express';

const app = express();

const port = 3000;

app.listen(port, 'localhost', () => {
    console.log(`[server] Running on http://localhost:${port}`);
});