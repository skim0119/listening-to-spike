# Listening To Spike

Experimental scripts to generate sound signal based on in-vitro neural spike signal. The module use OSC (open-sound control) protocol to connect to audio workstation.

```mermaid
graph LR
subgraph Neuron Culture
M[MEA] --> D[(Data Base)]
end
subgraph Processing
F[Collector]
O(MiV-OS) -->|Spiketrain| F
end
D -->|Raw Signal| O
subgraph Audio Workstation
c1((channel 1))
c2((channel 2))
c3((channel 3))
e(...)
end
F --> o
o([OSC])
o --> c1
o --> c2
o --> c3
o --> e
```

## Installation

> At this moment, we only support `Mac-OS` for single-file installation. For other OSs, user can install the package and dependencies using `poetry`.

The installation package (`.dmg` file) can be found [here](https://github.com/skim0119/listening-to-spike/releases).

## How to Use

1. Select spike-recording to load. (This process can take some time, depending on the size of the signal)
2. Configure IP and port number for OSC protocol.
3. Click play (_stop button is not functioning at this point_)

<img width="825" alt="image" src="https://user-images.githubusercontent.com/3798023/191491697-6de802fd-6609-41c4-a432-c11c4463fd75.png">

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
