---
url: "https://docs.polymarket.com/developers/proxy-wallet"
title: "Proxy wallet - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/proxy-wallet#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Overview](https://docs.polymarket.com/developers/proxy-wallet#overview)
- [Deployments](https://docs.polymarket.com/developers/proxy-wallet#deployments)

## [​](https://docs.polymarket.com/developers/proxy-wallet\#overview)  Overview

When a user first uses Polymarket.com to trade they are prompted to create a wallet. When they do this, a 1 of 1 multisig is deployed to Polygon which is controlled/owned by the accessing EOA (either MetaMask wallet or MagicLink wallet). This proxy wallet is where all the user’s positions (ERC1155) and USDC (ERC20) are held.Using proxy wallets allows Polymarket to provide an improved UX where multi-step transactions can be executed atomically and transactions can be relayed by relayers on the gas station network. If you are a developer looking to programmatically access positions you accumulated via the Polymarket.com interface, you can either continue using the smart contract wallet by executing transactions through it from the owner account, or you can transfer these assets to a new address using the owner account.

* * *

## [​](https://docs.polymarket.com/developers/proxy-wallet\#deployments)  Deployments

Each user has their own proxy wallet (and thus proxy wallet address) but the factories are available at the following deployed addresses on the **Polygon network**:

| **Address** | **Details** |
| --- | --- |
| [0xaacfeea03eb1561c4e67d661e40682bd20e3541b](https://polygonscan.com/address/0xaacfeea03eb1561c4e67d661e40682bd20e3541b) | **Gnosis safe factory** – Gnosis safes are used for all MetaMask users |
| [0xaB45c5A4B0c941a2F231C04C3f49182e1A254052](https://polygonscan.com/address/0xaB45c5A4B0c941a2F231C04C3f49182e1A254052) | **Polymarket proxy factory** – Polymarket custom proxy contracts are used for all MagicLink users |

[Deployment and Additional Information](https://docs.polymarket.com/developers/CTF/deployment-resources) [Overview](https://docs.polymarket.com/developers/neg-risk/overview)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.