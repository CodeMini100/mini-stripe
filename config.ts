import * as dotenv from 'dotenv';
import * as fs from 'fs';

interface Config {
    DATABASE_URL: string,
    API_KEY: string,
    // Here, add other configuration parameters as required
};

// Define a default configuration to ensure there are fail-safes in case environment variables are missing
const defaultConfig = {
    DATABASE_URL: 'localhost',
    API_KEY: 'your-api-key',
    // Good practice to provide other necessary defaults too
};

/**
 * Load configuration from environment variables, if they're available, and merge them with defaults.
 *
 * @returns { Config } Configuration object
 */
export function loadConfig(): Config {
    // Load environment variables from .env file, ignore if not found
    try {
        dotenv.config();
    } catch(err) {
        console.warn('No .env file found. Loading config from environment.');
    }

    const config: Config = {
        DATABASE_URL: process.env.DATABASE_URL || defaultConfig.DATABASE_URL,
        API_KEY: process.env.API_KEY || defaultConfig.API_KEY,
        // Here, add other necessary configuration parameters
    };

    // Verify that configs are null detection are working properly
    for (const key in config) {
        if (Object.prototype.hasOwnProperty.call(config, key)) {
            const element = config[key as keyof Config];
            if (!element) {
                console.error(`Configuration load failed. ${key} is undefined.`);
                process.exit(1);
            }
        }
    }

    console.info('Config loaded successfully.');
    return config;
}