import { loadDemoConfig } from '../examples/basic_payments_demo/demo_config';

describe('DemoConfig', () => {
    test('loadDemoConfig returns default values when env variables are not set', () => {
        const config = loadDemoConfig();
        expect(config.dbConnectionString).toBe('mongodb://local/demoDb');
        expect(config.port).toBe(4000);
        expect(config.environment).toBe('development');
        expect(config.otherSettings).toEqual({});
    });

    test('loadDemoConfig populated with environment variables', () => {
        process.env.DB_CONNECTION_STRING = 'mongodb://testDb';
        process.env.PORT = '5000';
        process.env.ENVIRONMENT = 'production';
        process.env.TEST_SETTING = 'testValue';

        const config = loadDemoConfig();
        expect(config.dbConnectionString).toBe('mongodb://testDb');
        expect(config.port).toBe(5000);
        expect(config.environment).toBe('production');
        expect(config.otherSettings.TEST_SETTING).toBe('testValue');
    });

    test('loadDemoConfig throws an error if an intrinsic type conversion fails', () => {
        process.env.PORT = 'notAnInteger';

        expect(() => {
            loadDemoConfig();
        }).toThrow();        
    });
});