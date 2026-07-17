# Sample Report

Smoke-test input for the publish toolchain (mermaid-cli + md-to-pdf). Run
the skill's publishing commands against this file; a correct setup produces
a small PDF whose diagram below is rendered as an image, not left as a code
block. Do not commit the output.

## A system, minimally

```mermaid
graph LR
    User(("User")) --> App["Sample app"]
    App --> DB[("Data store")]
    App --> Ext["External API"]
```

## And a flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant D as Data store
    U->>A: request
    A->>D: query
    D-->>A: rows
    A-->>U: response
```

If both diagrams appear as images in the PDF, the toolchain works.
