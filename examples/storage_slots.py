from utils.Storage import Storage

store = Storage()
store.search_storage_slots("0xBb2b8038a1640196FbE3e38816F3e67Cba72D940", '2260fac5e5542a773aa44fbcfedf7c193bc2c599', nslots=10)

slot_value = store.get_storage_slot("0xBb2b8038a1640196FbE3e38816F3e67Cba72D940", 6)
print(slot_value)

