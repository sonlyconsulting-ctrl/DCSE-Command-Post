# CTJ Customer Product Card Experience

Task ID: SC-CTJ-COMMERCIAL-PACKAGING-PAYMENTS-20260912-16
Status: CANDIDATE UX CONTRACT

## Card anatomy

Every sellable CTJ product card should contain:

1. FAMILY / PRODUCT IDENTIFIER
2. PRODUCT TITLE
3. ONE-SENTENCE JOB
4. FORMAT / EFFORT
5. DELIVERABLE OR RESULT
6. A LA CARTE PRICE
7. MEMBERSHIP RELATIONSHIP
8. PRIMARY CTA
9. PAYMENT METHOD SCREEN
10. CONFIRMATION / ACCESS STATE

## Example card logic

Mental Ingenuity

PROVE YOUR THINKING UNDER PRESSURE

Six interactive chambers challenge evidence filtering, constraints, perspective, causal reasoning, contradiction, and adaptation.

Includes:
- six-chamber interactive ascent
- Reasoning Records
- final Reasoning Signature
- portable record/export

A la carte:
$29

Primary CTA:
BUY ONCE

Secondary eligibility:
MEMBER ACCESS, only when entitlement is actually verified

## Buy-once flow

BUY ONCE
-> Order Summary
-> Choose Payment Method
-> Cash App $SonlyConsulting OR PayPal @SonlyConsulting
-> Pay externally
-> Return and Confirm Payment
-> Payment submitted
-> SC verifies
-> Verification email
-> Access product

## Order summary screen

Display:
- product
- amount
- order ID
- buyer email
- payment selection
- concise fulfillment expectation

Do not display:
- fake "instant access" if verification is manual
- payment credentials
- unsupported payment-provider claims

## Payment-selection screen

Headline:
Choose how you want to pay

Options:
Cash App
$SonlyConsulting

PayPal
@SonlyConsulting

Instruction:
Use the exact order amount and include your order ID in the payment note when available.

CTA after external payment:
I'VE PAID - VERIFY MY PURCHASE

## Verification screen

Headline:
Payment submitted

Copy:
We have your order details. Access is released after the payment is matched and verified.

Show:
- order ID
- product
- amount
- method
- email

Do not call the order paid until merchant-side verification succeeds.

## Verified screen

Headline:
Payment verified

Show:
- product
- order ID
- access/start action
- confirmation-email notice

CTA:
START MY CTJ PRODUCT

## Customer experience principle

The user should never have to wonder:
- what they bought
- what they owe
- where to pay
- what reference to include
- whether payment was received
- whether it was verified
- where to start

The card is the beginning of the transaction experience, not merely a marketing tile.
