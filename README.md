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
uv run python -m start_workflow
```
## Surviving outages

Because this agent uses Temporal for resilience, it will survive a whole host of different infrastructure problems. Here are just a couple:

### Network outages - using `pfctl` on a Mac

We will cause network outages with some firewall rules.

We will simulate a network outage by adding firewall rules using `pfctl`. This repository includes a `pf.rules` file that firewall
rules to block access to both the OpenAI API and the National Weather Service (NWS) APIs. The former IPs are quite stable, but for the
latter (NWS) the DNS resolution often returns different IPs. If you find the rules in the `pf.rules` file are not blocking access
to the NWS APIs, check for new IPs by running the following command:
```
dig +short api.weather.gov
```
After editing the `pf.rules` file to suit your case, you can use the following commands to set and delete the rules, and enable and disable the firewall.

To set rules
```
sudo pfctl -f pf.rules
```

To remove the rules. WARNING: this will delete all rules - you are using pfctl for real, use with caution.
```
sudo pfctl -F all
```

To see the current list of rules:
```
sudo pfctl -s rules
```

To enable the firewall
```
sudo pfctl -e
```

To enable the firewall
```
sudo pfctl -d
```

### Agent crash

You can kill the worker in the middle of running the agent and it will pick up where it left off when you restart the worker.