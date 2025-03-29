import { handleChargeSucceeded, handleSubscriptionRenewed } from '../webhooks/webhook_service'
import { Charge } from '../models/charge'
import { Subscription } from '../models/subscription'

jest.mock('../models/charge')
jest.mock('../models/subscription')

describe('webhook_service', () => {
    describe('handleChargeSucceeded', () => {
        it('successfully processes a successful charge event', async () => {
            const mockCharge = {id: 'abc123', update: jest.fn()}
            Charge.findById = jest.fn().mockResolvedValue(mockCharge)

            await handleChargeSucceeded({id: 'abc123', otherData: 'example'})

            expect(Charge.findById).toHaveBeenCalledWith('abc123')
            // expect(mockCharge.update).toHaveBeenCalledWith({otherData: 'example'}) Add this when update logic is implemented
        })

        it('throws error if charge not found', async () => {
            Charge.findById = jest.fn().mockResolvedValue(null)
            await expect(handleChargeSucceeded({id: 'abc123'})).rejects.toThrow('Charge with ID abc123 not found')
        })

        it('throws error if processing fails', async () => {
            Charge.findById = jest.fn().mockRejectedValue(new Error('Mock database error'))
            await expect(handleChargeSucceeded({id: 'abc123'})).rejects.toThrow('Failed to process charge succeeded event: Mock database error')
        })
    })

    describe('handleSubscriptionRenewed', () => {
        it('successfully processes a subscription renewal event', async () => {
            const mockSubscription = {id: 'abc123', update: jest.fn()}
            Subscription.findById = jest.fn().mockResolvedValue(mockSubscription)

            await handleSubscriptionRenewed({id: 'abc123', otherData: 'example'})

            expect(Subscription.findById).toHaveBeenCalledWith('abc123')
            // expect(mockSubscription.update).toHaveBeenCalledWith({otherData: 'example'}) Add this when update logic is implemented
        })

        it('throws error if subscription not found', async () => {
            Subscription.findById = jest.fn().mockResolvedValue(null)
            await expect(handleSubscriptionRenewed({id: 'abc123'})).rejects.toThrow('Subscription with ID abc123 not found')
        })

        it('throws error if processing fails', async () => {
            Subscription.findById = jest.fn().mockRejectedValue(new Error('Mock database error'))
            await expect(handleSubscriptionRenewed({id: 'abc123'})).rejects.toThrow('Failed to process subscription renewed event: Mock database error')
        })
    })
})