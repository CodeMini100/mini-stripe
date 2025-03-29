import { Request, Response } from 'express';
import { createCustomerHandler, getCustomerHandler } from '../customers/customer_controller';
import { Customer } from '../customers/customer_model';

describe('Customer Controller', () => {
  let req: Request, res: Response, next: any;
  const someRandomError = new Error('some random error');

  beforeEach(() => {
    req = {
      body: {},
      params: {}
    } as any as Request;

    res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    } as any as Response;

    next = jest.fn();

    jest
      .spyOn(Customer.prototype, 'save')
      .mockImplementationOnce(() => Promise.resolve());

  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should create a customer and return 201 status', async () => {
    req.body = {
      name: 'John Doe',
      phoneNumber: '123456789',
      email: 'john.doe@mail.com'
    };

    await createCustomerHandler(req, res, next);

    expect(res.status).toHaveBeenCalledWith(201);
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining(req.body));
  });

  test('should handle error when saving a customer and return 500 status', async () => {
    req.body = {
      name: 'John Doe',
      phoneNumber: '123456789',
      email: 'john.doe@mail.com'
    };

    jest.spyOn(Customer.prototype, 'save').mockImplementationOnce(() => Promise.reject(someRandomError));

    await createCustomerHandler(req, res, next);

    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({
      message: 'An error occurred while creating the customer',
      error: someRandomError
    });
  });

  test('should fetch a customer and return 200 status', async () => {
    const returnedCustomerInfo = {
        id: '123',
        name: 'John Doe',
        phoneNumber: '123456789',
        email: 'john.doe@mail.com'
    };

    req.params.id = returnedCustomerInfo.id;

    jest.spyOn(Customer, 'findOne').mockImplementationOnce(() => Promise.resolve(returnedCustomerInfo));

    await getCustomerHandler(req, res, next);

    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining(returnedCustomerInfo));
  });

  test('should handle error when fetching a customer and return 500 status', async () => {
    req.params.id = '123';

    jest.spyOn(Customer, 'findOne').mockImplementationOnce(() => Promise.reject(someRandomError));

    await getCustomerHandler(req, res, next);

    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({
      message: 'An error occurred while fetching the customer',
      error: someRandomError
    });
  });
});