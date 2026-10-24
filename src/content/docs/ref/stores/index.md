---
title: "stores global"
description: "The experience's shared store: versioned facts, blobs and leases across every server."
---

The experience's shared store: versioned facts, blobs and leases across every server.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call                                  | Purpose                                                                                                       |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [`open`](/ref/stores/open/)           | Returns the experience's one store. It takes no id; passing one is an error.                                  |
| [`request`](/ref/stores/request/)     | Sends one raw query to the store and yields until it answers; returns the answer table and any blob bytes.    |
| [`lease`](/ref/stores/lease/)         | Takes a lease on `key` for `holder`, lasting `ttl_ms` milliseconds (up to one hour); returns a fencing token. |
| [`renew`](/ref/stores/renew/)         | Extends the lease on `key` that `token` holds.                                                                |
| [`release`](/ref/stores/release/)     | Gives up the lease on `key` that `token` holds.                                                               |
| [`blob_list`](/ref/stores/blob_list/) | Lists a player's blobs across all blob stores in this scope, each with its store, key, version and size.      |
