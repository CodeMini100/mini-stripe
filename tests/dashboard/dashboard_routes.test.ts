import { Request, Response } from 'express';
import { getDashboardHandler, getTransactionDetailsHandler } from '../dashboard/dashboard_routes';

describe('DashboardRoutes', () => {
    const mockResponse = () => {
        const res = {};
        res.status = jest.fn().mockReturnValue(res);
        res.json = jest.fn().mockReturnValue(res);
        return res;
    };

    describe('getDashboardHandler', () => {
        test('should handle valid request and return JSON response', () => {
            const req = {} as Request;
            const res = mockResponse();

            getDashboardHandler(req, res as unknown as Response);

            expect(res.json).toHaveBeenCalled();
        });

        test('should handle error and return 500 error code', () => {
            const req = {} as Request;
            const res = mockResponse();

            console.error = jest.fn();

            // Simulated situation where function fails to handle request.
            (global as any).dbFail = true;

            getDashboardHandler(req, res as unknown as Response);

            expect(res.status).toHaveBeenCalledWith(500);
            expect(res.json).not.toHaveBeenCalled();

            // Reset state
            (global as any).dbFail = false;
        });
    });

    describe('getTransactionDetailsHandler', () => {
        test('should handle valid request and return JSON response', () => {
            const req = { params: { id: '42' } } as Request;
            const res = mockResponse();

            getTransactionDetailsHandler(req, res as unknown as Response);

            expect(res.json).toHaveBeenCalled();
        });

        test('should handle error and return 500 error code', () => {
            const req = { params: { id: '42' } } as Request;
            const res = mockResponse();

            console.error = jest.fn();

            // Simulated situation where function fails to handle request.
            (global as any).dbFail = true;

            getTransactionDetailsHandler(req, res as unknown as Response);

            expect(res.status).toHaveBeenCalledWith(500);
            expect(res.json).not.toHaveBeenCalled();

            // Reset state
            (global as any).dbFail = false;
        });
    });
});