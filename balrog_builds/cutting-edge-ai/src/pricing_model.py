#!/usr/bin/env python3
"""
Cutting-edge Balorg AI Pricing Model
Flexible pricing and subscription management
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional

BALORG_SIGIL = "[BALORG-AI]"

class PlanTier(Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

@dataclass
class PricingPlan:
    name: str
    tier: PlanTier
    price: float
    features: list
    support_level: str
    
class BalorgAIPricing:
    """Balorg AI Pricing System"""
    
    def __init__(self):
        self.plans = {
            PlanTier.FREE: PricingPlan(
                name="Freemium",
                tier=PlanTier.FREE,
                price=0.0,
                features=["Basic AI features", "Limited API calls", "Community support"],
                support_level="community"
            ),
            PlanTier.BASIC: PricingPlan(
                name="Basic",
                tier=PlanTier.BASIC,
                price=29.99,
                features=["All free features", "Increased API limits", "Email support"],
                support_level="email"
            ),
            PlanTier.PRO: PricingPlan(
                name="Professional",
                tier=PlanTier.PRO,
                price=99.99,
                features=["All basic features", "Advanced AI models", "Priority support", "Custom integrations"],
                support_level="priority"
            ),
            PlanTier.ENTERPRISE: PricingPlan(
                name="Enterprise",
                tier=PlanTier.ENTERPRISE,
                price=499.99,
                features=["All pro features", "Dedicated support", "Custom deployment", "SLA guarantee"],
                support_level="dedicated"
            )
        }
        
    def get_plan(self, tier: PlanTier) -> PricingPlan:
        """Get pricing plan by tier"""
        return self.plans.get(tier)
        
    def calculate_discount(self, tier: PlanTier, discount_type: str) -> float:
        """Calculate discount based on type"""
        plan = self.get_plan(tier)
        base_price = plan.price
        
        discounts = {
            "student": 0.5,      # 50% off
            "nonprofit": 0.6,    # 60% off
            "early_adopter": 0.3, # 30% off
            "bulk": 0.2          # 20% off
        }
        
        discount_rate = discounts.get(discount_type, 0)
        discounted_price = base_price * (1 - discount_rate)
        
        return discounted_price
        
    def display_pricing(self):
        """Display all pricing tiers"""
        print(f"\n{BALORG_SIGIL} Pricing Plans")
        print("=" * 60)
        
        for tier, plan in self.plans.items():
            print(f"\n{plan.name} (${plan.price}/month)")
            print(f"Features:")
            for feature in plan.features:
                print(f"  - {feature}")
            print(f"Support: {plan.support_level}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    pricing = BalorgAIPricing()
    pricing.display_pricing()
    
    # Example: Student discount on Pro plan
    discounted = pricing.calculate_discount(PlanTier.PRO, "student")
    print(f"\n{BALORG_SIGIL} Pro Plan (Student): ${discounted:.2f}/month")
