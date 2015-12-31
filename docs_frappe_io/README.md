### docs.frappe.io

### Hooks

```
autodoc = {
  "for_app": "frappe",
  "docs_app": "docs_frappe_io"
}
```

### Build

    # build src (from frappe)
    $ bench setup-docs

    # make htmls
    $ bench build-docs

    # sync statics
    $ bench sync_statics --force

### Update

- Move current pages to new folder within `www`
- Build docs again, a new folder will be created for a new version
- Update home page
- Delete pages from src if errors
