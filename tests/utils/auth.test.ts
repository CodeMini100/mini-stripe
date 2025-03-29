import jwt from 'jsonwebtoken';
import { generateToken, verifyToken} from '../utils/auth';
import { UserDataType } from '../types/userDataType';

jest.mock('jsonwebtoken', () => ({
  sign: jest.fn(),
  verify: jest.fn(),
}));

const mockUser: UserDataType = {
    id: 1,
    name: "Mock User",
    email: "mock@example.com",
};

describe('Auth Utilities', () => {
  it('should create a token when generateToken is called', () => {
    const mockToken = 'mockToken';
    (jwt.sign as jest.Mock).mockReturnValue(mockToken);
    
    const token = generateToken(mockUser);

    expect(jwt.sign).toHaveBeenCalledWith(mockUser, 'A_KEY_OF_YOUR_CHOICE');
    expect(token).toEqual(mockToken);
  });

  it('should throw an error if generating token fails', () => {
    (jwt.sign as jest.Mock).mockImplementation(() => {throw new Error('Token not generated')});

    expect(() => {
        generateToken(mockUser);
    }).toThrowError(new Error('Failed to generate token: Token not generated'));
  });

  it('should return true when verifyToken is called with valid token', () => {
    (jwt.verify as jest.Mock).mockReturnValue(true);

    const result = verifyToken('mockToken');

    expect(jwt.verify).toHaveBeenCalledWith('mockToken', 'A_KEY_OF_YOUR_CHOICE');
    expect(result).toBe(true);
  });

  it('should throw an error when verifyToken is called with invalid token', () => {
    (jwt.verify as jest.Mock).mockImplementation(() => {
        throw new Error('Invalid token');
    });

    expect(() => {
        verifyToken('invalidToken');
    }).toThrowError(new Error('Failed to verify token: Invalid token'));
  });
});