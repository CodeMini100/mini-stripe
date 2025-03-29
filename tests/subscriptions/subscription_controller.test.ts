import { createSubscriptionHandler, cancelSubscriptionHandler } from '../subscriptions/subscription_controller';
import { Request, Response } from 'express';

describe('Subscription Controller', () => {
    let mockRequest: Partial<Request>;
    let mockResponse: Partial<Response>;

    beforeEach(() => {
        mockRequest = {
            body: {},
            params: {}
        };
        mockResponse = {
            status: jest.fn().mockReturnThis(),
            send: jest.fn()
        };
    });
    
    describe('createSubscriptionHandler', () => {

        test('should send 400 status when request body is undefined', async () => {
            mockRequest.body = undefined;

            await createSubscriptionHandler(mockRequest as Request, mockResponse as Response);

            expect(mockResponse.status).toHaveBeenCalledWith(400);
            expect(mockResponse.send).toHaveBeenCalledWith({ error: 'Invalid request body' });
        });

        test('should send 200 status when request body exists', async () => {
            mockRequest.body = { id: 1 };

            await createSubscriptionHandler(mockRequest as Request, mockResponse as Response);

            expect(mockResponse.status).toHaveBeenCalledWith(200);
            expect(mockResponse.send).toHaveBeenCalledWith({ message: 'Subscription created successfully' });
        });
    });

    describe('cancelSubscriptionHandler', () => {
        
        test('should send 400 status when request params id is undefined', async () => {
            mockRequest.params.id = undefined;

            await cancelSubscriptionHandler(mockRequest as Request, mockResponse as Response);

            expect(mockResponse.status).toHaveBeenCalledWith(400);
            expect(mockResponse.send).toHaveBeenCalledWith({ error: 'Invalid subscription id' });
        });

        test('should send 200 status when request params id exists', async () => {
            mockRequest.params.id = '123';

            await cancelSubscriptionHandler(mockRequest as Request, mockResponse as Response);

            expect(mockResponse.status).toHaveBeenCalledWith(200);
            expect(mockResponse.send).toHaveBeenCalledWith({ message: 'Subscription cancelled successfully' });
        });
    });
});