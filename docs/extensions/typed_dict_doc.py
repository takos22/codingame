from typing import Any, Dict, Optional

from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter


class TypedDictAttrs:
    def __init__(self, type_dict: Dict[str, Any]):
        self.type_dict = type_dict

    def __getattr__(self, name) -> Optional[Any]:
        return self.type_dict[name]


class TypeDictClassDocumenter(ClassDocumenter):
    objtype = "typeddict"
    directivetype = "class"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options.undoc_members = True

    def get_attr(self, obj: Any, name: str, *defargs: Any) -> Any:
        if obj is self.object:
            return super().get_attr(
                TypedDictAttrs(self.object.__annotations__), name, *defargs
            )
        return super().get_attr(obj, name, *defargs)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_autodocumenter(TypeDictClassDocumenter)

    return {"version": "0.1.0", "parallel_read_safe": True}
