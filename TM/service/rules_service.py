from uuid import uuid4

from ..rest.json import CreateRulesetInput
from ..repo import RulesetDTO, add_ruleset


def create_ruleset(ruleset: CreateRulesetInput):
    ruleset_id = uuid4()
    add_ruleset(RulesetDTO())
    return ruleset_id