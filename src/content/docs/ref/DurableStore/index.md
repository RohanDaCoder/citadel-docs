---
title: "DurableStore type"
description: "Shared durable stores"
---

Shared durable stores. Calls yield; pcall catches structured errors such as {err = "conflict", version = 3}. One store per experience.

## Functions

| Call                                            | Purpose                                                                                                                     |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [`get`](/ref/DurableStore/get/)                 | Returns a fact's value and its version; version 0 means absent.                                                             |
| [`set`](/ref/DurableStore/set/)                 | Writes a fact if its version is still `if_version`, and returns the new version. A mismatch errors with {err = "conflict"}. |
| [`delete`](/ref/DurableStore/delete/)           | Removes a fact if its version is still `if_version`.                                                                        |
| [`increment`](/ref/DurableStore/increment/)     | Adds `by` to a number atomically, starting at zero, and returns the result. Never retry it blindly after a timeout.         |
| [`list`](/ref/DurableStore/list/)               | Returns fact keys with this prefix and the cursor for the next page, or nil at the end.                                     |
| [`blob_get`](/ref/DurableStore/blob_get/)       | Returns one player's binary blob, or nil, and its version; `owner` is the player's uuid.                                    |
| [`blob_put`](/ref/DurableStore/blob_put/)       | Writes a player's binary blob if its version is still `if_version`, and returns the new version. At most 32 MiB.            |
| [`blob_delete`](/ref/DurableStore/blob_delete/) | Deletes a player's blob if its version is still `if_version`.                                                               |
