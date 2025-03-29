import { loadConfig } from './config';
import * as dotenv from 'dotenv';
import { mocked } from 'ts-jest/utils';

jest.mock('dotenv');

describe('config.ts', () => {
    beforeEach(() => {
        jest.resetModules();
        process.env = {};
    });

    test('loadConfig should load environment variables when .env file available', () => {
        mocked(dotenv.config).mockImplementation(() => {
            process.env.DATABASE_URL = 'test-db-url';
            process.env.API_KEY = 'test-api-key';
        });

        const config = loadConfig();

        expect(config).toEqual({
            DATABASE_URL: 'test-db-url',
            API_KEY: 'test-api-key'
        });

        expect(dotenv.config).toHaveBeenCalled();
    });

    test('loadConfig should load default config when .env file not available', () => {
        mocked(dotenv.config).mockImplementation(() => {
            throw new Error();
        });

        const config = loadConfig();

        expect(config).toEqual({
            DATABASE_URL: 'localhost',
            API_KEY: 'your-api-key'
        });

        expect(dotenv.config).toHaveBeenCalled();
    });

    test('loadConfig should exit process with error when config load failed', () => {
        const log = console.log;
        console.log = jest.fn();
        process.exit = jest.fn() as any as jest.Mock<void, [number?]>;

        const config = loadConfig();

        expect(process.exit).toHaveBeenCalledWith(1);
        expect(console.log).toHaveBeenCalledWith('Configuration load failed. API_KEY is undefined.');

        console.log = log;
    });
});