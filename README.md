# Listening To Spike

Experimental scripts to generate sound signal based on in-vitro neural spike signal. The module use OSC (open-sound control) protocol to connect to audio workstation.

## Debugging

### OSC Server

To launch test osc-server, use CLI tool:

```sh
-> % osc-listener --help
Usage: osc-listener [OPTIONS]

Options:
    --ip TEXT       The ip to listen
    --port INTEGER  The port to listen
    --help          Show this message and exit.
```
