# outbox module

A reusable shared library for nextweekwithus domain components including Outbox pattern implementation, historical logging, and other shared utilities. This library is designed to provide ready-to-use components across all projects in the nextweekwithus ecosystem.

## Overview

**outbox module** is not just an outbox library—it serves as a centralized repository for all shared utilities and components used across nextweekwithus projects. Currently includes:

- **Outbox Pattern**: Reliable message publishing with transactional guarantees
- **Shared Utilities**: Common enums, exceptions, and utility functions

## Installation

Install the package directly from the Git repository:



### Using in requirements.txt

Add the following line to your `requirements.txt`:


**Note**: Replace `v1.0.0` with the specific version tag you want to use.

## Django Setup

### 1. Add to Installed Apps

Add the Outbox app configuration to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your other apps
    "outbox.apps.OutboxConfig",
]
```

### 2. Run Migrations

Apply the outbox migrations to your database:

```bash
python manage.py migrate outbox
```

### 3. Configuration (Optional)

Configure the outbox settings in your Django settings if needed:

```python
# settings.py
import os

outbox = {
    "PROJECT_TAG": "this have to be your project name for example nextweekwithus",
    "OUTBOX": {
        "HTTP_PUBLISHER": {
            "NO_SQL_WRAPPER": {
                "SINGLE": os.environ.get("SINGLE_HTTP_PUBLISHER", "single_http_publisher_url"),
                "BULK": os.environ.get("SINGLE_HTTP_PUBLISHER", "bulk_http_publisher_url"),
            },
        },
        "CACHE_PUBLISHER": {
            "REDIS": {
                "HOST": os.environ.get("REDIS_HOST", "localhost"),
                "PORT": int(os.environ.get("REDIS_PORT", 6379)),
                "PASSWORD": os.environ.get("REDIS_PASSWORD", None),
                "DB": int(os.environ.get("REDIS_DB", 0)),
                "TTL": int(os.environ.get("REDIS_TTL", 3600)),
            }
        },
    }
}
```

## Versioning and Tagging Best Practices

This package follows **Semantic Versioning** (SemVer):

- **Major (x.0.0)**: Breaking changes that require code modifications in consuming projects
- **Minor (x.y.0)**: New features that are backward compatible
- **Patch (x.y.z)**: Bug fixes and small improvements

Current version: `1.0.0`

### When to Create Tags

Create a new tag for every significant change:

- **`feat:`** New feature added → Increment **minor** version (1.0.0 → 1.0.0)
- **`fix:`** Bug fix → Increment **patch** version (1.0.0 → 1.0.1)
- **`refactor:`** Code refactoring → Increment **patch** version (1.0.0 → 1.0.1)
- **`breaking:`** Breaking change → Increment **major** version (1.0.0 → 2.0.0)

### Release Process

Follow these steps for every release:

#### Step 1: Update Version

Update the version in `pyproject.toml`:

```toml
[project]
version = "1.0.0"  # Update to new version
```

#### Step 2: Generate Migrations (if models changed)

If you modified any models, generate and include migration files:

```bash
# Generate new migrations
python manage.py makemigrations outbox

# Test migrations locally
python manage.py migrate outbox

# Add migration files to git
git add outbox/outbox/migrations/
```

#### Step 3: Commit Changes

```bash
git add pyproject.toml
git add .  # Include any other changes
git commit -m "feat: add new feature X"  # Use conventional commit format
```

#### Step 4: Create and Push Tag

```bash
# Create a tag matching the version
git tag -a v1.0.0 -m "always mention changes you have maid here"

# Push the commit
git push origin your-develop-branch

# Push the tag
git push origin v1.0.0
```

**Important**: Always create tags **after** committing your changes. The tag should point to a commit that includes the version update.

#### Step 5: Update Consumer Projects

Update the version in your target project's `requirements.txt`:



Then reinstall the package:

#### Step 6: Run Migrations in Consumer Projects

If there were model changes, run migrations in your consumer project:

```bash
python manage.py migrate outbox
```

## Migration Management

### Creating Migrations

When you modify models in `outbox`:

```bash
# Generate migrations
python manage.py makemigrations outbox

# Review the generated migration file
# located in outbox/outbox/migrations/

# Test locally
python manage.py migrate outbox
```

### Applying Migrations in Consumer Projects

After updating to a new version with model changes:

```bash
# Apply outbox migrations
python manage.py migrate outbox
```

**Always** commit and push migration files together with your model changes.

## Development Workflow Example

Here's a complete example of adding a new feature:

```bash
# 1. Make your changes to the code
vim outbox/outbox/models.py

# 2. Generate migrations if models changed
python manage.py makemigrations outbox

# 3. Update version in pyproject.toml
vim pyproject.toml  # Change version from 1.0.0 to 1.0.0

# 4. Commit everything
git add .
git commit -m "feat: add new outbox retry mechanism"

# 5. Create and push tag
git tag -a v1.0.0 -m "always mention changes you have maid here"
git push origin your-dyour-devdelop-branchevdelop-branch
git push origin v1.0.0

# 6. Update consumer projects
# Update requirements.txt with new version
# Run: pip install --upgrade --force-reinstall git+https://...@v1.0.0
# Run: python manage.py migrate outbox if any changes in model 
```

## Contributing

When contributing to this library:

1. Follow semantic versioning principles
2. Use conventional commit messages (`feat:`, `fix:`, `refactor:`, etc.)
3. Always generate and commit migration files for model changes
4. Create appropriate tags for releases
5. Update version in `pyproject.toml` before tagging
6. Test migrations locally before pushing

## Support

---

**Current Version**: 1.0.0  
