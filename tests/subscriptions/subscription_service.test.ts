import { SubscriptionService } from '../subscriptions/subscription_service';

describe('SubscriptionService', () => {
    let service: SubscriptionService;

    beforeEach(() => {
        service = new SubscriptionService();
    });

    describe('createSubscription', () => {
        test('should correctly create a new subscription', () => {
            const newSubscription = service.createSubscription('customer_id1', 'plan_id1');
            expect(newSubscription).toHaveProperty('id');
            expect(newSubscription).toHaveProperty('status', 'active');
            expect(newSubscription).toHaveProperty('customerId', 'customer_id1');
            expect(newSubscription).toHaveProperty('planId', 'plan_id1');
        });
    });

    describe('cancelSubscription', () => {
        test('should correctly cancel a subscription', () => {
            const newSubscription = service.createSubscription('customer_id1', 'plan_id1');
            const cancelledSubscription = service.cancelSubscription(newSubscription.id);
            expect(cancelledSubscription).toHaveProperty('status', 'cancelled');
        });

        test('should throw error for invalid subscription id', () => {
            expect(() => {
                service.cancelSubscription('nonexistent_id');
            }).toThrowError('Subscription not found');
        });
    });

    describe('generateInvoice', () => {
        test('should correctly generate an invoice for active subscription', () => {
            const newSubscription = service.createSubscription('customer_id1', 'plan_id1');
            const invoice = service.generateInvoice(newSubscription.id);
            expect(invoice).toBe('Invoice generated');
        });

        test('should throw error for nonexistent or non-active subscription', () => {
            expect(() => {
                service.generateInvoice('nonexistent_id');
            }).toThrowError('Could not generate invoice for non-existent or non-active subscription');

            const newSubscription = service.createSubscription('customer_id1', 'plan_id1');
            service.cancelSubscription(newSubscription.id);
            expect(() => {
                service.generateInvoice(newSubscription.id);
            }).toThrowError('Could not generate invoice for non-existent or non-active subscription');
        });
    });
});