import { createCustomer, getCustomerById } from '../customers/customer_service';
import { Customer } from '../models/customer';

// Mock customer data
const mockCustomer: Customer = {
  id: '123',
  name: 'John Doe',
  email: 'johndoe@example.com',
  address: '123 Street',
};

// Setup successful mock database interactions
jest.mock('../models/customer', () => ({
  create: jest.fn().mockResolvedValue(mockCustomer),
  findById: jest.fn().mockResolvedValue(mockCustomer),
}));

describe('CustomerService', () => {
  describe('createCustomer', () => {
    it('should successfully create a new customer', async () => {
      const data = {
        name: 'John Doe',
        email: 'johndoe@example.com',
        address: '123 Street',
      };

      const result = await createCustomer(data);

      expect(result).toEqual(mockCustomer);
    });

    it('should throw an error when data is invalid', async () => {
      const data = {
        name: '',
        email: '',
        address: '',
      };

      await expect(createCustomer(data)).rejects.toThrow('createCustomer function not implemented.');
    });
  });

  describe('getCustomerById', () => {
    it('should successfully retrieve a customer by id', async () => {
      const result = await getCustomerById('123');

      expect(result).toEqual(mockCustomer);
    });

    it('should throw an error when the id is invalid', async () => {
      await expect(getCustomerById('')).rejects.toThrow('getCustomerById function not implemented.');
    });
  });
});