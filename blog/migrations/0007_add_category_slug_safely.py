# blog/migrations/000X_add_category_slug_safely.py
from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slugs(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    # Build a set for fast membership checks
    existing = set(Category.objects.exclude(slug__isnull=True).exclude(slug="").values_list("slug", flat=True))

    for cat in Category.objects.all():
        if not getattr(cat, "slug", None):
            base = slugify(cat.name) or "category"
            slug = base
            i = 1
            # Ensure uniqueness across all categories (including ones we just set in this loop)
            while slug in existing:
                slug = f"{base}-{i}"
                i += 1
            cat.slug = slug
            cat.save(update_fields=["slug"])
            existing.add(slug)

class Migration(migrations.Migration):

    # IMPORTANT: set this to your latest applied blog migration
    dependencies = [
        ("blog", "0005_alter_post_image"),  # <-- change this!
    ]

    operations = [
        # 1) Add field as nullable & non-unique so the DB accepts it
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=50, blank=True, null=True, db_index=True),
        ),
        # 2) Populate slugs safely
        migrations.RunPython(generate_unique_slugs, reverse_code=migrations.RunPython.noop),
        # 3) Enforce constraints after data is clean
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=50, unique=True),  # now NOT NULL by default
        ),
    ]
