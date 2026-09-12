# CTJ Payment, Verification, and Fulfillment Flow

Task ID: SC-CTJ-COMMERCIAL-PACKAGING-PAYMENTS-20260912-16
Status: CANDIDATE FREE-COMPATIBLE FLOW

## Static payment methods

User-provided merchant identities:

Cash App
$SonlyConsulting

PayPal
@SonlyConsulting

Treat these identities as customer-facing payment labels.

Do not fabricate provider URLs from handles. The actual destination links must be verified before release.

## Why payment belongs inside packaging workflow

The product card is not complete when it only states a price.

A complete card must answer:
1. what the product is
2. who it is for
3. what is included
4. what it costs
5. how membership relates
6. how the buyer pays
7. what proof/confirmation is required
8. what happens after payment
9. when access is granted
10. what the buyer owns or may access later

Therefore packaging, pricing, checkout, verification, and fulfillment should be designed as one commercial workflow.

## Candidate free-compatible purchase flow

### Step 1: Product card

Customer chooses:
BUY ONCE

If member access applies:
MEMBER ACCESS is shown separately and only when entitlement is actually verified.

### Step 2: Order intent

Before external payment, create an order-intent record containing:
- order ID
- product ID
- product name
- price
- customer email
- timestamp
- selected payment method
- status = PAYMENT_PENDING

Do not collect payment credentials.

### Step 3: Payment method selection

Customer selects:
- Cash App: $SonlyConsulting
- PayPal: @SonlyConsulting

Display:
- exact amount
- order ID
- instruction to include the order ID in the payment note when the provider permits it
- return-to-confirmation action

### Step 4: Payment submission

After paying externally, customer returns to the confirmation screen.

Customer submits:
- order ID
- email used for purchase
- payer name or payment handle
- transaction/reference ID
- payment method

Screenshot should not be the primary verification evidence because screenshots can be altered.

If a screenshot is accepted as secondary evidence, it must not contain unnecessary financial or account information.

Status:
PAYMENT_SUBMITTED

### Step 5: Merchant verification

SC verifies the transaction inside the authorized Cash App or PayPal merchant/account interface.

The model/system does not receive merchant passwords, MFA, tokens, bank details, or private credentials.

Verify:
- recipient is correct
- amount matches
- transaction/reference matches
- payment is completed, not pending/reversed
- order ID/customer identity reasonably reconciles

Status after success:
PAYMENT_VERIFIED

If unmatched:
PAYMENT_REVIEW

If rejected/reversed:
PAYMENT_FAILED or PAYMENT_REVERSED

### Step 6: Fulfillment

Only PAYMENT_VERIFIED creates the paid entitlement.

Fulfillment record contains:
- order ID
- product
- customer email
- payment method
- verification timestamp
- entitlement type
- fulfillment URL/reference
- Keeper state if applicable

No card/bank/payment credentials are stored.

### Step 7: Confirmation email

Subject:
Your Sonly Consulting CTJ purchase is verified

Required email elements:
- customer's purchased product
- amount
- order ID
- payment verified statement
- access/start link or access instructions
- what to keep for records
- support/reply instruction
- refund/cancellation terms link when approved
- privacy/terms link when approved

Do not email sensitive payment details.

### Step 8: Access

Candidate states:
- VERIFIED_PAID
- FULFILLED
- IN_PROGRESS
- COMPLETED
- KEEPER, when applicable

For membership:
separate entitlement state from payment/order state.

## Verification principle

Customer proof starts the verification process.
Merchant-side confirmation completes it.

Do not grant paid access based only on a customer-supplied screenshot or transaction claim.

## Later automation path

When a governed payment processor/webhook becomes available:
PAYMENT_PENDING -> provider payment event -> PAYMENT_VERIFIED -> entitlement -> email

The same order state model can remain in place.

This means the current manual flow is not throwaway work. It is the first implementation of the same commercial architecture.
