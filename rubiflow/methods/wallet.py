"""
Rubika Digital Wallet, Balance, and Transfer methods.
"""

from typing import Any, Dict, List, Optional


class WalletMethods:
    """Methods for Rubika Wallet balance, money transfers, and cash-outs."""

    async def execute(self, method: str, input_data: Optional[Dict[str, Any]] = None, api_version: str = "6") -> Dict[str, Any]:
        raise NotImplementedError

    async def get_wallet_status(self) -> Dict[str, Any]:
        """Retrieves wallet balance and account status."""
        res = await self.execute("getWalletStatus", {})
        return res.get("data", {}).get("wallet", {})

    async def get_wallet_transactions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves recent wallet transaction history."""
        res = await self.execute("getWalletTransactions", {"limit": limit})
        return res.get("data", {}).get("transactions", [])

    async def transfer_credit(
        self,
        recipient_guid: str,
        amount: int,
    ) -> Dict[str, Any]:
        """Transfers balance between Rubika user accounts."""
        payload = {
            "recipient_guid": recipient_guid,
            "amount": amount,
        }
        return await self.execute("transferCredit", payload)

    async def cash_out(
        self,
        amount: int,
        sheba_iban: str,
    ) -> Dict[str, Any]:
        """Withdraws wallet funds to an Iranian Sheba (IBAN) bank account."""
        payload = {
            "amount": amount,
            "sheba": sheba_iban.replace("IR", "").strip(),
        }
        return await self.execute("cashOut", payload)

    async def get_wallet_currencies(self) -> List[Dict[str, Any]]:
        """Retrieves list of supported digital currencies."""
        res = await self.execute("getCurrencies", {})
        return res.get("data", {}).get("currencies", [])
