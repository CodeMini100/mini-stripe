import { Charge, Customer, PaymentMethod } from '../types'; // replace with actual path to types

export class PaymentService {
  /**
   * Create a charge record and processes payment
   * @param {string} customerId - The id of the customer to charge
   * @param {number} amount - The amount to charge in the smallest currency unit (e.g cents for USD)
   * @param {PaymentMethod} paymentMethod - The payment method to use for the charge
   * @returns {Promise<Charge>} The charge record after the transaction has been processed
   */
  async createCharge(customerId: string, amount: number, paymentMethod: PaymentMethod): Promise<Charge> {
    // TODO: Add implementation for creating and processing a charge with error handling
    throw new Error('Not implemented');
  }

  /**
   * Initiates a refund and updates charge status
   * @param {string} chargeId - The id of the charge to refund
   * @returns {Promise<Charge>} The updated charge record after the refund
   */
  async refundCharge(chargeId: string): Promise<Charge> {
    // TODO: Add implementation for refunding a charge and updating charge status with error handling
    throw new Error('Not implemented');
  }
}

// TODO: Remember to import PaymentService where it needs to be used, or consider using dependency injection