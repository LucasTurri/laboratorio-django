import json
import os
from pathlib import Path

import django
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import transaction


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from blog.models import Post

    call_command("migrate", interactive=False)
    user_model = get_user_model()

    with transaction.atomic():
        if not Post.objects.exists():
            fixture = Path(__file__).with_name("demo_data.json")
            records = json.loads(fixture.read_text(encoding="utf-8"))
            author_ids = {
                item["fields"]["author"]
                for item in records
                if item["model"] == "blog.comment"
            }

            for author_id in sorted(author_ids):
                author = user_model(pk=author_id, username=f"leitor-demo-{author_id}")
                author.set_unusable_password()
                author.save()

            call_command("loaddata", str(fixture))

        username = os.environ["DJANGO_SUPERUSER_USERNAME"]
        if not user_model.objects.filter(username=username).exists():
            user_model.objects.create_superuser(
                username=username,
                password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
            )


if __name__ == "__main__":
    main()