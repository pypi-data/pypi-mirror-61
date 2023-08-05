import os
from weasyprint import HTML
from jinja2 import Template


def create_pdf(template_file_path, template_assets_dir, output_file_path, kv_pairs):
    """Converts Jinja2 templates to PDF

    :param template_file_path: Path to template filename
    :param template_assets_dir: Assets used by the template
    :param output_file_path: Output file path
    :param kv_pairs: Jinja2 key/value pairs

    :return: None
    """

    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(template_file_path, 'r') as file:
        template_html = Template(file.read())
        rendered_html = template_html.render(kv_pairs)

        HTML(string=rendered_html, base_url=template_assets_dir).write_pdf(output_file_path)
