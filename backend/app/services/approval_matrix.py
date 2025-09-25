from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ApprovalStep:
    roles: List[str]


# Amounts assumed in INR (Lac == 100,000)
MATRIX = [
    (0, 10000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
    ]),
    (10000, 20000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
    ]),
    (20000, 50000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
        ApprovalStep(['po']),
    ]),
    (50000, 100000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
        ApprovalStep(['po']),
    ]),
    (100000, 300000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
        ApprovalStep(['dfa', 'dor']),
    ]),
    (300000, 1000000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
        ApprovalStep(['dfa']),
        ApprovalStep(['dor']),
    ]),
    (1000000, 5000000, [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
        ApprovalStep(['pc']),
        ApprovalStep(['ed']),
        ApprovalStep(['dfa']),
        ApprovalStep(['dor']),
    ]),
    (5000000, float('inf'), [
        ApprovalStep(['cost_center_head']),
        ApprovalStep(['admin_team']),
        ApprovalStep(['finance']),
        ApprovalStep(['pc']),
        ApprovalStep(['pd']),
        ApprovalStep(['ed']),
        ApprovalStep(['dfa']),
        ApprovalStep(['dor']),
    ]),
]


def get_approval_steps(amount: float) -> List[ApprovalStep]:
    for lower, upper, steps in MATRIX:
        if lower <= amount < upper:
            return steps
    return MATRIX[-1][2]