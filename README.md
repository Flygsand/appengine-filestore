# appengine-filestore

appengine-filestore is a RESTful HTTP file store for Google App
Engine. Kinda like a poor man's S3, but cooler. Here are the basic
operations:

    PUT /<filename> HTTP/1.1
    ...
    <body>

Creates an entry for a file named `<filename>` with the data given by
`<body>` into the file store. Returns a `201 Created` along with a
unique identifier (UUID) as the response body. This identifier is used
to refer to the file in subsequent operations.

    GET /<uuid> HTTP/1.1

Returns a `200 OK` and the contents of the file referenced by
`<uuid>`, or a `404 Not Found` if `<uuid>` was not referencing any
file in the file store.

    DELETE /<uuid> HTTP/1.1

Deletes the file referenced by `uuid` and returns a `200 OK`, or a
`404 Not Found` if `<uuid>` was not referencing any file in the file
store.

