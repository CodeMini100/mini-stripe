/**
 * Interface for storing demo configuration
 */
interface DemoConfig {
    dbConnectionString: string,
    port: number,
    environment: "production" | "development" | "test",
    otherSettings: Record<string, unknown>
}

/**
 * Default demo configuration for testing.
 */
const defaultConfig: DemoConfig = {
    dbConnectionString: 'mongodb://local/demoDb',
    port: 4000,
    environment: 'development',
    otherSettings: {}
}

/**
 * Load or mocks the environment variables for the demo
 * @return {DemoConfig} The demo configuration
 */
export function loadDemoConfig(): DemoConfig {
    try {
        // Check if environment variables are set
        const dbConnectionString = process.env.DB_CONNECTION_STRING || defaultConfig.dbConnectionString;
        const port = process.env.PORT ? parseInt(process.env.PORT) : defaultConfig.port;
        const environment = process.env.ENVIRONMENT || defaultConfig.environment;

        // Load other settings from environment variables
        let otherSettings = { ...defaultConfig.otherSettings };
        Object.keys(otherSettings).forEach((key) => {
            otherSettings[key] = process.env[key.toUpperCase()] || otherSettings[key];
        });

        return {
            dbConnectionString,
            port,
            environment,
            otherSettings
        };
    } catch (error) {
        console.error(`Error loading demo config: ${error}`);
        process.exit(1);
    }
}