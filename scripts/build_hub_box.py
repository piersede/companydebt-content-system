"""
Generate a wp:acf/hub-box Gutenberg block from a plain Python definition.

Usage:
    from scripts.build_hub_box import hub_box_block

    block = hub_box_block([
        {
            "heading": "Types of Liquidation",
            "items": [
                ("Creditors' Voluntary Liquidation", "/liquidation/creditors-voluntary-liquidation/"),
                ("Compulsory Liquidation",            "/liquidation/compulsory-liquidation/"),
            ],
        },
        {
            "heading": "Director Consequences",
            "items": [
                ("Director Disqualification", "/liquidation/director-disqualification/"),
            ],
        },
    ])

Or run directly to preview output:
    python scripts/build_hub_box.py
"""

import json

# ACF field IDs — must match the registered hub-box block field group
_F = {
    "bcg_image_or_icon": "field_63db793eeff55",
    "icon":              "field_63db796beff56",
    "heading":           "field_63db7984eff57",
    "style":             "field_63e0c5d43a570",
    "list_item_title":   "field_63db79a9eff59",
    "list_item_url":     "field_63db79b9eff5a",
    "list_item":         "field_63db7994eff58",
    "view_all":          "field_63db79c8eff5b",
    "boxes":             "field_63db7a841bb00",
    "hub_boxes":         "field_63db7922eff54",
}


def hub_box_block(sections: list[dict]) -> str:
    """
    Build the full <!-- wp:acf/hub-box ... /--> block string.

    Each section dict:
        heading (str): card heading
        items   (list of (title, url) tuples)
        style   (str, optional): "list" (default) or "description"
        description (str, optional): used when style="description"
    """
    data: dict = {}

    for i, section in enumerate(sections):
        prefix = f"hub_boxes_boxes_{i}_"
        heading = section["heading"]
        style = section.get("style", "list")

        data[f"{prefix}bcg_image_or_icon"] = "background"
        data[f"_{prefix}bcg_image_or_icon"] = _F["bcg_image_or_icon"]
        data[f"{prefix}icon"] = ""
        data[f"_{prefix}icon"] = _F["icon"]
        data[f"{prefix}heading"] = heading
        data[f"_{prefix}heading"] = _F["heading"]
        data[f"{prefix}style"] = style
        data[f"_{prefix}style"] = _F["style"]

        if style == "description":
            data[f"{prefix}content"] = section.get("description", "")
            data[f"_{prefix}content"] = "field_63e0c6153a571"
        else:
            items = section.get("items", [])
            for j, (title, url) in enumerate(items):
                data[f"{prefix}list_item_{j}_title"] = title
                data[f"_{prefix}list_item_{j}_title"] = _F["list_item_title"]
                data[f"{prefix}list_item_{j}_url"] = url
                data[f"_{prefix}list_item_{j}_url"] = _F["list_item_url"]
            data[f"{prefix}list_item"] = len(items)
            data[f"_{prefix}list_item"] = _F["list_item"]

        data[f"{prefix}view_all"] = "0"
        data[f"_{prefix}view_all"] = _F["view_all"]

    data["hub_boxes_boxes"] = len(sections)
    data["_hub_boxes_boxes"] = _F["boxes"]
    data["hub_boxes"] = ""
    data["_hub_boxes"] = _F["hub_boxes"]

    payload = json.dumps({"name": "acf/hub-box", "data": data, "mode": "edit"},
                         ensure_ascii=False)
    return f"<!-- wp:acf/hub-box {payload} /-->"


if __name__ == "__main__":
    demo = hub_box_block([
        {
            "heading": "Section One",
            "items": [
                ("Guide A", "/path/to/a/"),
                ("Guide B", "/path/to/b/"),
            ],
        },
        {
            "heading": "Section Two",
            "items": [
                ("Guide C", "/path/to/c/"),
            ],
        },
    ])
    print(demo[:200], "...")
