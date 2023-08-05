from datetime import datetime, timedelta
from typing import Optional, Union, List, Dict, Iterator

from .items import Device
from .utils import Lookup
from .champion import Champion, Ability
from .enumerations import Language, DeviceType


class ChampionInfo:
    """
    Represents a collection of champions, cards, talents and shop items.

    Attributes
    ----------
    language : Language
        The language of this entry.
    """
    def __init__(
        self, language: Language, expires_at: datetime, champions_data: dict, items_data: dict
    ):
        self.language = language
        self._expires_at = expires_at
        sorted_devices: Dict[int, List[Device]] = {}
        for d in items_data:
            champ_list = sorted_devices.setdefault(d["champion_id"], [])
            champ_list.append(Device(d))
        self._devices: Lookup[Device] = Lookup(d for dl in sorted_devices.values() for d in dl)
        self._champions: Lookup[Champion] = Lookup(
            Champion(sorted_devices.get(c["id"], []), c) for c in champions_data
        )
        self._abilities: Lookup[Ability] = Lookup(
            a for c in self._champions for a in c.abilities
        )

    @property
    def champions(self) -> Iterator[Champion]:
        """
        An iterator that lets you iterate over all champions.

        Use ``list()`` to get a list instead.
        """
        return iter(self._champions)

    @property
    def abilities(self) -> Iterator[Ability]:
        """
        An iterator that lets you iterate over all champion's abilities.

        Use ``list()`` to get a list instead.
        """
        return iter(self._abilities)

    @property
    def devices(self) -> Iterator[Device]:
        """
        An iterator that lets you iterate over all devices (cards, talents and shop items).\n
        This also includes other devices that are returned from the API,
        but are considered invalid.

        Use ``list()`` to get a list instead.
        """
        return iter(self._devices)

    @property
    def cards(self) -> Iterator[Device]:
        """
        A filtered iterator that lets you iterate over all cards.

        Use ``list()`` to get a list instead.
        """
        dt = DeviceType["Card"]
        return filter(lambda d: d.type == dt, self._devices)

    @property
    def talents(self) -> Iterator[Device]:
        """
        A filtered iterator that lets you iterate over all talents.

        Use ``list()`` to get a list instead.
        """
        dt = DeviceType["Talent"]
        return filter(lambda d: d.type == dt, self._devices)

    @property
    def items(self) -> Iterator[Device]:
        """
        A filtered iterator that lets you iterate over all shop items.

        Use ``list()`` to get a list instead.
        """
        dt = DeviceType["Item"]
        return filter(lambda d: d.type == dt, self._devices)

    def get_champion(
        self, champion: Union[str, int], *, fuzzy: bool = False
    ) -> Optional[Champion]:
        """
        Returns a champion for the given Name or ID.
        Case sensitive.

        Parameters
        ----------
        champion : Union[str, int]
            The Name or ID of the champion you want to get.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Champion]
            The champion you requested.\n
            `None` is returned if a champion with the requested Name or ID couldn't be found.
        """
        return self._champions.lookup(champion, fuzzy=fuzzy)

    def get_card(self, card: Union[str, int], *, fuzzy: bool = False) -> Optional[Device]:
        """
        Returns a champion's card for the given Name or ID.
        Case sensitive.

        Parameters
        ----------
        card : Union[str, int]
            The Name or ID of the card you want to get.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Device]
            The card you requested.\n
            `None` is returned if a card with the requested Name or ID couldn't be found.
        """
        return self._devices.lookup(card, fuzzy=fuzzy)

    def get_talent(self, talent: Union[str, int], *, fuzzy: bool = False) -> Optional[Device]:
        """
        Returns a champion's talent for the given Name or ID.
        Case sensitive.

        Parameters
        ----------
        talent : Union[str, int]
            The Name or ID of the talent you want to get.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Device]
            The talent you requested.\n
            `None` is returned if a talent with the requested Name or ID couldn't be found.
        """
        return self._devices.lookup(talent, fuzzy=fuzzy)

    def get_item(self, item: Union[str, int], *, fuzzy: bool = False) -> Optional[Device]:
        """
        Returns a shop item for the given Name or ID.
        Case sensitive.

        Parameters
        ----------
        item : Union[str, int]
            The Name or ID of the shop item you want to get.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Device]
            The shop item you requested.\n
            `None` is returned if a shop item with the requested Name or ID couldn't be found.
        """
        return self._devices.lookup(item, fuzzy=fuzzy)


class DataCache:
    def __init__(self):
        self._cache: Dict[Language, ChampionInfo] = {}
        self.refresh_every = timedelta(hours=12)

    def _create_entry(self, language: Language, champions_data: dict, items_data: dict):
        expires_at = datetime.utcnow() + self.refresh_every
        self._cache[language] = ChampionInfo(language, expires_at, champions_data, items_data)

    def __getitem__(self, language: Language):
        return self._cache.get(language)

    def _needs_refreshing(self, language: Language = Language.English) -> bool:
        entry = self._cache.get(language)
        return entry is None or datetime.utcnow() >= entry._expires_at

    def get_champion(
        self,
        champion: Union[str, int],
        language: Language = Language.English,
        *,
        fuzzy: bool = False,
    ) -> Optional[Champion]:
        """
        Returns a champion for the given Name or ID, and Language specified.
        Case sensitive.

        This method can return `None` or stale data if the entry hasn't been fetched yet,
        or haven't been updated in a while.\n
        Consider using the `get_champion_info` method from the main API instead.

        Parameters
        ----------
        champion : Union[str, int]
            The Name or ID of the champion you want to get.
        language : Language
            The `Language` you want to get the champion in.\n
            Defaults to `Language.English`.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Champion]
            The champion you requested.\n
            `None` is returned if a champion couldn't be found, or the entry for the language
            specified hasn't been fetched yet.
        """
        entry = self._cache.get(language)
        if entry:
            return entry.get_champion(champion, fuzzy=fuzzy)
        return None

    def get_card(
        self,
        card: Union[str, int],
        language: Language = Language.English,
        *,
        fuzzy: bool = False,
    ) -> Optional[Device]:
        """
        Returns a card for the given Name or ID, and Language specified.
        Case sensitive.

        This method can return `None` or stale data if the entry hasn't been fetched yet,
        or haven't been updated in a while.\n
        Consider using the `get_champion_info` method from the main API instead.

        Parameters
        ----------
        card : Union[str, int]
            The Name or ID of the card you want to get.
        language : Language
            The `Language` you want to get the card in.\n
            Defaults to `Language.English`.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Device]
            The card you requested.\n
            `None` is returned if a card couldn't be found, or the entry for the language
            specified hasn't been fetched yet.
        """
        entry = self._cache.get(language)
        if entry:
            return entry.get_card(card, fuzzy=fuzzy)
        return None

    def get_talent(
        self,
        talent: Union[str, int],
        language: Language = Language.English,
        *,
        fuzzy: bool = False,
    ) -> Optional[Device]:
        """
        Returns a talent for the given Name or ID, and Language specified.
        Case sensitive.

        This method can return `None` or stale data if the entry hasn't been fetched yet,
        or haven't been updated in a while.\n
        Consider using the `get_champion_info` method from the main API instead.

        Parameters
        ----------
        talent : Union[str, int]
            The Name or ID of the talent you want to get.
        language : Language
            The `Language` you want to get the talent in.\n
            Defaults to `Language.English`.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Device]
            The talent you requested.\n
            `None` is returned if a talent couldn't be found, or the entry for the language
            specified hasn't been fetched yet.\n
        """
        entry = self._cache.get(language)
        if entry:
            return entry.get_talent(talent, fuzzy=fuzzy)
        return None

    def get_item(
        self,
        item: Union[str, int],
        language: Language = Language.English,
        *,
        fuzzy: bool = False,
    ) -> Optional[Device]:
        """
        Returns a shop item for the given Name or ID, and Language specified.
        Case sensitive.

        This method can return `None` or stale data if the entry hasn't been fetched yet,
        or haven't been updated in a while.\n
        Consider using the `get_champion_info` method from the main API instead.

        Parameters
        ----------
        item : Union[str, int]
            The Name or ID of the item you want to get.
        language : Language
            The `Language` you want to get the shop item in.\n
            Defaults to `Language.English`.
        fuzzy : bool
            When set to `True`, makes the Name search case insensitive.\n
            Defaults to `False`.

        Returns
        -------
        Optional[Device]
            The shop item you requested.\n
            `None` is returned if a shop item couldn't be found, or the entry for the language
            specified hasn't been fetched yet.
        """
        entry = self._cache.get(language)
        if entry:
            return entry.get_item(item, fuzzy=fuzzy)
        return None
