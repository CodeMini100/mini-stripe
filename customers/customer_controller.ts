import { Request, Response } from "express";
import { Customer } from './customer_model'; // assuming there exists a Customer model file.

/**
 * Creates a new customer based on request data.
 * @param req - The incoming express request.
 * @param res - The outgoing express response.
 * @returns A promise representing the operation.
 */
export async function createCustomerHandler(req: Request, res: Response): Promise<void> {
    try {
        // TODO: validate req.body properties in here before creating the customer

        const newCustomer: Customer = new Customer(req.body); // assuming the Customer model has a constructor that handles properties

        // TODO: Save the newCustomer in the database

        // Send the created customer instance back in response
        res.status(201).json(newCustomer);
    } catch (error) {
        // Handle the error as per the application error handling guidelines
        res.status(500).json({ message: 'An error occurred while creating the customer', error });
    }
}


/**
 * Fetches a customer's details by their ID from the request parameters.
 * @param req - The incoming express request.
 * @param res - The outgoing express response.
 * @returns A promise representing the operation.
 */
export async function getCustomerHandler(req: Request, res: Response): Promise<void> {
    try {
        // TODO: Validate req.params.id before fetching the customer

        // TODO: Fetch customer from the database using the id

        // Send the fetched customer instance back in response
        res.status(200).json(customer);
    } catch (error) {
        // Handle the error as per the application error handling guidelines
        res.status(500).json({ message: 'An error occurred while fetching the customer', error });
    }
}