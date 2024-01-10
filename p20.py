import sys
from numpy import lcm


LOW = 0
HIGH = 1


def ingest_p20(lines):
    data = {}
    for line in lines:
        elems = line.strip().split()
        if elems[0] == "broadcaster":
            mod_type = "B"
            name = "broadcaster"
        else:
            mod_type = elems[0][0]
            name = elems[0][1:]
        dests = [elem.rstrip(",") for elem in elems[2:]]
        data[name] = (mod_type, dests)

    return data


class Module:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests

class FlipFlop(Module):
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.is_on = False

    def pulse(self, pulse_type, source_name):
        if pulse_type == LOW:
            self.is_on = not self.is_on
            pulse_type_send = HIGH if self.is_on else LOW
            return [(self.name, dest, pulse_type_send) for dest in self.dests]
        else:
            return []

    def register(self, source_name):
        pass


class Conjunction(Module):
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.memory = {}

    def pulse(self, pulse_type, source_name):
        self.memory[source_name] = pulse_type
        pulse_type_send = LOW if all(x == HIGH for x in self.memory.values()) else HIGH
        return [(self.name, dest, pulse_type_send) for dest in self.dests]

    def register(self, source_name):
        self.memory[source_name] = LOW


class Broadcaster(Module):
    def __init__(self, name, dests):
        super().__init__(name, dests)

    def pulse(self, pulse_type, source_name):
        return [(self.name, dest, pulse_type) for dest in self.dests]

    def register(self, source_name):
        pass


def create_modules(data):
    modules = {}
    for name, (mod_type, dests) in data.items():
        module = (FlipFlop(name, dests) if mod_type == "%" else
                  Conjunction(name, dests) if mod_type == "&" else
                  Broadcaster(name, dests))
        modules[name] = module
    for name, module in modules.items():
        for dest in module.dests:
            module = modules.get(dest)
            if module is not None:
                module.register(name)

    return modules


def p20a(modules):
    pulse_counts = {LOW: 0, HIGH: 0}
    for ipush in range(1000):
        tasks = [(None, "broadcaster", LOW)]
        while len(tasks) > 0:
            src, dest, pulse_type = tasks.pop(0)
            module = modules.get(dest)
            if module is not None:
                tasks.extend(module.pulse(pulse_type, src))
            pulse_counts[pulse_type] += 1

    return pulse_counts[LOW] * pulse_counts[HIGH]


def p20b():
    """The graph set up in the input is a set of four 12-bit counters
    made up of 12 FlipFlops. Each one reports some of its bits into a
    Conjunction. The Conjunction is hooked back up to some of the
    bits, and sends (ineffectual) HIGH pulses most of the time. But
    when first those particular bits are all on, the Conjunction sends
    a LOW pulse to all the bits that are off, which turns them on, and
    to the first (least significant) bit, causing a cascade that zeros
    all the bits and resets the counter.

    Each of the four counters rolls over at a different number because
    it has different bits hooked up to the Conjunction. When all four
    Conjuctions roll over on the same button press, the output node
    receives a LOW pulse. So the number of button presses is the least
    common multiple (LCM) of the four cycle lengths.
    """
    # Get the cycle lengths by drawing a graph of the inputs and
    # finding the bits hooked up to the Conjunction
    cycle_lengths = [0b111011010101,
                     0b111101001101,
                     0b111010010101,
                     0b111100100101]

    return lcm.reduce(cycle_lengths)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <infile>".format(sys.argv[0]))
        sys.exit(1);

    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
    data = ingest_p20(lines)
    modules = create_modules(data)

    print("Problem 20a: {}".format(p20a(modules)))
    print("Problem 20b: {}".format(p20b()))
