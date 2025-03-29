import { Request, Response } from 'express';
import { createChargeHandler, refundHandler } from './payment_controller';

describe('Payment Controller', () => {
    let req: Partial<Request>;
    let res: Partial<Response>;
    let status: jest.Mock;
    let json: jest.Mock;

    beforeEach(() => {
        status = jest.fn().mockReturnThis();
        json = jest.fn().mockReturnThis();
        res = { status, json };
        req = {};
    });

    describe('createChargeHandler', () => {

        it('should throw an error when chargeData is missing', () => {

            createChargeHandler(req as Request, res as Response);
            
            expect(status).toHaveBeenCalledTimes(1);
            expect(json).toHaveBeenCalledTimes(1);
            expect(status).toHaveBeenCalledWith(400);
            expect(json).toHaveBeenCalledWith({ error: 'Invalid charge data.' });

        });

        it('should process the charge when chargeData is valid', () => {
            req.body = { customerId: '123', amount: 1000, currency: 'usd', source: 'card_1J2WaSBG5BvmovIxOl6zv7Bv' };

            createChargeHandler(req as Request, res as Response);

            expect(status).toHaveBeenCalledWith(200);
            expect(json).toHaveBeenCalledWith({ message: 'Charge successfully created.' });

        });

    });

    describe('refundHandler', () => {

        it('should throw an error when refundData is missing', () => {

            refundHandler(req as Request, res as Response);
            
            expect(status).toHaveBeenCalledTimes(1);
            expect(json).toHaveBeenCalledTimes(1);
            expect(status).toHaveBeenCalledWith(400);
            expect(json).toHaveBeenCalledWith({ error: 'Invalid refund data.' });

        });

        it('should process the refund when refundData is valid', () => {
            req.body = { chargeId: 'ch_1J2WaSBG5BvmovIxRRlwwKlm' };

            refundHandler(req as Request, res as Response);

            expect(status).toHaveBeenCalledWith(200);
            expect(json).toHaveBeenCalledWith({ message: 'Refund successfully processed.' });

        });

    });
});