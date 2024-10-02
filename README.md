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
* `list`: List all posts and drafts.
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

* `-d, --draft`: Build including drafts.
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
* `set`: Set configurations.

### `blog config list`

List all configurations.

**Usage**:

```console
$ blog config list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `blog config set`

Set configurations.

**Usage**:

```console
$ blog config set [OPTIONS]
```

**Options**:

* `--mode TEXT`: Management mode.
* `--port INTEGER`: Listen on the given port.  [default: 4000]
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
$ blog info [OPTIONS] PATTERN
```

**Arguments**:

* `PATTERN`: Pattern of post or draft name.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog list`

List all posts and drafts.

**Usage**:

```console
$ blog list [OPTIONS]
```

**Options**:

* `-d, --draft`: List only all drafts.
* `-p, --post`: List only all posts.
* `--help`: Show this message and exit.

## `blog open`

Open post or draft in editor.

**Usage**:

```console
$ blog open [OPTIONS] PATTERN
```

**Arguments**:

* `PATTERN`: Pattern of post or draft name.  [required]

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
$ blog publish [OPTIONS] PATTERN
```

**Arguments**:

* `PATTERN`: Pattern of draft name.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog remove`

Remove a post or draft.

**Usage**:

```console
$ blog remove [OPTIONS] PATTERN
```

**Arguments**:

* `PATTERN`: Pattern of post or draft name.  [required]

**Options**:

* `--help`: Show this message and exit.

## `blog serve`

Start blog server locally through jekyll.

**Usage**:

```console
$ blog serve [OPTIONS]
```

**Options**:

* `-d, --draft`: Start blog server with drafts.
* `--port INTEGER`: Listen on the given port.  [default: 4000]
* `--help`: Show this message and exit.

## `blog unpublish`

Unpublish a post.

**Usage**:

```console
$ blog unpublish [OPTIONS] PATTERN
```

**Arguments**:

* `PATTERN`: Pattern of post name.  [required]

**Options**:

* `--help`: Show this message and exit.
