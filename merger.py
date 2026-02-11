"""
CTF (Conditional Token Framework) operations — merge and redeem.

Merge: YES + NO tokens → USDC (1:1)
  This is how you actually REALIZE arbitrage profits.
  After buying YES + NO for < $1.00, merge them back to get $1.00 USDC.

Redeem: Winning tokens → USDC (after market resolution)
  After a market resolves, redeem winning outcome tokens for collateral.

Note: These are on-chain operations on Polygon. They require gas (MATIC)
and interact directly with the CTF smart contract.
"""

import logging
from web3 import Web3
from config import Config

log = logging.getLogger("polyarb.merger")

# Contract addresses on Polygon mainnet
CTF_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# Neg-risk adapter
NEG_RISK_ADAPTER = "0xC5d563A36AE78145C45a50134d48A1215220f80a"

# Minimal ABI for mergePositions and redeemPositions
CTF_ABI = [
    {
        "inputs": [
            {"name": "collateralToken", "type": "address"},
            {"name": "parentCollectionId", "type": "bytes32"},
            {"name": "conditionId", "type": "bytes32"},
            {"name": "partition", "type": "uint256[]"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "mergePositions",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"name": "collateralToken", "type": "address"},
            {"name": "parentCollectionId", "type": "bytes32"},
            {"name": "conditionId", "type": "bytes32"},
            {"name": "indexSets", "type": "uint256[]"},
        ],
        "name": "redeemPositions",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"name": "account", "type": "address"},
            {"name": "id", "type": "uint256"},
        ],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]


class CTFMerger:
    """
    Handles on-chain merge and redeem operations for the Conditional Token Framework.

    Merge = the profit realization step in arb trading.
    After buying YES+NO tokens cheaply off the CLOB, merge them 1:1 back to USDC.
    """

    def __init__(self, cfg: Config, rpc_url: str | None = None):
        if rpc_url is None:
            rpc_url = "https://polygon-rpc.com"

        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.w3.eth.account.from_key(cfg.private_key)
        self.address = self.account.address
        self.chain_id = cfg.chain_id

        self.ctf = self.w3.eth.contract(
            address=Web3.to_checksum_address(CTF_ADDRESS),
            abi=CTF_ABI,
        )

        log.info("CTF Merger initialized for %s", self.address)

    def merge_positions(self, condition_id: str, amount: int) -> str | None:
        """
        Merge YES + NO tokens back into USDC.

        This is the profit realization step:
          - You bought YES+NO for < $1.00 via the CLOB
          - mergePositions burns 1 YES + 1 NO → gives back 1 USDC
          - Your profit = $1.00 - what you paid

        Args:
            condition_id: The market's condition ID (bytes32 hex)
            amount: Number of full sets to merge (in token units, 6 decimals for USDC)

        Returns:
            Transaction hash on success, None on failure
        """
        try:
            # Binary market partition: [1, 2] represents the two outcomes
            partition = [1, 2]
            parent_collection_id = bytes(32)  # null for Polymarket

            # Ensure condition_id is bytes32
            if isinstance(condition_id, str):
                if condition_id.startswith("0x"):
                    condition_bytes = bytes.fromhex(condition_id[2:])
                else:
                    condition_bytes = bytes.fromhex(condition_id)
            else:
                condition_bytes = condition_id

            tx = self.ctf.functions.mergePositions(
                Web3.to_checksum_address(USDC_ADDRESS),
                parent_collection_id,
                condition_bytes,
                partition,
                amount,
            ).build_transaction({
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "gas": 300000,
                "gasPrice": self.w3.eth.gas_price,
                "chainId": self.chain_id,
            })

            signed = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

            if receipt.status == 1:
                log.info("MERGE SUCCESS: %d sets merged | tx=%s", amount, tx_hash.hex())
                return tx_hash.hex()
            else:
                log.error("MERGE FAILED: tx=%s reverted", tx_hash.hex())
                return None

        except Exception as e:
            log.error("Merge error: %s", e, exc_info=True)
            return None

    def redeem_positions(self, condition_id: str) -> str | None:
        """
        Redeem winning tokens after market resolution.

        After a market resolves, the winning outcome tokens can be
        redeemed 1:1 for USDC.

        Args:
            condition_id: The market's condition ID (bytes32 hex)

        Returns:
            Transaction hash on success, None on failure
        """
        try:
            index_sets = [1, 2]
            parent_collection_id = bytes(32)

            if isinstance(condition_id, str):
                if condition_id.startswith("0x"):
                    condition_bytes = bytes.fromhex(condition_id[2:])
                else:
                    condition_bytes = bytes.fromhex(condition_id)
            else:
                condition_bytes = condition_id

            tx = self.ctf.functions.redeemPositions(
                Web3.to_checksum_address(USDC_ADDRESS),
                parent_collection_id,
                condition_bytes,
                index_sets,
            ).build_transaction({
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
                "chainId": self.chain_id,
            })

            signed = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

            if receipt.status == 1:
                log.info("REDEEM SUCCESS: tx=%s", tx_hash.hex())
                return tx_hash.hex()
            else:
                log.error("REDEEM FAILED: tx=%s reverted", tx_hash.hex())
                return None

        except Exception as e:
            log.error("Redeem error: %s", e, exc_info=True)
            return None

    def get_token_balance(self, token_id: str) -> int:
        """Check balance of a specific conditional token."""
        try:
            token_id_int = int(token_id)
            balance = self.ctf.functions.balanceOf(self.address, token_id_int).call()
            return balance
        except Exception as e:
            log.error("Balance check error: %s", e)
            return 0
