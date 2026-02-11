---
url: "https://docs.polymarket.com/developers/CTF/redeem"
title: "Reedeeming Tokens - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/CTF/redeem#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Conditional Token Frameworks

Reedeeming Tokens

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Once a condition has had it’s payouts reported (ie by the UMACTFAdapter calling `reportPayouts` on the CTF contract), users with shares in the winning outcome can redeem them for the underlying collateral. Specifically, users can call the `redeemPositions` function on the CTF contract which will burn all valuable conditional tokens in return for collateral according to the reported payout vector. This function has the following parameters:

- `collateralToken`: IERC20 - The address of the positions’ backing collateral token.
- `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being redeemed. Null in Polymarket case.
- `indexSets`: uint\[\] - The ID of the condition to redeem.
- `indexSets`: uint\[\] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A\|B and C but not A\|B and B\|C (is not disjoint). Each element’s a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A\|B, 0b010 is B, etc. In the Polymarket case 1\|2.

[Merging Tokens](https://docs.polymarket.com/developers/CTF/merge) [Deployment and Additional Information](https://docs.polymarket.com/developers/CTF/deployment-resources)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.