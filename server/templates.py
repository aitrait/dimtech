from jinja2 import Environment, PrefixLoader, FileSystemLoader


template_env = Environment(
    loader=PrefixLoader({
        "user": FileSystemLoader("modules/user/templates"),
        "admin": FileSystemLoader("modules/admin/templates")
    })
)
