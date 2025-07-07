# tools/memory_utils.py

def store_tool_output(context, tool_name: str, summary: str, metadata: dict = None):
    """Writes a tool's summary into memory with optional metadata."""
    metadata = metadata or {}
    metadata.update({"source_tool": tool_name})
    context.memory.add_memory_entry(text=summary, metadata=metadata)
