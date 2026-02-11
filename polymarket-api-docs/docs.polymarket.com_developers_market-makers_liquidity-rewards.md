---
url: "https://docs.polymarket.com/developers/market-makers/liquidity-rewards"
title: "Liquidity Rewards - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/market-makers/liquidity-rewards#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Market Makers

Liquidity Rewards

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Overview](https://docs.polymarket.com/developers/market-makers/liquidity-rewards#overview)
- [Methodology](https://docs.polymarket.com/developers/market-makers/liquidity-rewards#methodology)
- [Equations](https://docs.polymarket.com/developers/market-makers/liquidity-rewards#equations)
- [Steps](https://docs.polymarket.com/developers/market-makers/liquidity-rewards#steps)

## [​](https://docs.polymarket.com/developers/market-makers/liquidity-rewards\#overview)  Overview

By posting resting limit orders, liquidity providers (makers) are automatically eligible for Polymarket’s incentive program. The overall goal of this program is to catalyze a healthy, liquid marketplace. We can further define this as creating incentives that:

- Catalyze liquidity across all markets
- Encourage liquidity throughout a market’s entire lifecycle
- Motivate passive, balanced quoting tight to a market’s mid-point
- Encourages trading activity
- Discourages blatantly exploitative behaviors

This program is heavily inspired by dYdX’s liquidity provider rewards which you can read more about [here](https://www.dydx.foundation/blog/liquidity-provider-rewards). In fact, the incentive methodology is essentially a copy of dYdX’s successful methodology but with some adjustments including specific adaptations for binary contract markets with distinct books, no staking mechanic a slightly modified order utility-relative depth function and reward amounts isolated per market. Rewards are distributed directly to the maker’s addresses daily at midnight UTC.

## [​](https://docs.polymarket.com/developers/market-makers/liquidity-rewards\#methodology)  Methodology

Polymarket liquidity providers will be rewarded based on a formula that rewards participation in markets (complementary consideration!), boosts two-sided depth (single-sided orders still score), and spread (vs. mid-market, adjusted for the size cutoff!). Each market still configure a max spread and min size cutoff within which orders are considered the average of rewards earned is determined by the relative share of each participant’s Qn in market m.

| Variable | Description |
| --- | --- |
| $ | order position scoring function |
| v | max spread from midpoint (in cents) |
| s | spread from size-cutoff-adjusted midpoint |
| b | in-game multiplier |
| m | market |
| m’ | market complement (i.e NO if m = YES) |
| n | trader index |
| u | sample index |
| c | scaling factor (currently 3.0 on all markets) |
| Qne | point total for book one for a sample |
| Qno | point total for book two for a sample |
| Spread% | distance from midpoint (bps or relative) for order n in market m |
| BidSize | share-denominated quantity of bid |
| AskSize | share-denominated quantity of ask |

## [​](https://docs.polymarket.com/developers/market-makers/liquidity-rewards\#equations)  Equations

**Equation 1:**S(v,s)=(v−sv)2⋅bS(v,s)= (\\frac{v-s}{v})^2 \\cdot bS(v,s)=(vv−s​)2⋅b**Equation 2:**Qone=S(v,Spreadm1)⋅BidSizem1+S(v,Spreadm2)⋅BidSizem2+…Q\_{one}= S(v,Spread\_{m\_1}) \\cdot BidSize\_{m\_1} + S(v,Spread\_{m\_2}) \\cdot BidSize\_{m\_2} + \\dots Qone​=S(v,Spreadm1​​)⋅BidSizem1​​+S(v,Spreadm2​​)⋅BidSizem2​​+…+S(v,Spreadm1′)⋅AskSizem1′+S(v,Spreadm2′)⋅AskSizem2′ \+ S(v, Spread\_{m^\\prime\_1}) \\cdot AskSize\_{m^\\prime\_1} + S(v, Spread\_{m^\\prime\_2}) \\cdot AskSize\_{m^\\prime\_2}+S(v,Spreadm1′​​)⋅AskSizem1′​​+S(v,Spreadm2′​​)⋅AskSizem2′​​**Equation 3:**Qtwo=S(v,Spreadm1)⋅AskSizem1+S(v,Spreadm2)⋅AskSizem2+…Q\_{two}= S(v,Spread\_{m\_1}) \\cdot AskSize\_{m\_1} + S(v,Spread\_{m\_2}) \\cdot AskSize\_{m\_2} + \\dots Qtwo​=S(v,Spreadm1​​)⋅AskSizem1​​+S(v,Spreadm2​​)⋅AskSizem2​​+…+S(v,Spreadm1′)⋅BidSizem1′+S(v,Spreadm2′)⋅BidSizem2′ \+ S(v, Spread\_{m^\\prime\_1}) \\cdot BidSize\_{m^\\prime\_1} + S(v, Spread\_{m^\\prime\_2}) \\cdot BidSize\_{m^\\prime\_2}+S(v,Spreadm1′​​)⋅BidSizem1′​​+S(v,Spreadm2′​​)⋅BidSizem2′​​**Equation 4:****Equation 4a:**If midpoint is in range \[0.10,0.90\] allow single sided liq to score:Qmin⁡=max⁡(min⁡(Qone,Qtwo),max⁡(Qone/c,Qtwo/c))Q\_{\\min} = \\max(\\min({Q\_{one}, Q\_{two}}), \\max(Q\_{one}/c, Q\_{two}/c))Qmin​=max(min(Qone​,Qtwo​),max(Qone​/c,Qtwo​/c))**Equation 4b:**If midpoint is in either range \[0,0.10) or (.90,1.0\] require liq to be double sided to score:Qmin⁡=min⁡(Qone,Qtwo)Q\_{\\min} = \\min({Q\_{one}, Q\_{two}})Qmin​=min(Qone​,Qtwo​)**Equation 5:**Qnormal=Qmin∑n=1N(Qmin)nQ\_{normal} = \\frac{Q\_{min}}{\\sum\_{n=1}^{N}{(Q\_{min})\_n}}Qnormal​=∑n=1N​(Qmin​)n​Qmin​​**Equation 6:**Qepoch=∑u=110,080(Qnormal)uQ\_{epoch} = \\sum\_{u=1}^{10,080}{(Q\_{normal})\_u}Qepoch​=∑u=110,080​(Qnormal​)u​**Equation 7:**Qfinal=Qepoch∑n=1N(Qepoch)nQ\_{final}=\\frac{Q\_{epoch}}{\\sum\_{n=1}^{N}{(Q\_{epoch})\_n}}Qfinal​=∑n=1N​(Qepoch​)n​Qepoch​​

## [​](https://docs.polymarket.com/developers/market-makers/liquidity-rewards\#steps)  Steps

1. Quadratic scoring rule for an order based on position between the adjusted midpoint and the minimum qualifying spread
2. Calculate first market side score. Assume a trader has the following open orders:

   - 100Q bid on m @0.49 (adjusted midpoint is 0.50 then spread of this order is 0.01 or 1c)
   - 200Q bid on m @0.48
   - 100Q ask on m’ @0.51

and assume an adjusted market midpoint of 0.50 and maxSpread config of 3c for both m and m’. Then the trader’s score is:Qne=((3−1)3)2⋅100+((3−2)3)2⋅200+((3−1)3)2⋅100Q\_{ne} = \\left( \\frac{(3-1)}{3} \\right)^2 \\cdot 100 + \\left( \\frac{(3-2)}{3} \\right)^2 \\cdot 200 + \\left( \\frac{(3-1)}{3} \\right)^2 \\cdot 100Qne​=(3(3−1)​)2⋅100+(3(3−2)​)2⋅200+(3(3−1)​)2⋅100QneQ\_{ne}Qne​ is calculated every minute using random sampling
3. Calculate second market side score. Assume a trader has the following open orders:

   - 100Q bid on m @0.485
   - 100Q bid on m’ @0.48
   - 200Q ask on m’ @0.505

and assume an adjusted market midpoint of 0.50 and maxSpread config of 3c for both m and m’. Then the trader’s score is:Qno=((3−1.5)3)2⋅100+((3−2)3)2⋅100+((3−.5)3)2⋅200Q\_{no} = \\left( \\frac{(3-1.5)}{3} \\right)^2 \\cdot 100 + \\left( \\frac{(3-2)}{3} \\right)^2 \\cdot 100 + \\left( \\frac{(3-.5)}{3} \\right)^2 \\cdot 200Qno​=(3(3−1.5)​)2⋅100+(3(3−2)​)2⋅100+(3(3−.5)​)2⋅200QnoQ\_{no}Qno​ is calculated every minute using random sampling
4. Boosts 2-sided liquidity by taking the minimum of QneQ\_{ne}Qne​ and QnoQ\_{no}Qno​, and rewards 1-side liquidity at a reduced rate (divided by c)Calculated every minute
5. QnormalQ\_{normal}Qnormal​ is the QminQ\_{min}Qmin​ of a market maker divided by the sum of all the QminQ\_{min}Qmin​ of other market makers in a given sample
6. QepochQ\_{epoch}Qepoch​ is the sum of all QnormalQ\_{normal}Qnormal​ for a trader in a given epoch
7. QfinalQ\_{final}Qfinal​ normalizes QepochQ\_{epoch}Qepoch​ by dividing it by the sum of all other market maker’s QepochQ\_{epoch}Qepoch​ in a given epoch this value is multiplied by the rewards available for the market to get a trader’s reward

Both min\_incentive\_size and max\_incentive\_spread can be fetched alongside full market objects via both the CLOB API and Markets API. Reward allocations for an epoch can be fetched via the Markets API.

[Trading](https://docs.polymarket.com/developers/market-makers/trading) [Maker Rebates Program](https://docs.polymarket.com/developers/market-makers/maker-rebates-program)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.