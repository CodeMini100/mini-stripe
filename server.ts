import express from 'express';
import { Application } from 'express';

/**
 * Create and configure an Express server
 * 
 * @returns {Application} Express Application
 */
function createServer(): Application {
    const server: Application = express();

    // TODO: Add middleware and routes
    // server.use(...)
    // server.get(...)

    return server;
}

/**
 * Bind Express server to a port and handle incoming requests
 * 
 * @param {Application} server - Express Application
 * @param {number} port - Port number
 * 
 * @returns {void} 
 */
function startServer(server: Application, port: number): void {
    server.listen(port, () => {
        console.log(`Server started at http://localhost:${port}`);
    });

    server.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
        // Error handler
        // TODO: Implement error handling
        console.error(err.stack);
        res.status(500).send('Something broke!');
    });
}


// Use the functions
const server = createServer();
const PORT = process.env.PORT || 3000;

startServer(server, PORT);

export { createServer, startServer };