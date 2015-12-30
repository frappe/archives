# Models

In wnlib, the standard terminology used for a single data record is `Document` and
for a collection of Documents is `DocList`. All objects in the system are usually `DocList`
type objects, even if there is only one record.

A collection type is class a `DocType`. `Customer` is a `DocType`, `Sales Order` is a `DocType`
and so on, even a `DocType` is a `DocType`. The properties of a `DocType` are called
`DocField`. Each `DocField` could be a scalar property, or a link (foreign key) or a placeholder
for a parent child relation (table).

## Creating models

