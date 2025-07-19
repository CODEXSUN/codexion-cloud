import os
import re
from jinja2 import Environment, FileSystemLoader
from cloud.utils.jinja_cleanup import postprocess_rendered

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def generate_from_template(template_name: str, output_filename: str, context: dict, output_dir: str):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(template_name)

    rendered = template.render(context)
    final_output = postprocess_rendered(rendered)

    output_path = os.path.join(output_dir, output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(final_output)


def generate_template_to_string(template_name: str, context: dict = None) -> str:
    context = context or {}
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(template_name)

    rendered = template.render(context)

    # Inline postprocess for quick use
    rendered = re.sub(r"@@B@@", "\n", rendered)
    rendered = re.sub(r"{#(?!\.r).*?#}", "", rendered, flags=re.DOTALL)

    return rendered.strip()
