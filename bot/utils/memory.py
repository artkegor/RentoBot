class FormMemory:
    """In-memory storage for users form answers."""
    def __init__(self):
        self._data = {}

    def set_answer(self, user_id: int, form: str, question: str, answer):
        self._data.setdefault(user_id, {}) \
            .setdefault(form, {})[question] = answer

    def get_answers(self, user_id: int, form: str) -> dict:
        return self._data.get(user_id, {}).get(form, {})

    def get_answer(self, user_id: int, form: str, question: str):
        return self._data.get(user_id, {}).get(form, {}).get(question)

    def clear_form(self, user_id: int, form: str):
        if user_id in self._data and form in self._data[user_id]:
            del self._data[user_id][form]


class ListingsMemory:
    """In-memory storage for users listings and pagination."""
    def __init__(self):
        self._data = {}

    def set_listings(self, user_id: int, key: str, listings: list[int]):
        self._data.setdefault(user_id, {})[key] = {
            "listings": listings,
            "page": 0,
        }

    def get_listings(self, user_id: int, key: str) -> list[int] | None:
        return self._data.get(user_id, {}).get(key, {}).get("listings")

    def get_page(self, user_id: int, key: str) -> int:
        return self._data.get(user_id, {}).get(key, {}).get("page", 0)

    def set_page(self, user_id: int, key: str, page: int):
        if user_id in self._data and key in self._data[user_id]:
            self._data[user_id][key]["page"] = page

    def clear(self, user_id: int, key: str):
        if user_id in self._data:
            self._data[user_id].pop(key, None)


form_memory = FormMemory()
listings_memory = ListingsMemory()
