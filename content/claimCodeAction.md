## `claimCodeActiom.py`

### Happy Path

Get the claim code from `http.args`
Lookup rows in `v_star_claim` that match the claim code
Present a confirmation form
- Name of star
- Email to claim

### Happy Path - OnSubmit

Create conformation email link
Send email
Leak send-email exceptions out to server as 500s
Respond with news of a successful email and a call to action


### Special Paths

#### No star found for claim code
Error response page, with email

#### Star already claimed
Error response page, with email

#### Multiple stars found code claim code (error)
Raise an exception as this is unexpected