from fastmcp import FastMCP
from okf import OKFBundle
from os import getenv

BUNDLE_PATH = getenv("BUNDLE_PATH")
mcp = FastMCP("OKF MCP server")

bundle_path = "./bundle"
bundle = OKFBundle(bundle_path)


@mcp.tool
def okf_read_concept(concept_id: str) -> str:
    c = bundle.get(concept_id)
    if not c:
        return f"No concept found with id '{concept_id}'. Try okf_list_concepts."
    return c.as_text()


@mcp.tool
def okf_list_concepts() -> str:
    return "\n".join(bundle.list_ids())


@mcp.tool
def okf_get_links(concept_id: str) -> str:
    neighbors = bundle.neighbors(concept_id)
    if not neighbors:
        return f"'{concept_id}' has no outgoing links, or does not exist."
    return "\n".join(f"{n.concept_id} ({n.type}): {n.title}" for n in neighbors)


@mcp.tool
def okf_find_by_tag(tag: str) -> str:
    matches = bundle.by_tag(tag)
    if not matches:
        return f"No concepts tagged '{tag}'."
    return "\n".join(f"{c.concept_id} ({c.type}): {c.title}" for c in matches)


@mcp.tool
def okf_find_by_type(type_: str) -> str:
    matches = bundle.by_type(type_)
    if not matches:
        return f"No concepts of type '{type_}'."
    return "\n".join(f"{c.concept_id}: {c.title}" for c in matches)


if __name__ == "__main__":
    mcp.run()
