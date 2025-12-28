from dataclasses import dataclass, field
from typing import List

@dataclass
class CardModal:
    """
    Represents the expected state of a Trello Card after processing emails.
    """
    title: str
    description: str
    labels: List[str] = field(default_factory=List)

    def add_label(self, label: str):
        if label not in self.labels:
            self.labels.append(label)
    