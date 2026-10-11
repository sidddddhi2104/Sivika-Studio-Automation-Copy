# Automation Test Plan - Sivika Studio

## Application scope (verified vs. unverified)
| Module | Verified on live site | Automated |
|---|---|---|
| Home `/` | Title "Welcome \| Sivika Studio", heading, tagline, Start Shopping -> `/register` | Yes |
| Register `/register` | Title "Register \| Sivika Art Studio", heading "Create Account", hero image, Register button, Login/Home links | Yes (negative paths only) |
| Login `/login` | Title "Login \| Sivika Art Studio", heading "Welcome Back", Login button, Register/Home links | Yes (negative paths; valid login opt-in) |
| Products, cart, checkout, orders | Not inspected (behind login) | **No - not assumed to exist** |

## Prioritisation
| Priority | Scenario | Reason |
|---|---|---|
| P1 | Page titles/headings, Start Shopping, nav links | Entry-point smoke checks, stable, repetitive |
| P1 | Login rejects invalid credentials | High-value security regression |
| P2 | Register rejects empty / malformed input | Guards the sign-up funnel without creating data |
| P2 | Hero image, direct URL access, Back button | Cheap regression coverage |
| P3 | Valid login (opt-in) | Needs a test account |

## Left for manual testing
Visual/aesthetic review, copy quality, real registration and payment flows (Razorpay-style gateways must not be automated against production), exploratory and usability testing, responsive layout review.
