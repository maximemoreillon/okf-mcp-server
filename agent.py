from langchain.agents import create_agent
from langchain.tools import tool

from dotenv import load_dotenv
from okf import OKFBundle

load_dotenv()


def build_okf_tools(bundle: OKFBundle) -> list:
    """Returns a list of LangChain tools bound to this specific bundle."""

    @tool
    def okf_read_concept(concept_id: str) -> str:
        """Read the full content of one OKF concept by its ID
        (the file path without the .md extension, e.g. 'tables/users').
        Returns frontmatter + body as text, or an error if not found."""
        c = bundle.get(concept_id)
        if not c:
            return f"No concept found with id '{concept_id}'. Try okf_list_concepts."
        return c.as_text()

    @tool
    def okf_list_concepts() -> str:
        """List every concept ID in the bundle. Use this to see what's
        available before reading a specific concept."""
        return "\n".join(bundle.list_ids())

    @tool
    def okf_get_links(concept_id: str) -> str:
        """List the concept IDs that a given concept links to (its
        neighbors in the knowledge graph). Use this to navigate outward
        from a concept instead of reading the whole bundle."""
        neighbors = bundle.neighbors(concept_id)
        if not neighbors:
            return f"'{concept_id}' has no outgoing links, or does not exist."
        return "\n".join(f"{n.concept_id} ({n.type}): {n.title}" for n in neighbors)

    @tool
    def okf_find_by_tag(tag: str) -> str:
        """Find concept IDs tagged with a given tag."""
        matches = bundle.by_tag(tag)
        if not matches:
            return f"No concepts tagged '{tag}'."
        return "\n".join(f"{c.concept_id} ({c.type}): {c.title}" for c in matches)

    @tool
    def okf_find_by_type(type_: str) -> str:
        """Find concept IDs of a given type (e.g. 'table', 'metric', 'runbook',
        whatever types your bundle's producer used)."""
        matches = bundle.by_type(type_)
        if not matches:
            return f"No concepts of type '{type_}'."
        return "\n".join(f"{c.concept_id}: {c.title}" for c in matches)

    return [
        okf_read_concept,
        okf_list_concepts,
        okf_get_links,
        okf_find_by_tag,
        okf_find_by_type,
    ]


def build_agent(bundle_path: str):
    """Example wiring with LangChain's tool-calling agent + Claude.
    Swap ChatAnthropic for any chat model that supports tool calling."""

    bundle = OKFBundle(bundle_path)
    tools = build_okf_tools(bundle)

    system_prompt = (
        "You are an assistant answering questions using an OKF knowledge "
        "bundle. Start with okf_list_concepts or okf_find_by_type/tag to "
        "orient yourself, then okf_read_concept to pull in only the "
        "concepts you actually need, following okf_get_links to traverse "
        "related concepts. Don't read the whole bundle up front."
    )

    agent = create_agent(
        model="gpt-5.4-mini",
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print('Usage: python agent.py /path/to/okf_bundle "your question"')
        sys.exit(1)

    bundle_path, question = sys.argv[1], sys.argv[2]
    agent = build_agent(bundle_path)
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)
