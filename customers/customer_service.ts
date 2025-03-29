import { Customer } from './models/customer';

/**
 * Data structure for creating a new customer.
 * Should align with the Customer model.
 */
interface NewCustomer {
  name: string;
  email: string;
  address: string;
}

/**
 * Inserts a new customer record into the database.
 * @param data - New customer data, in line with the NewCustomer interface
 * @returns The newly created Customer item or an error message if the creation failed
 * @throws {Error} Will throw an error if the input data is not valid or the DB operation fails
 */
export async function createCustomer(data: NewCustomer): Promise<Customer> {
  // TODO: Implement database logic here
  // If validation or DB operations fail, throw an error

  throw new Error('createCustomer function not implemented.');
}

/**
 * Retrieves a customer by ID from the database.
 * @param customerId - The ID of the sought customer
 * @returns The requested Customer item or an error message if no such customer is found
 * @throws {Error} Will throw an error if the input ID is not valid or the DB operation fails
 */
export async function getCustomerById(customerId: string): Promise<Customer> {
  // TODO: Implement database logic here
  // If validation or DB operations fail, throw an error

  throw new Error('getCustomerById function not implemented.');
}