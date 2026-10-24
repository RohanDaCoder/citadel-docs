---
title: "HttpResponse type"
description: "What http.get returns"
---

What `http.get` returns. A failed request is not an error: read `ok`.

## Functions

| Call                                | Purpose                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------ |
| [`json`](/ref/HttpResponse/json/)   | The body as a table; an error when it is not JSON.                       |
| [`image`](/ref/HttpResponse/image/) | A PNG body: `pixels` is 4 bytes (RGBA) a pixel, row by row from the top. |

## Fields

| Field                                                                     | Purpose                                    |
| ------------------------------------------------------------------------- | ------------------------------------------ |
| [`httpResponse.ok: boolean`](/ref/HttpResponse/ok/)                       | True for a 2xx status.                     |
| [`httpResponse.status: number`](/ref/HttpResponse/status/)                | The HTTP status; 0 when no answer came.    |
| [`httpResponse.error: string ?`](/ref/HttpResponse/error/)                | Why no answer came, or nil.                |
| [`httpResponse.body: string`](/ref/HttpResponse/body/)                    | The answer as bytes.                       |
| [`httpResponse.headers: {[string]: string }`](/ref/HttpResponse/headers/) | The answer's headers, names in lower case. |
