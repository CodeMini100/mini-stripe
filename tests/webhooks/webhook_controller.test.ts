import { webhookHandler, parseEvent } from '../webhooks/webhook_controller';
import { Response, Request } from 'express';
import { mocked } from 'ts-jest/utils';

jest.mock('express');

describe('webhookController', () => {
    let mockReq: Request;
    let mockRes: Response;
    let payload: any;
    let signature: any;

    beforeEach(() => {
        mockReq = {} as Request;
        mockRes = {} as Response;
        payload = { event: 'ping', data: { id: 1 } };
        signature = 'valid_signature';
        mocked(mockRes.status).mockImplementation(() => mockRes);
    });

    describe('webhookHandler', () => {
        it('should send 400 when parseEvent returns null', async () => {
            jest.spyOn(global as any, 'parseEvent').mockReturnValue(null);
            await webhookHandler(mockReq, mockRes);
            expect(mockRes.status).toHaveBeenCalledWith(400);
            expect(mockRes.send).toHaveBeenCalledWith('Invalid signature');
        });

        it('should send 200 when parseEvent returns an event data', async () => {
            jest.spyOn(global as any, 'parseEvent').mockReturnValue(payload);
            await webhookHandler(mockReq, mockRes);
            expect(mockRes.status).toHaveBeenCalledWith(200);
            expect(mockRes.send).toHaveBeenCalledWith('Successfully received event');
        });

        it('should send 500 when an error is thrown', async () => {
            jest.spyOn(global as any, 'parseEvent').mockImplementation(() => { throw new Error(); });
            await webhookHandler(mockReq, mockRes);
            expect(mockRes.status).toHaveBeenCalledWith(500);
            expect(mockRes.send).toHaveBeenCalledWith('Error processing webhook event');
        });
    });

    describe('parseEvent', () => {
        it('should return payload if signatures match', () => {
            const result = parseEvent(payload, signature);
            expect(result).toMatchObject(payload);
        });

        it('should return null if signatures do not match', () => {
            const result = parseEvent(payload, 'invalid_signature');
            expect(result).toBeNull();
        });

        it('should return null if an error is thrown', () => {
            const errorPayload = { event: 'error' };
            const result = parseEvent(errorPayload, signature);
            expect(result).toBeNull();
        });
    });
});