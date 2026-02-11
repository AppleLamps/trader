---
url: "https://docs.polymarket.com/developers/builders/builder-tiers"
title: "Builder Tiers - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/builders/builder-tiers#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Polymarket Builders Program

Builder Tiers

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Overview](https://docs.polymarket.com/developers/builders/builder-tiers#overview)
- [Feature Definitions](https://docs.polymarket.com/developers/builders/builder-tiers#feature-definitions)
- [Tier Comparison](https://docs.polymarket.com/developers/builders/builder-tiers#tier-comparison)
- [Unverified](https://docs.polymarket.com/developers/builders/builder-tiers#unverified)
- [Verified](https://docs.polymarket.com/developers/builders/builder-tiers#verified)
- [Partner](https://docs.polymarket.com/developers/builders/builder-tiers#partner)
- [Contact](https://docs.polymarket.com/developers/builders/builder-tiers#contact)
- [FAQ](https://docs.polymarket.com/developers/builders/builder-tiers#faq)
- [Next Steps](https://docs.polymarket.com/developers/builders/builder-tiers#next-steps)

## [​](https://docs.polymarket.com/developers/builders/builder-tiers\#overview)  Overview

Polymarket Builders lets anyone integrate without approval.
Tiers exist to manage rate limits while rewarding high performing integrations with weekly rewards and revenue sharing opportunities. Higher tiers also unlock engineering support, marketing promotion, and priority access.

## [​](https://docs.polymarket.com/developers/builders/builder-tiers\#feature-definitions)  Feature Definitions

| Feature | Description |
| --- | --- |
| **Daily Relayer Txn Limit** | Maximum Relayer transactions per day for Safe/Proxy wallet operations |
| **API Rate Limits** | Rate limits for non-relayer endpoints (CLOB, Gamma, etc.) |
| **Subsidized Transactions** | Gas fees subsidized for Relayer and CLOB operations via Safe/Proxy wallets |
| **Order Attribution** | Orders tracked and attributed to your Builder profile |
| **RevShare Protocol** | Infrastructure allowing Builders to charge fees |
| **Leaderboard Visibility** | Visibility on the [Builder leaderboard](https://builders.polymarket.com/) |
| **Weekly Rewards** | Weekly USDC rewards program for visible builders based on volume |
| **Telegram Channel** | Private Builders channel for announcements and support |
| **Badge** | Verified Builder affiliate badge on your Builder profile |
| **Engineering Support** | Direct access to engineering team |
| **Marketing Support** | Promotion via official Polymarket social accounts |
| **Weekly Rewards Boost** | Multiplier on the weekly USDC rewards program for visible builders |
| **Priority Access** | Early access to new features and products |

## [​](https://docs.polymarket.com/developers/builders/builder-tiers\#tier-comparison)  Tier Comparison

| Feature | Unverified | Verified | Partner |
| --- | --- | --- | --- |
| **Daily Relayer Txn Limit** | 100/day | 3,000/day | Unlimited |
| **API Rate Limits** | Standard | Standard | Highest |
| **Subsidized Transactions** | ✅ | ✅ | ✅ |
| **Order Attribution** | ✅ | ✅ | ✅ |
| **RevShare Protocol** | ❌ | ✅ | ✅ |
| **Leaderboard Visibility** | ❌ | ✅ | ✅ |
| **Weekly Rewards** | ❌ | ✅ | ✅ |
| **Telegram Channel** | ❌ | ✅ | ✅ |
| **Badge** | ❌ | ✅ | ✅ |
| **Engineering Support** | ❌ | Standard | Elevated |
| **Marketing Support** | ❌ | Standard | Elevated |
| **Weekly Reward Boosts** | ❌ | ❌ | ✅ |
| **Priority Access** | ❌ | ❌ | ✅ |

* * *

### [​](https://docs.polymarket.com/developers/builders/builder-tiers\#unverified)  Unverified

## 100 transactions/day

The default tier for all new builders. Create Builder API keys instantly from your Polymarket profile.

**How to get started:**

1. Go to [polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)
2. Create a builder profile and click **”\+ Create New”** to generate builder API keys
3. Implement [builder signing](https://docs.polymarket.com/developers/builders/order-attribution); required for Relayer access and CLOB order attribution

**Included:**

- Gasless trading on all CLOB orders through Safe/Proxy wallets
- Gas subsidized on all Relayer transactions through Safe/Proxy wallets up to daily limit
- Order attribution credit to your Builder profile
- Access to all client libraries and documentation

* * *

### [​](https://docs.polymarket.com/developers/builders/builder-tiers\#verified)  Verified

## 3,000 transactions/day

For builders who need higher throughput. Requires manual approval by Polymarket.

**How to upgrade:**Contact us with your Builder API Key, use case, expected volume, and relevant info (app, docs, X profile).**Unlocks over Unverified:**

- 15x daily Relayer transaction limit
- RevShare Protocol Access
- Telegram channel
- Leaderboard visibility
- Eligible for Weekly Rewards Program
- Promotion and verified affiliate badge from @PolymarketBuild

* * *

### [​](https://docs.polymarket.com/developers/builders/builder-tiers\#partner)  Partner

## Unlimited transactions/day

Enterprise tier for high-volume integrations and strategic partners.

**How to apply:**Reach out to discuss partnership opportunities.**Unlocks over Verified:**

- Unlimited Relayer transactions
- Highest API rate limits
- Elevated engineering support
- Elevated and coordinated marketing support
- Priority access to new features and products
- Multiplier on the Weekly Rewards Program

* * *

## [​](https://docs.polymarket.com/developers/builders/builder-tiers\#contact)  Contact

Ready to upgrade or have questions?

- [builder@polymarket.com](mailto:builder@polymarket.com)

* * *

## [​](https://docs.polymarket.com/developers/builders/builder-tiers\#faq)  FAQ

How do I know if I'm verified?

Verification is displayed in your [Builder Profile](https://polymarket.com/settings?tab=builder) settings.

What happens if I exceed my daily limit?

Relayer requests beyond your daily limit will be rate-limited and return an error. Consider upgrading to Verified or Partner tier if you’re hitting limits.

Can I get a temporary limit increase?

For special events or product launches, contact [builder@polymarket.com](mailto:builder@polymarket.com)

* * *

## [​](https://docs.polymarket.com/developers/builders/builder-tiers\#next-steps)  Next Steps

[**Get Your Builder Keys** \\
\\
Create Builder API credentials to get started](https://docs.polymarket.com/developers/builders/builder-profile) [**Use Your Builder Keys** \\
\\
Configure Builder API credentials to attribute orders](https://docs.polymarket.com/developers/builders/relayer-client)

[Builder Program Introduction](https://docs.polymarket.com/developers/builders/builder-intro) [Builder Profile & Keys](https://docs.polymarket.com/developers/builders/builder-profile)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.