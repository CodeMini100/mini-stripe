import { Logger } from '../utils/logger';

describe('Logger', () => {
    
    let consoleMock: jest.SpyInstance;

    afterEach(() => {
        consoleMock.mockRestore();
    });

    describe('logDebug', () => {
        test('should log debug messages', () => {
            consoleMock = jest.spyOn(console, 'debug').mockImplementation();
            const message = 'debug message';

            Logger.logDebug(message);

            expect(consoleMock).toHaveBeenCalledWith(message);
        });
    });

    describe('logInfo', () => {
        test('should log info messages', () => {
            consoleMock = jest.spyOn(console, 'info').mockImplementation();
            const message = 'info message';
            
            Logger.logInfo(message);

            expect(consoleMock).toHaveBeenCalledWith(message);
        });
    });

    describe('logError', () => {
        test('should log error messages', () => {
            consoleMock = jest.spyOn(console, 'error').mockImplementation();
            const message = 'error message';
            
            Logger.logError(message);

            expect(consoleMock).toHaveBeenCalledWith(message);
        });
    });
});