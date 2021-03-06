from gilded_rose.entities import Item, ItemType
from gilded_rose.entities.item_runner import ItemRunner

from gilded_rose.processors.legacy import LegacyProcessor
from gilded_rose.processors.quality import IncreaseQuality, DecreaseQuality, CapQualityOnMaximum, QualityIsNeverNegative, SetQualityTo
from gilded_rose.processors.conditional import WhenPastExpiration, WhenSellInPast
from gilded_rose.processors.sell_in import UpdateSellInDate


class ItemRunnerFactory:

    item_behaviour = {
        ItemType.legendary: [],

        ItemType.maturable: [IncreaseQuality(),
                             UpdateSellInDate(),
                             WhenPastExpiration(IncreaseQuality()),
                             CapQualityOnMaximum(),
                             QualityIsNeverNegative()],

        ItemType.common: [DecreaseQuality(),
                          UpdateSellInDate(),
                          WhenPastExpiration(DecreaseQuality()),
                          QualityIsNeverNegative()],

        ItemType.backstage_pass: [IncreaseQuality(),
                                  WhenSellInPast(11, IncreaseQuality()),
                                  WhenSellInPast(6, IncreaseQuality()),
                                  UpdateSellInDate(),
                                  WhenPastExpiration(SetQualityTo(0)),
                                  CapQualityOnMaximum(),
                                  QualityIsNeverNegative()],

        ItemType.conjured: [DecreaseQuality(2),
                            UpdateSellInDate(),
                            WhenPastExpiration(DecreaseQuality(2)),
                            QualityIsNeverNegative()]
    }

    @classmethod
    def from_item(cls, item: Item):
        item_type = cls._get_type_from_name(item.name)
        processors = cls.item_behaviour.get(item_type)

        return ItemRunner(item, processors)

    @classmethod
    def _get_type_from_name(cls, name: str) -> ItemType:
        if name == "Aged Brie":
            return ItemType.maturable
        if name == "Sulfuras, Hand of Ragnaros":
            return ItemType.legendary
        if name == "Backstage passes to a TAFKAL80ETC concert":
            return ItemType.backstage_pass
        if name == "Conjured":
            return ItemType.conjured
        return ItemType.common
