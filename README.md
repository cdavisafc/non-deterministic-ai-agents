# A very, very non-deterministic agent

That Temporal cannot be used for AI agents because workflows need to deterministic is a MYTH!!!

While parts of Temporal applications do need to be deterministic (i.e. the fact that we will loop until
the LLM decided it has reached its goal), Temporal applications absolutely can have non-deterministic parts (i.e. an LLM and a tool that generates random numbers).

The fact that some parts need to be deterministic is what allows Temporal to pick up exactly where it left off
after a failure. That is goodness.

In short, it's absolutely not hard to build AI agents with Temporal - and as a bonus, they are durable!

# Running the app

Run the worker:

```bash
uv run python -m worker
```

Start the agent:

```bash
uv run python -m start_workflow"
```

