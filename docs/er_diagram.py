"""Render the ZIP-level ER diagram (Chen notation) to er_diagram.png.

Requires: pip install graphviz  (plus the Graphviz `dot`/`neato` binaries)
Run:      python er_diagram.py
"""

from graphviz import Graph

ENTITY = dict(
    shape="box",
    style="filled",
    fillcolor="#b3b3ff",
    fontname="Times-Bold",
    fontsize="20",
    width="2.0",
    height="0.65",
)
REL = dict(
    shape="diamond",
    style="filled",
    fillcolor="#b0b0b0",
    fontname="Times-Roman",
    fontsize="15",
    width="1.25",
    height="0.85",
)
ATTR = dict(
    shape="ellipse",
    style="filled",
    fillcolor="#66e033",
    fontname="Times-Roman",
    fontsize="15",
    margin="0.02",
)

g = Graph("er", engine="neato", format="png")

g.attr(
    dpi="200",
    splines="line",
    overlap="true",
    bgcolor="white",
    pad="0.3",
    labelloc="b",
    fontname="Times-Roman",
    fontsize="15",
)
g.attr(
    "edge", fontname="Times-Roman", fontsize="15", labeldistance="2.2", labelangle="25"
)


def pos(x, y):
    return f"{x},{y}!"


entities = {
    "states": ("States", 1.9, 6.0),
    "zips": ("ZIP codes", 1.9, 3.2),
    "hv": ("Home values", 7.0, 5.6),
    "rents": ("Rents", 7.0, 3.4),
    "income": ("Income", 7.0, 1.4),
    "src": ("Data sources", 12.2, 3.4),
}
for name, (label, x, y) in entities.items():
    g.node(name, label, pos=pos(x, y), **ENTITY)

attributes = [
    ("st_fips", "state_fips", True, "states", 1.1, 7.0),
    ("st_abbr", "state_abbr", False, "states", 2.7, 7.0),
    ("z_zip", "zip_code", True, "zips", 0.2, 2.0),
    ("z_city", "city", False, "zips", 1.3, 1.6),
    ("z_county", "county_name", False, "zips", 2.6, 1.6),
    ("z_region", "zillow_region_id", False, "zips", -0.3, 4.1),
    ("hv_zip", "zip_code", True, "hv", 5.7, 6.7),
    ("hv_month", "month", True, "hv", 7.0, 6.7),
    ("hv_val", "zhvi_usd", False, "hv", 8.3, 6.7),
    ("r_zip", "zip_code", True, "rents", 5.7, 4.5),
    ("r_month", "month", True, "rents", 7.0, 4.5),
    ("r_val", "zori_usd", False, "rents", 8.3, 4.5),
    ("i_zip", "zip_code", True, "income", 5.0, 0.3),
    ("i_year", "end_year", True, "income", 6.3, 0.3),
    ("i_val", "income_usd", False, "income", 7.7, 0.3),
    ("i_moe", "income_moe", False, "income", 9.2, 0.3),
    ("s_id", "source_id", True, "src", 11.4, 4.9),
    ("s_name", "series_name", False, "src", 13.0, 4.9),
    ("s_url", "source_url", False, "src", 11.4, 1.9),
    ("s_at", "retrieved_at", False, "src", 13.0, 1.9),
]
for node_id, label, is_pk, owner, x, y in attributes:
    text = f"<<u><b>{label}</b></u>>" if is_pk else label
    g.node(node_id, text, pos=pos(x, y), **ATTR)
    g.edge(owner, node_id)

relationships = [
    ("contains", "contains", 1.9, 4.6, "states", "zips"),
    ("has_hv", "has", 4.4, 5.2, "zips", "hv"),
    ("has_r", "has", 4.4, 3.4, "zips", "rents"),
    ("has_i", "has", 4.4, 2.0, "zips", "income"),
    ("prov_hv", "provides", 9.6, 5.6, "src", "hv"),
    ("prov_r", "provides", 9.6, 3.4, "src", "rents"),
    ("prov_i", "provides", 9.6, 1.4, "src", "income"),
]
for rel_id, label, x, y, one, many in relationships:
    g.node(rel_id, label, pos=pos(x, y), **REL)
    g.edge(
        rel_id, one, dir="forward", arrowhead="normal", headlabel="1"
    )  # arrow -> one side
    g.edge(rel_id, many, headlabel="0..N")

# g.attr(
#     label=(
#         "1. Each home value, rent, and income observation belongs to exactly one ZIP code and exactly one data source.\\l"
#         "2. Each ZIP code belongs to exactly one state; city and county_name are descriptive attributes of the ZIP code.\\l"
#         "3. In the observation entities (Home values, Rents, Income), the two underlined attributes form one composite primary key.\\l"
#         "Purple rectangle: entity   |   Gray diamond: relationship   |   Green oval: attribute   |   Underlined: primary key   |   "
#         "Arrow points to the one side.\\l"
#     )
# )

if __name__ == "__main__":
    out = g.render("er_diagram", cleanup=True)
    print("wrote", out)
