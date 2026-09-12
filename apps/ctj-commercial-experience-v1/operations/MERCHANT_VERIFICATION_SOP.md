# CTJ Merchant Verification SOP - Candidate

Task: SC-CTJ-COMMERCIAL-EXPERIENCE-BUILD-20260912-17
Status: CANDIDATE / MANUAL VERIFICATION

## Purpose

Define the human verification step between a customer's payment submission and any paid entitlement.

## Inputs

From customer order:
- order ID
- product
- amount
- customer email
- selected payment method
- payer name or handle
- transaction/reference ID

## Verify in authorized merchant interface

1. Sign in directly to the authorized Cash App or PayPal merchant/account interface.
2. Do not expose merchant passwords, MFA, recovery codes, API tokens, bank details, or private credentials to ChatGPT, GitHub, logs, email templates, or customer-facing code.
3. Find the transaction using the provider's authorized interface.
4. Confirm the recipient account is the intended Sonly Consulting merchant identity.
5. Confirm the amount equals the order amount.
6. Confirm the transaction/reference reconciles to the submitted order.
7. Confirm the transaction is completed rather than pending, reversed, cancelled, or otherwise unavailable.
8. Record only a non-secret verification receipt/reference suitable for audit.
9. Move the order to PAYMENT_VERIFIED only after these checks pass.
10. Fulfill access and send the approved verified-payment email.

## If the transaction cannot be reconciled

Move to PAYMENT_REVIEW.

Do not grant entitlement.

Contact the customer using the order email and order ID. Do not request payment passwords, card details, bank credentials, MFA codes, or recovery information.

## If payment is reversed or fails

Use PAYMENT_FAILED or PAYMENT_REVERSED as applicable.

Any already-created entitlement must follow the approved entitlement/revocation policy before change.

## Evidence

Material fulfillment should preserve:
- order ID
- product
- amount
- payment method
- verification timestamp
- non-secret verification receipt/reference
- fulfillment timestamp/reference
- operator identity or controlled execution receipt

No secret credential data belongs in the evidence record.
