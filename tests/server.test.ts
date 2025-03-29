import { Application, Request, Response, NextFunction } from 'express';
import { createServer, startServer } from './server';

jest.mock('express', () => {
  return () => ({
    use: jest.fn(),
    get: jest.fn(),
    listen: jest.fn((port: number, callback: Function) => callback())
  });
});

describe('createServer', () => {
  let server: Application;

  beforeEach(() => {
    server = createServer();
  });

  test('should call express', () => {
    expect(server).toBeDefined();
  });

  // You could also add more tests for your middleware and routes here
});

describe('startServer', () => {
  let server: Application;

  beforeEach(() => {
    server = createServer();
  });

  test('should call listen on server with correct port', () => {
    const port = 3000;
    startServer(server, port);
    expect(server.listen).toHaveBeenCalled();
    expect(server.listen).toHaveBeenCalledWith(port, expect.any(Function));
  });

  test('should add error handling middleware', () => {
    const port = 3000;
    startServer(server, port);

    const middleware = (server.use as jest.Mock).mock.calls[0][0];
    expect(middleware).toBeInstanceOf(Function);

    const err = new Error('Test error');
    const req = {} as Request;
    const res = {
      status: jest.fn().mockReturnThis(),
      send: jest.fn()
    } as unknown as Response;
    const next = jest.fn();

    middleware(err, req, res, next);

    expect(console.error).toHaveBeenCalledWith(err.stack);
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.send).toHaveBeenCalledWith('Something broke!');
    expect(next).not.toHaveBeenCalled();
  });

  test('should not call next function in error handler', () => {
    const port = 3000;
    startServer(server, port);

    const middleware = (server.use as jest.Mock).mock.calls[0][0];
    expect(middleware).toBeInstanceOf(Function);

    const err = new Error('Test error');
    const req = {} as Request;
    const res = {} as unknown as Response;
    const next = jest.fn();

    middleware(err, req, res, next);
    
    expect(next).not.toHaveBeenCalled();
  });
});