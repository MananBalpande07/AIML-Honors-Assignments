from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class PaymentProcessor(ABC):
    """Abstract base class defining the blueprint for all payment gateways."""

    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    @abstractmethod
    def validate_details(self, account_info: str) -> bool:
        pass

    @abstractmethod
    def execute_payment(self, amount: float, mode: str, account_info: str) -> dict:
        pass

    def create_receipt(self, gateway_name: str, amount: float, mode: str) -> dict:
        return {
            "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
            "gateway": gateway_name,
            "mode": mode,
            "amount": f"INR {amount:.2f}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "SUCCESS",
        }


class PayPalGateway(PaymentProcessor):
    """Concrete implementation for PayPal payment processing."""

    def validate_details(self, account_info: str) -> bool:
        return "@" in account_info or len(account_info.strip()) >= 10

    def execute_payment(self, amount: float, mode: str, account_info: str) -> dict:
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")
        if not self.validate_details(account_info):
            raise ValueError("Invalid PayPal email or card number provided.")

        print(f"[PayPal] Authenticating {mode} for merchant '{self.merchant_id}'...")
        return self.create_receipt("PayPal", amount, mode)


class PhonePeGateway(PaymentProcessor):
    """Concrete implementation for PhonePe payment processing."""

    def validate_details(self, account_info: str) -> bool:
        return "@" in account_info or (account_info.isdigit() and len(account_info) in (10, 16))

    def execute_payment(self, amount: float, mode: str, account_info: str) -> dict:
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")
        if not self.validate_details(account_info):
            raise ValueError("Invalid UPI ID, mobile number, or card details.")

        print(f"[PhonePe] Routing {mode} request via merchant '{self.merchant_id}'...")
        return self.create_receipt("PhonePe", amount, mode)


class GatewayFactory:
    """Factory class to instantiate the requested payment gateway."""

    _gateways = {
        "paypal": PayPalGateway,
        "phonepe": PhonePeGateway,
    }

    @classmethod
    def get_gateway(cls, provider: str, merchant_id: str) -> PaymentProcessor:
        gateway_cls = cls._gateways.get(provider.strip().lower())
        if not gateway_cls:
            supported = ", ".join(cls._gateways.keys())
            raise ValueError(f"Unsupported gateway '{provider}'. Available options: {supported}")
        return gateway_cls(merchant_id)


def run_payment_portal():
    print("=== Multi-Gateway Payment Engine ===")
    print("Available Gateways: PayPal | PhonePe")
    print("Supported Modes   : UPI | Card | NetBanking")

    try:
        provider = input("\nSelect Payment Gateway: ").strip()
        mode = input("Select Payment Mode (UPI/Card/NetBanking): ").strip()
        account_info = input("Enter UPI ID / Email / Card Number: ").strip()
        amount = float(input("Enter Amount (INR): ").strip())

        processor = GatewayFactory.get_gateway(provider, merchant_id="MERCH_AIML_07")
        receipt = processor.execute_payment(amount, mode, account_info)

        print("\n--- Payment Receipt ---")
        for key, value in receipt.items():
            print(f"{key.replace('_', ' ').title():<16}: {value}")

    except ValueError as err:
        print(f"\n[Transaction Failed] {err}")
    except Exception as exc:
        print(f"\n[System Error] Unexpected issue occurred: {exc}")


if __name__ == "__main__":
    run_payment_portal()