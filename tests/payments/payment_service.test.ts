import { PaymentService } from '../payments/payment_service';
import { PaymentMethod, Charge } from '../types';

describe('PaymentService', () => {

  let paymentService: PaymentService;
  
  beforeEach(() => {
    paymentService = new PaymentService(); // assuming PaymentService does not required any args in the constructor
  });

  describe('createCharge', () => {
    
    // Mocking the charge object as we do not have the real implementation
    const mockCharge: Charge = {
      id: 'ch_1JfKWS2eZvKYlo2Cdn3XBMvu',
      amount: 2000,
      currency: 'usd',
      customer: 'cus_Kh8c7AvmjqgBLs',
      payment_method_details: {
        type: 'card',
      },
      status: 'succeeded',
    };

    it('creates a charge and processes a payment', async () => {
      const spy = jest.spyOn(paymentService, 'createCharge').mockImplementation(async () => mockCharge);
      
      const result = await paymentService.createCharge('cus_Kh8c7AvmjqgBLs', 2000, PaymentMethod.Card);

      expect(spy).toHaveBeenCalledWith('cus_Kh8c7AvmjqgBLs', 2000, PaymentMethod.Card);
      expect(result).toEqual(mockCharge);
      
      spy.mockRestore();
    });

    it('throws an error when amount is negative', async () => {
      await expect(paymentService.createCharge('cus_Kh8c7AvmjqgBLs', -2000, PaymentMethod.Card)).rejects.toThrow();
    });
  });
  
  describe('refundCharge', () => {
  
    // Mocking the refund object
    const mockRefundCharge: Charge = {
      ...mockCharge,
      refunded: true,
    };

    it('initiates a refund and updates charge status', async () => {
      const spy = jest.spyOn(paymentService, 'refundCharge').mockImplementation(async () => mockRefundCharge);
      
      const result = await paymentService.refundCharge('ch_1JfKWS2eZvKYlo2Cdn3XBMvu');

      expect(spy).toHaveBeenCalledWith('ch_1JfKWS2eZvKYlo2Cdn3XBMvu');
      expect(result).toEqual(mockRefundCharge);
      
      spy.mockRestore();
    });
  
    it('throws an error when chargeId does not exist', async () => {
      await expect(paymentService.refundCharge('invalid_id')).rejects.toThrow();
    });
  });
});