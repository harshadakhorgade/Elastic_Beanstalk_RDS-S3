import django_tables2 as tables
from images.models import Image

class ImageTable(tables.Table):
    preview = tables.TemplateColumn(
        template_code="""
            {% if record.file %}
                <img src="{{ record.file.url }}" class="img-fluid" height="50" width="50">
            {% else %}
                <span class="text-muted">No image</span>
            {% endif %}
        """,
        verbose_name="Preview",
        orderable=False
    )

    class Meta:
        model = Image
        fields = ("title", "uploaded_at", "preview")
