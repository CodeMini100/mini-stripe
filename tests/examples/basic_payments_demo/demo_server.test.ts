import { initDemoServer, demoCharge, demoRefund } from './demo_server';
import express from 'express';
import request from 'supertest';

describe('Demo Server', () => {
    let app: express.Application;

    beforeAll(() => {
        app = express();
    });

    test('initDemoServer()', () => {
        const consoleSpy = jest.spyOn(console, 'log');
        const oldListen = app.listen;
        app.listen = jest.fn((port, callback) => {
            // Call the callback immediately to mimic server started successfully
            callback();
            
            return oldListen.call(app, port);
        });

        initDemoServer();

        expect(consoleSpy).toHaveBeenCalledWith('Server started at http://localhost:3000');
        expect(app.listen).toHaveBeenCalledWith(3000, expect.any(Function));

        // Handle case where server fails to start
        app.listen = jest.fn(() => {
            throw new Error('Server start failure');
        });

        expect(initDemoServer).toThrow('Failed to start server: Server start failure');
    });

    describe('demoCharge()', () => {
        // Mock request and response objects
        const req = {
            body: {
                // example body data, adjust as needed.
                amount: 100,
                currency: 'usd',
                card: {
                    number: '4242424242424242',
                    exp_month: 12,
                    exp_year: 2023,
                    cvc: '123'
                }
            }
        } as express.Request;

        const res = {} as express.Response;

        test('should create a charge with valid request data', async () => {
            const mockCreateCharge = jest.fn();
            // Assuming paymentService is an imported service, we need to mock it
            const paymentService = {
                createCharge: mockCreateCharge
            };

            // Call function and check that the mock payment service was called correctly
            await demoCharge(req, res);
            expect(mockCreateCharge).toHaveBeenCalledWith(req.body);
        });
    });

    describe('demoRefund()', () => {
        // Mock request and response objects
        const req = {
            body: {
                // example body data, adjust as needed.
                chargeId: 'ch_1234567890'
            }
        } as express.Request;

        const res = {} as express.Response;

        test('should issue a refund with valid charge ID', async () => {
            const mockCreateRefund = jest.fn();
            // Assuming paymentService is an imported service, we need to mock it
            const paymentService = {
                createRefund: mockCreateRefund
            };

            // Call function and check that the mock payment service was called correctly
            await demoRefund(req, res);
            expect(mockCreateRefund).toHaveBeenCalledWith(req.body.chargeId);
        });
    });

});