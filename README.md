# Jekyll CLI

Jekyll Blog CLI Tool.

**Usage**:

```console
$ blog [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `build`: Build jekyll site.
* `config`: Configuration Subcommands.
* `draft`: Create a draft.
* `info`: Show info about post or draft.
* `init`: Initialize the application interactively.
* `list`: List all posts and drafts or find items by...
* `open`: Open post or draft in editor.
* `post`: Create a post.
* `publish`: Publish a draft.
* `remove`: Remove a post or draft.
* `serve`: Start blog server locally through jekyll.
* `unpublish`: Unpublish a post.

## `blog build`

Build jekyll site.

**Usage**:

```console
$ blog build [OPTIONS]
```

**Options**:

* `--draft / --no-draft`: Build including drafts.  [default: no-draft]
* `--help`: Show this message and exit.

## `blog config`

Configuration Subcommands.

**Usage**:

```console
$ blog config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all configurations.
* `set`: Set a configuration.

### `blog config list`

List all configurations.

**Usage**:

```console
$ blog config list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `blog config set`

Set a configuration.

**Usage**:

```console
$ blog config set [OPTIONS] KEY VALUE
```

**Arguments**:

* `KEY`: Configuration key using dot-notation.  [required]
* `VALUE`: Configuration value.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog draft`

Create a draft.

**Usage**:

```console
$ blog draft [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of draft item.  [required]

**Options**:

* `-t, --title TEXT`: Title of draft.
* `-c, --class TEXT`: Categories of draft.
* `-g, --tag TEXT`: Tags of draft.
* `-o, --open`: Open draft after creation.
* `--help`: Show this message and exit.

## `blog info`

Show info about post or draft.

**Usage**:

```console
$ blog info [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of post or draft.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog init`

Initialize the application interactively.

**Usage**:

```console
$ blog init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `blog list`

List all posts and drafts or find items by name.

**Usage**:

```console
$ blog list [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: Name of post or draft.

**Options**:

* `-d, --draft`: List only all drafts.
* `-p, --post`: List only all posts.
* `--help`: Show this message and exit.

## `blog open`

Open post or draft in editor.

**Usage**:

```console
$ blog open [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of post or draft.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog post`

Create a post.

**Usage**:

```console
$ blog post [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of post item.  [required]

**Options**:

* `-t, --title TEXT`: Title of post.
* `-c, --class TEXT`: Categories of post.
* `-g, --tag TEXT`: Tags of post.
* `-o, --open`: Open post after creation.
* `--help`: Show this message and exit.

## `blog publish`

Publish a draft.

**Usage**:

```console
$ blog publish [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of draft.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog remove`

Remove a post or draft.

**Usage**:

```console
$ blog remove [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of post or draft.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog serve`

Start blog server locally through jekyll.

**Usage**:

```console
$ blog serve [OPTIONS]
```

**Options**:

* `--draft / --no-draft`: Start blog server with drafts.  [default: no-draft]
* `--port INTEGER`: Listen on the given port.  [default: 4001]
* `--help`: Show this message and exit.

## `blog unpublish`

Unpublish a post.

**Usage**:

```console
$ blog unpublish [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Name of post.  [required]

**Options**:

* `--help`: Show this message and exit.
